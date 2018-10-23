#from generic_vpp_server import GenericVPPServer
#from multiprocessing import Manager

import pvlib
import pytz
from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class PVobj():
    # create an instance of a PV class object
    def __init__(self, derid, lat, lon, alt, tz,
                 tilt, azimuth, dc_capacity, ac_capacity,
                 forecast_method='persistence', surrogateid=None):

        self.derid = derid
        # TODO: using a surrogate in forecasting is NOT implemented
        self.surrogateid = surrogateid
        if forecast_method.lower() in ['arma', 'persistence']:
            self.forecast_method = forecast_method.lower()
        else:
            # TODO: raise error
            warnstring = 'DER ID ' + str(derid) + \
               ' : no forecast method specified, default to persistence'
            raise RuntimeWarning(warnstring)
            self.forecast_method = None
        self.dc_capacity = dc_capacity
        self.ac_capacity = ac_capacity
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.timezone = tz
        self.tilt = tilt
        self.azimuth = azimuth


    # PVobj member functions
    def forecast(self,
                 start,
                 end,
                 history,
                 deltat=timedelta(minutes=15),
                 dataWindowLength=timedelta(hours=1),
                 order=(1, 1, 0)):

        # wrapper for functions forecast_ARMA and forecast_persistence

        if self.forecast_method=='arma':
            return forecast_ARMA(self,
                                 start,
                                 end,
                                 history,
                                 deltat,
                                 dataWindowLength,
                                 order)

        elif self.forecast_method=='persistence':
            return forecast_persistence(self,
                                        start,
                                        end,
                                        history,
                                        deltat,
                                        dataWindowLength)


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

# block of code copied here pending pvlib v0.6.1

NS_PER_HR = 1.e9 * 3600.  # nanoseconds per hour

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
    clearSky : pandas Dataframe
        contains ghi, dhi, dni, poa, aoi, extraI, beam, diffuseSky,
        diffuseGround, diffuseTotal
    """

    # initialize clear sky df and fill with information
    clearSky = pd.DataFrame(index=pd.DatetimeIndex(dr))
    # get solar position information
    sp = solar_position(pvobj, dr)
    clearSky['zenith'] = sp['zenith']
    clearSky['elevation'] = sp['elevation']

    clearSky['extraI'] = pvlib.irradiance.get_extra_radiation(dr)

    # calculate GHI using Haurwitz model
    clearSky['ghi'] = pvlib.clearsky.haurwitz(sp['apparent_zenith'])

    clearSky['dni'] = dniDiscIrrad(clearSky)

    clearSky['dhi'] = DHIfromGHI(clearSky)

    clearSky['aoi'] = pvlib.irradiance.aoi(surface_tilt=pvobj.tilt,
                                           surface_azimuth=pvobj.azimuth,
                                           solar_zenith=sp['zenith'],
                                           solar_azimuth=sp['azimuth'])

    # Convert the AOI to radians
    clearSky['aoi'] *= (np.pi/180.0)

    # Calculate the POA irradiance based on the given site information
    clearSky['beam'] = pvlib.irradiance.beam_component(pvobj.tilt,
                                                       pvobj.azimuth,
                                                       sp['zenith'],
                                                       sp['azimuth'],
                                                       clearSky['dni'])

    # Calculate the diffuse radiation from the sky (using Hay and Davies)
    clearSky['diffuseSky'] = pvlib.irradiance.haydavies(pvobj.tilt,
                                                        pvobj.azimuth,
                                                        clearSky['dhi'],
                                                        clearSky['dni'],
                                                        clearSky['extraI'],
                                                        sp['zenith'],
                                                        sp['azimuth'])

    # Calculate the diffuse radiation from the ground in the plane of array
    clearSky['diffuseGround'] = pvlib.irradiance.get_ground_diffuse(pvobj.tilt,
                                                              clearSky['ghi'])

    # Sum the two diffuse to get total diffuse
    clearSky['diffuseTotal'] = clearSky['diffuseGround'] + \
                                 clearSky['diffuseSky']

    # Sum the diffuse and beam to get the total POA irradicance
    clearSky['poa'] = clearSky['diffuseTotal'] + clearSky['beam']

    return clearSky


def calc_clear_index(meas, ub):
    # calculates clear-sky index of meas relative to ub
    # accepts input as pd.Series or np.ndarray
    # returns the same type as the inputs
    clearIndex = calc_ratio(meas, ub)
    clearIndex[clearIndex == np.inf] = 1.0
    clearIndex[np.isnan(clearIndex)] = 1.0
    clearIndex[clearIndex > 1.0] = 1.0

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

    history : pandas DataFrame with key 'ac_power'
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
    end_data_time = min([max(history.index), start])
    # select data within dataWindowLength
    fitdata = history.loc[(history.index>=end_data_time - dataWindowLength) &
                         (history.index<=end_data_time)]

    return fitdata


def is_leap_year(year):
    """Determine whether a year is a leap year."""

    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def get_clearsky_power(pvobj, dr):
    # calculates clearsky AC power for pvobj at times in dr    


    clearsky = clear_sky_model(pvobj, dr)
    clearsky = clearsky[['ghi', 'poa']]

    # model DC power from POA irradiance
    clearsky['dc_power'] = clearsky['poa'] / 1000 * pvobj.dc_capacity

    # model AC power from DC power, with clipping
    clearsky['ac_power'] = np.where(clearsky['dc_power']>pvobj.ac_capacity,
                                    pvobj.ac_capacity,
                                    clearsky['dc_power']
                                    )
    
    return clearsky


def forecast_persistence(pvobj, start, end, history, deltat,
                         dataWindowLength=timedelta(hours=1)):

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

    Returns
    --------

    """
    # time index for forecast
    dr = pd.DatetimeIndex(start=start, end=end, freq=deltat)

    # for sunrise and sunset calculation, time must be in timezone for location
    local_end = end.astimezone(pvobj.timezone)
    doy = pd.Timestamp(local_end).dayofyear
    declination = pvlib.solarposition.declination_spencer71(doy)
    eot = pvlib.solarposition.equation_of_time_spencer71(doy)
    sr, ss, tr = sun_rise_set_transit_geometric(local_end,
                                                                  pvobj.lat,
                                                                  pvobj.lon,
                                                                  declination,
                                                                  eot)

    # length of time for after-sunrise forecast
    delta_fc = dataWindowLength + timedelta(minutes=30)

    if end<sr:
        # forecast period is before sunrise
        fcst_power = pd.Series(data=0.0, index=dr, name='ac_power')
    elif start < sr + delta_fc:
        # forecast period is too near sunrise for history to have valid data
        # get yesterday's data +/- deltat on either side of forecast window
        # so we can interpolate to forecast points
        fcst_power = _align_data_to_forecast(start - timedelta(days=1),
                                             end - timedelta(days=1),
                                             deltat, history)
    else:
        # get data for forecast
        fitdata = _get_data_for_persistence(start, history, dataWindowLength)
    
        # get clear-sky power at time of year
        cspower = get_clearsky_power(pvobj, fitdata.index)
        
        # compute average clear sky power index
        cspower_index = calc_ratio(fitdata, cspower['ac_power'])
    
        fcst_cspower = get_clearsky_power(pvobj, dr)
    
        # forecast ac_power_index using persistence of clear sky power index
        fcst_power = pd.Series(data=fcst_cspower['ac_power'] * cspower_index.mean(),
                               index=dr,
                               name='ac_power')

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

    history : pandas Series or DataFrame containing key 'ac_power'
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

    idr = _extend_datetime_index(fstart, fend, deltat, min(history.index))

    tmpdata = pd.DataFrame(index=idr, data=np.nan, columns=['ac_power'])

    # merge history into empty dataframe that has the index we want
    # use outer join to retain time points in history
    newdata = tmpdata.merge(history.to_frame(),
                            how='outer',
                            on=['ac_power'],
                            left_index=True,
                            right_index=True).tz_convert(tmpdata.index.tz)

    # fill in values on idr timesteps by interpolation
    newdata.interpolate(inplace=True)

    # trim to start at first index in idr (in phase with forecast start),
    # and don't overrun history
    idata = newdata[(newdata.index>=min(idr)) &
                    (newdata.index<=max(history.index))].copy()

    # calculates minutes out of phase with midnight
    base = int((idr[0].replace(hour=0, second=0) -
                idr[0].normalize()).total_seconds() / 60)

    # want time averages in phase with forecast start over specified deltat.
    idata = idata.resample(pd.to_timedelta(deltat),
                           closed='left',
                           label='left',
                           base=base).mean()

    return idata, idr


def _get_data_for_ARMA_forecast(start, end, deltat, history,
                                dataWindowLength):

    """
    Returns interpolated history data in phase with forecast start time and
    time interval.

    Parameters
    -----------

    start : datetime
        the time for the first forecast value

    end : datetime
        the last time to be forecast

    deltat : timedelta
        the time interval for the forecast

    history : pandas DataFrame with key 'ac_power'
        historical values of AC power from which the forecast is made.

    dataWindowLenth : timedelta
        time interval in history to be considered

    Returns
    ----------
    fitdata :
        data from history aligned to be in phase with requested forecast

    fdr : pandas DatetimeIndex
        time index for requested forecast

    steps : integer
        number of time steps in the forecast forecast
    """

    # align history data with forecast start time and interval
    idata, idr = _align_data_to_forecast(start, end, deltat, history)

    # select aligned data within dataWindowLength
    end_data_time = max(idata.index)
    first_data_time = end_data_time - dataWindowLength
    fitdata = idata.loc[(idata.index>=first_data_time) &
                        (idata.index<=end_data_time)]

    # determine number of intervals for forecast. start with first interval
    # after the data used to fit the model. +1 because steps counts intervals
    # we want the interval after the last entry in fdr
    f_intervals = len(idr[idr>max(fitdata.index)]) + 1

    return fitdata, f_intervals


def forecast_ARMA(pvobj, start, end, history, deltat,
                  dataWindowLength=timedelta(hours=1), order=None):

    """
    Generate forecast from start to end at time resolution deltat
    using an ARMA model of order fit to AC power data in history.

    Parameters
    -----------

    pvobj : an instance of type PVobj

    start : datetime
        the time for the first forecast value

    end : datetime
        the last time to be forecast

    deltat : timedelta
        the time interval for the forecast

    history : pandas Series
        historical values of AC power from which the forecast is made.

    order : tuple of three integers
        autoregressive, difference, and moving average orders for an ARMA
        forecast model

    dataWindowLenth : timedelta, default one hour

    """

    # TODO: input validation

    fitdata, f_intervals = _get_data_for_ARMA_forecast(pvobj, start, end,
                                                       deltat, history,
                                                       dataWindowLength)

    # TODO: model identification logic

    # fit model of order (p, d, q)
    # defaults:
    if not order:
        if deltat.total_seconds()>=15*60:
            # use MA process for time intervals 15 min or longer
            p = 0
            d = 1
            q = 1
        else:
            # use AR process
            p = 1
            d = 1
            q = 0
        order = (p, d, q)

    model = sm.tsa.statespace.SARIMAX(fitdata,
                                      trend='n',
                                      order=order)
    results = model.fit()

    f = results.forecast(f_intervals)

    # create datetime index for forecast
    fdr = pd.DatetimeIndex(start=start, end=end, freq=pd.to_timedelta(deltat))

    return f[fdr]


if __name__ == "__main__":

    USMtn = pytz.timezone('US/Mountain')
    if pvlib.__version__ < '0.4.1':
        print('pvlib out-of-date, found version ' + pvlib.__version__ +
              ', please upgrade to 0.4.1 or later')
    else:
        # make a dict of PV system objects
        pvdict = {};
        pvdict['sunpower'] = PVobj('sunpower',
                                        dc_capacity=1900,
                                        ac_capacity=3000,
                                        lat=35.05,
                                        lon=-106.54,
                                        alt=1657,
                                        tz=USMtn,
                                        tilt=35,
                                        azimuth=180,
                                        forecast_method='persistence')

        from dateutil import parser
        timestamps = [parser.parse(ts).replace(tzinfo=pytz.UTC).astimezone(USMtn)
                      for ts in ['2018-02-18T16:00:00',
                                 '2018-02-18T16:15:00',
                                 '2018-02-18T16:30:00',
                                 '2018-02-18T16:45:00']]
        values = [300.0, 400.1, 500.2, 600.3]
        history = pd.Series(data=values, index=pd.DatetimeIndex(timestamps))
        start = parser.parse('2018-02-18T17:00:00').replace(tzinfo=pytz.UTC).astimezone(USMtn)
        end = parser.parse('2018-02-18T18:00:00').replace(tzinfo=pytz.UTC).astimezone(USMtn)

        fc = pvdict['sunpower'].forecast(start=start,
                                        end=end,
                                        history=history,
                                        deltat=timedelta(minutes=15),
                                        dataWindowLength=timedelta(hours=1))
        print(fc)

