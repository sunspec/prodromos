#from generic_vpp_server import GenericVPPServer
#from multiprocessing import Manager

import pvlib
from datetime import timedelta
from math import ceil
import pandas as pd
import numpy as np
import statsmodels.api as sm


NS_PER_HR = 1.e9 * 3600.  # nanoseconds per hour


# Forecast functions
def solar_position(pvobj, dr):
    # returns ephemeris in a dataframe sp

    Location = pvlib.location.Location(pvobj.lat,
                                       pvobj.lon,
                                       pvobj.timezone,
                                       pvobj.alt)

    sp = pvlib.solarposition.ephemeris(dr, Location.latitude,
                                       Location.longitude)

    return sp


def _hour_angle_to_hours(times, hourangle, longitude, equation_of_time):
    """converts hour angles in degrees to hours as a numpy array"""
    naive_times = times.tz_localize(None)  # naive but still localized
    tzs = 1 / NS_PER_HR * (
        naive_times.astype(np.int64) - times.astype(np.int64))
    hours = (hourangle - longitude - equation_of_time / 4.) / 15. + 12. + tzs
    return np.asarray(hours)


def _local_times_from_hours_since_midnight(times, hours):
    """
    converts hours since midnight from an array of floats to localized times
    """
    tz_info = times.tz  # pytz timezone info
    naive_times = times.tz_localize(None)  # naive but still localized
    # normalize local, naive times to previous midnight and add the hours until
    # sunrise, sunset, and transit
    return pd.DatetimeIndex(
        (naive_times.normalize().astype(np.int64) +
         (hours * NS_PER_HR).astype(np.int64)).astype('datetime64[ns]'),
        tz=tz_info)


def _times_to_hours_after_local_midnight(times):
    """convert local pandas datetime indices to array of hours as floats"""
    times = times.tz_localize(None)
    hrs = 1 / NS_PER_HR * (
        times.astype(np.int64) - times.normalize().astype(np.int64))
    return np.array(hrs)

def sun_rise_set_transit_geometric(times, latitude, longitude, declination,
                                   equation_of_time):
    """
    Geometric calculation of solar sunrise, sunset, and transit.

    .. warning:: The geometric calculation assumes a circular earth orbit with
        the sun as a point source at its center, and neglects the effect of
        atmospheric refraction on zenith. The error depends on location and
        time of year but is of order 10 minutes.

    Parameters
    ----------
    times : pandas.DatetimeIndex
        Corresponding timestamps, must be localized to the timezone for the
        ``latitude`` and ``longitude``.
    latitude : float
        Latitude in degrees, positive north of equator, negative to south
    longitude : float
        Longitude in degrees, positive east of prime meridian, negative to west
    declination : numeric
        declination angle in radians at ``times``
    equation_of_time : numeric
        difference in time between solar time and mean solar time in minutes

    Returns
    -------
    sunrise : datetime
        localized sunrise time
    sunset : datetime
        localized sunset time
    transit : datetime
        localized sun transit time

    References
    ----------
    [1] J. A. Duffie and W. A. Beckman,  "Solar Engineering of Thermal
    Processes, 3rd Edition," J. Wiley and Sons, New York (2006)

    [2] Frank Vignola et al., "Solar And Infrared Radiation Measurements,"
    CRC Press (2012)

    """
    if not isinstance(times, pd.DatetimeIndex):
        times = pd.DatetimeIndex([times])

    latitude_rad = np.radians(latitude)  # radians
    sunset_angle_rad = np.arccos(-np.tan(declination) * np.tan(latitude_rad))
    sunset_angle = np.degrees(sunset_angle_rad)  # degrees
    # solar noon is at hour angle zero
    # so sunrise is just negative of sunset
    sunrise_angle = -sunset_angle
    sunrise_hour = _hour_angle_to_hours(
        times, sunrise_angle, longitude, equation_of_time)
    sunset_hour = _hour_angle_to_hours(
        times, sunset_angle, longitude, equation_of_time)
    transit_hour = _hour_angle_to_hours(times, 0, longitude, equation_of_time)
    sunrise = _local_times_from_hours_since_midnight(times, sunrise_hour)
    sunset = _local_times_from_hours_since_midnight(times, sunset_hour)
    transit = _local_times_from_hours_since_midnight(times, transit_hour)
    return sunrise, sunset, transit


def get_sr_ss(pvobj, dt):
    """
    Returns sunrise and sunset for local datetime dt at location of pbobj
    """
    # for sunrise and sunset calculation, time must be in timezone for location
    local_dt = dt.astimezone(pvobj.timezone)
    doy = pd.Timestamp(local_dt).dayofyear
    declination = pvlib.solarposition.declination_spencer71(doy)
    eot = pvlib.solarposition.equation_of_time_spencer71(doy)
    sr, ss, _ = sun_rise_set_transit_geometric(local_dt, pvobj.lat,
        pvobj.lon, declination, eot)
    if len(sr)==1: # return as datetime
        return sr[0], ss[0]
    else:  # return as pd.DatetimeIndex
        return sr, ss


def dniDiscIrrad(weather):
    """
    Use the DISC model to estimate the DNI from GHI

    Parameters
    -----------
    weather : pandas DataFrame
        contains the following keys:
            ghi: global horizontal irradiance in W/m2
            zenith : solar zenith angle in degrees

    Returns
    --------
    DNI : pandas Series
        direct normal irradiance
    """
    disc = pvlib.irradiance.disc(ghi=weather['ghi'],
                                 solar_zenith=weather['zenith'],
                                 datetime_or_doy=weather.index)
    # NA's show up when the DNI component is zero (or less than zero), fill with 0.
    disc.fillna(0, inplace=True)

    return disc['dni']


def DHIfromGHI(weather):
    """
    Solve for DHI from GHI and DNI
        GHI =  DHI + DNI*sin(solar altitude angle)

    Parameters
    -----------
    weather : pandas DataFrame
        contains the following keys:
            ghi : global horizontal irradiance in W/m2
            dni : direct normal irradiance in W/m2
            elevation : solar elevation in degrees

    Returns
    --------
    DHI : pandas Series
        diffuse horizontal irradiance
    """
    return weather['ghi'] - weather['dni'] * \
             np.sin(weather['elevation'] * (np.pi / 180))


def get_tracker_position(pvobj, solar_zenith, solar_azimuth):
    """
    Calculates angle of incidence aoi, panel tilt and panel azimuth for
    a single axis tracking system
    """
    
    return pvlib.tracking.singleaxis(solar_zenith, solar_azimuth,
                                     pvobj.axis_tilt, pvobj.axis_azimuth,
                                     pvobj.max_angle, pvobj.backtrack,
                                     pvobj.gcr)


def clear_sky_model(pvobj, dr):
    """
    Calculate clear-sky irradiance (GHI, DHI, DNI and POA) and related
    quantities

    Parameters
    -------------

    pvobj : instance of type PVobj

    dr : pandas DatetimeIndex
        times at which irradiance values are calculated

    Returns
    ----------
    poa : pandas Series
        plane-of-array irradiance
    """

    # get solar position information
    sp = solar_position(pvobj, dr)
    zenith = sp['zenith']
    apparent_zenith = sp['zenith']
    solar_azimuth = sp['azimuth']

#    clearSky['zenith'] = sp['zenith']
#    clearSky['elevation'] = sp['elevation']

    extraI = pvlib.irradiance.get_extra_radiation(dr)

    # calculate GHI using Haurwitz model
    haurwitz = pvlib.clearsky.haurwitz(apparent_zenith)
    ghi = haurwitz['ghi']

    disc = pvlib.irradiance.disc(ghi, zenith, dr)
    #dniDiscIrrad(clearSky)
    dni = disc['dni']

    dhi = ghi - dni * np.sin((90.0 - zenith) * (np.pi / 180))

    if not pvobj.tracking:
        aoi = pvlib.irradiance.aoi(surface_tilt=pvobj.tilt,
                                   surface_azimuth=pvobj.azimuth,
                                   solar_zenith=zenith,
                                   solar_azimuth=solar_azimuth)
        tilt = pvobj.tilt
        azimuth = pvobj.azimuth
    else:
        result = get_tracker_position(pvobj, solar_zenith=apparent_zenith,
                                      solar_azimuth=solar_azimuth)
        aoi = result['aoi']
        tilt = result['surface_tilt']
        azimuth = result['surface_azimuth']

    # Convert the AOI to radians
    aoi *= (np.pi/180.0)

    # Calculate the POA irradiance based on the given site information
    beam = pvlib.irradiance.beam_component(tilt,
                                           azimuth,
                                           zenith,
                                           solar_azimuth,
                                           dni)

    # Calculate the diffuse radiation from the sky (using Hay and Davies)
    diffuseSky = pvlib.irradiance.haydavies(tilt,
                                            azimuth,
                                            dhi,
                                            dni,
                                            extraI,
                                            zenith,
                                            solar_azimuth)

    # Calculate the diffuse radiation from the ground in the plane of array
    diffuseGround = pvlib.irradiance.get_ground_diffuse(tilt, ghi)

    # Sum the two diffuse to get total diffuse
    diffuseTotal = diffuseGround + diffuseSky

    # Sum the diffuse and beam to get the total POA irradicance
    poa = diffuseTotal + beam

    return poa


def calc_clear_index(meas, ub):
    # calculates clear-sky index of meas relative to ub
    # accepts input as pd.Series or np.ndarray
    # returns the same type as the inputs
    clearIndex = calc_ratio(meas, ub)
    clearIndex[clearIndex == np.inf] = 1.0
    clearIndex[np.isnan(clearIndex)] = 1.0

    return clearIndex


def calc_ratio(X, Y):

    # Compute the ratio X / Y
    # inputs X and Y can be pandas.Series, or np.ndarray
    # returns the same type as the inputs
    np.seterr(divide='ignore')
    ratio = np.true_divide(X, Y)
    np.seterr(divide='raise')
    return ratio


def _get_data_for_persistence(start, history, dataWindowLength):

    """
    Returns data from history for persistence forecast

    Parameters
    -----------

    pvobj : an instance of type PVobj

    start : datetime
        the time for the first forecast value

    history : pandas Series
        historical values of AC power from which the forecast is made.

    dataWindowLenth : timedelta
        time interval in history to be considered

    Returns
    ----------
    fitdata :
        data from history in period of duration dataWindowLength, prior to the
        minimum of either the forecast start or the last time in history

    """

    # find last time to include. Earliest of either forecast start or the last
    # time in history
    end_data_time = min([history.index[-1], start])
    # select data within dataWindowLength
    fitdata = history.loc[(history.index>=end_data_time - dataWindowLength) &
                         (history.index<=end_data_time)]

    return fitdata


def is_leap_year(year):
    """Determine whether a year is a leap year."""

    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def get_clearsky_power(pvobj, dr):
    # calculates clearsky AC power for pvobj at times in dr    


    poa = clear_sky_model(pvobj, dr)

    # model DC power from POA irradiance
    dc_power = poa / 1000 * pvobj.dc_capacity

    # model AC power from DC power, with clipping
    ac_power = np.where(dc_power > pvobj.ac_capacity, pvobj.ac_capacity,
                        dc_power)
    
    return ac_power


def forecast_persistence(pvobj, start, end, history, deltat,
                         dataWindowLength=timedelta(hours=1),
                         sunrise=None):

    """
    Generate forecast for pvobj from start to end at time resolution deltat
    using the persistence method applied to data in history.

    Parameters
    -----------

    pvobj : an instance of type PVobj

    start : datetime
        the time for the first forecast value

    end : datetime
        the last time to be forecast

    history : pandas Series
        historical values of AC power from which the forecast is made.

    deltat : timedelta
        the time interval for the forecast

    dataWindowLenth : timedelta
        time interval in history to be considered

    sunrise : str, default None
        method for forecasting sunrise hours, values are 'yesterday', None

    Returns
    --------
    fcst_power : pandas Series
        forecast from start to end at interval deltat
    """
    # time index for forecast
    dr = pd.DatetimeIndex(start=start, end=end, freq=deltat)

    sr, ss = get_sr_ss(pvobj, end)
    sr_yest, ss_yest = get_sr_ss(pvobj, end - timedelta(days=1))

    # length of time for after-sunrise forecast
    delta_fc = dataWindowLength + timedelta(minutes=30)

    if ((end < sr) and (start > ss_yest)):
        # forecast period is before sunrise
        fcst_power = pd.Series(data=0.0, index=dr, name='ac_power',
                               dtype=np.float)
    elif ((start < sr + delta_fc) and
          (sunrise=='yesterday') and
          (len((history.index >= start - timedelta(days=1)) &
              (history.index - timedelta(days=1) <= end))>2)):
        # forecast period is too near sunrise for history to have valid data
        # get yesterday's data +/- deltat on either side of forecast window
        # so we can interpolate to forecast points
        idata, idr = _align_data_to_forecast(start - timedelta(days=1),
                                             end - timedelta(days=1),
                                             deltat, history)
        fcst_power = idata.loc[dr - timedelta(days=1)]
        fcst_power.index = dr
        fcst_power.name = 'ac_power'
    else:
        # get data for forecast
        fitdata = _get_data_for_persistence(start, history, dataWindowLength)

        # get clear-sky power at time of year
        cspower = get_clearsky_power(pvobj, fitdata.index)

        # compute average clear sky power index

        fcst_cspower = get_clearsky_power(pvobj, dr)

        # forecast ac_power_index using persistence of clear sky power index
        fcst_power = pd.Series(data=fcst_cspower * cspower_index.mean(),
                               index=dr, name='ac_power', dtype=np.float)

    return fcst_power


def _extend_datetime_index(start, end, deltat, earlier):
    """
    Extends a datetime index to begin prior to ``earlier`` time.

    Parameters
    -------------
    start : datetime
        the start time for the datetime index

    end : datetime
        the end time for the datetime index

    deltat : timedelta
        the time interval for the datetime index

    earlier : datetime
        earlier time to include in the extended datetime index

    Returns
    ------------
    idr : DateTimeIndex
        start replaced by earlier time, time interval and end time maintained

    """

    if earlier > start:
        raise Exception("Error in _extend_datetime_index: earlier > start")
        return

    # number of intervals with length deltat between start of input
    # datetime index and the earlier time to be included
    num_intervals = int(
              (start - earlier).total_seconds() / deltat.seconds)

    # extend datetime index to include earlier time
    idr = pd.DatetimeIndex(start=(start - num_intervals*deltat),
                           end=end,
                           freq=pd.to_timedelta(deltat))

    return idr


def _align_data_to_forecast(fstart, fend, deltat, history):
    """
    Interpolate history to times that are in phase with forecast

    Parameters
    -----------
    fstart : datetime
        first time for the forecast

    fend : datetime
        end time for the forecast

    deltat : timedelta
        interval for the forecast

    history : pandas Series named 'ac_power'
        measurements to use for the forecast

    Returns
    ---------
    idata : pandas DataFrame
        contains history interpolated to times that are in phase with requested
        forecast times

    idr : pandas DatetimeIndex
        datetime index that includes history and forecast periods and is in
        phase with forecast times

    """
    history.name = 'ac_power' # so that we can use pd.Dataframe.merge
    history = history.to_frame()
    idr = _extend_datetime_index(fstart, fend, deltat, min(history.index))

    tmpdata = pd.DataFrame(index=idr, data=np.nan, columns=['ac_power'],
                           dtype=np.float)

    # merge history into empty dataframe that has the index we want
    # use outer join to retain time points in history
    newdata = tmpdata.merge(history,
                            how='outer',
                            on=['ac_power'],
                            left_index=True,
                            right_index=True).tz_convert(tmpdata.index.tz)

    # if history has exact timesteps as idr, the merge above preseves the nan 
    # in tmpdata, so newdata will still have nan where it should have data
    newdata.loc[idr] = history.loc[idr]
    # fill in values on idr timesteps by interpolation
    newdata.interpolate(inplace=True)

    # trim to start at first index in idr (in phase with forecast start),
    # and don't overrun history

    idata = newdata[(newdata.index>=idr[0]) &
                    (newdata.index<=idr[-1]) &
                    (newdata.index<=history.index[-1])].copy()

    # calculates minutes out of phase with midnight
    base = int((idr[0].replace(hour=0, second=0) -
                idr[0].normalize()).total_seconds() / 60)

    # want time averages in phase with forecast start over specified deltat.
    idata = idata.resample(pd.to_timedelta(deltat),
                           closed='left',
                           label='left',
                           base=base).mean()

    return idata, idr


def get_num_intervals(end, start, deltat):
    """
    Calculate number of intervals of length deltat from end working back to
    start, to include start.

    Parameters
    ------------
    end : datetime

    start : datetime

    deltat : timedelta

    """
    return ceil((end - start).total_seconds() / deltat.seconds)


def _get_data_for_ARMA_forecast(start, end, deltat, history,
                                dataWindowLength):

    """
    Select data from history for fitting the forecast model.

    Parameters
    -----------

    start : datetime
        the first time in the forecast

    end : datetime
        the last time in be forecast

    deltat : timedelta
        the time interval for the forecast

    history : pandas Series
        historical values of the quantity to be forecast

    Returns
    ----------
    fitdata : pandas Series
        data from history aligned to be in phase with requested forecast

    f_intervals : integer
        number of time steps in the forecast
    """

    # find number of deltat intervals between start and last time in history
    # assumes that start > max(history.index)
    if start < history.index[-1]:
        # truncate history
        history = history.loc[history.index < start]

    K = get_num_intervals(start, history.index[-1], deltat)

    # find number of deltat intervals covering dataWindowLength in history
    N = get_num_intervals(start - K*deltat,
                          start - K*deltat - dataWindowLength,
                          deltat)

    # start time of resampled history in phase with forecast start
    resample_start = start - (K + N - 1) * deltat
    resample_end = start - K * deltat

    # select aligned data within dataWindowLength
    end_data_time = idata.index[-1]
    first_data_time = end_data_time - dataWindowLength
    fitdata = idata.loc[(idata.index>=first_data_time) &
                        (idata.index<=end_data_time)]

    # determine number of intervals for forecast. start with first interval
    # after the data used to fit the model. +1 because steps counts intervals
    # we want the interval after the last entry in fdr
    f_intervals = len(idr[idr>fitdata.index[-1]]) + 1

    # extract window from resampled history
    return idata.loc[(idata.index>=resample_start) &
                        (idata.index<=resample_end)].copy()


def forecast_ARMA(pvobj, start, end, history, deltat,
                  dataWindowLength=timedelta(hours=1), order=None,
                  start_params=None):

    """
    Generate forecast from start to end with steps deltat
    using an ARMA model fit to data in history.

    Parameters
    -----------

    start : datetime
        the first time to be forecast

    end : datetime
        the last time to be forecast

    deltat : timedelta
        the time step for the forecast

    history : pandas Series
        historical values from which the forecast is made.

    dataWindowLenth : timedelta, default one hour
        time interval for data in history to be considered for model fitting

    dataWindowLenth : timedelta, default one hour

    order : tuple of three integers
        autoregressive, difference, and moving average orders for an ARMA
        forecast model

    start_params : list of float
        initial guess of model parameters, one value for each autoregressive
        and moving average coefficient, followed by the value for the variance
        term
    """

    # TODO: input validation

    fitdata, f_intervals = _get_data_for_ARMA_forecast(start, end,
                                                       deltat, history,
                                                       dataWindowLength)

    # TODO: model identification logic

    # fit model of order (p, d, q)
    # defaults to first order differencing to help with non-stationarity
    if not order:
        if deltat.total_seconds()>=15*60:
            # use MA process for time intervals 15 min or longer
            p = 0
            d = 1
            q = 1
            start_params = [1, 0]
        else:
            # use AR process for time intervals < 15 min
            p = 1
            d = 1
            q = 0
            start_params = [0, 1]
        order = (p, d, q)

    model = sm.tsa.statespace.SARIMAX(fitdata,
                                      trend='n',
                                      order=order)
    # if not provided, generate guess of model parameters, helps overcome
    # non-stationarity

    if not start_params:
        # generate a list with one entry '0' for each AR or MA parameter
        # plus an entry '1' for the variance parameter
        start_params = []
        for i in range(0, order[0]+order[2]):
            start_params.append(0)
        start_params.append(1)

    # generate the ARMA model object

    results = model.fit(start_params=start_params)

    # if not provided, generate guess of model parameters, helps overcome 
    # non-stationarity
    if not start_params:
        # generate a list with one entry '0' for each AR or MA parameter 
        # plus an entry '1' for the variance parameter
        start_params = []
        for i in range(0, order[0]+order[2]):
            start_params.append(0)
        start_params.append(1)

    # generate the ARMA model object
    results = model.fit(start_params=start_params)

    # total intervals to forecast from end of data to end of forecast
    idr = pd.DatetimeIndex(start=fitdata.index[-1],
                           end=end,
                           freq=pd.to_timedelta(deltat))

    f_intervals = len(idr) - 1 # first time in idr is last data point

    # forecast
    f = results.forecast(f_intervals)

    # return the requested forecast times
    f = f[fdr]
    # limit forecast to 0.0 and clear-sky power
    # get clear-sky power at time of year
    cspower = get_clearsky_power(pvobj, fdr)
    f[f > cspower] = cspower
    f[f < 0] = 0.0
    sr, ss = get_sr_ss(pvobj, end)
    f[f.index < sr] = 0.0
    f[f.index > ss] = 0.0

    return f[fdr]
