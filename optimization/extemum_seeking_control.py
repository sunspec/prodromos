"""
Extremum Seeking Control algorithm for distribution voltage regulation using DER devices

See the following papers for technical details:
* D. B. Arnold, M. Negrete-Pincetic, M. D. Sankur, D. M. Auslander and D. S. Callaway, "Model-Free Optimal Control of
  VAR Resources in Distribution Systems: An Extremum Seeking Approach," IEEE Transactions on Power Systems, vol. 31,
  no. 5, pp. 3583-3593, Sept. 2016.

* J. Johnson, R. Darbali, J. Hernandez-Alvidrez, A. Summers, J. Quiroz, D. Arnold, J. Anandan, "Distribution
  Voltage Regulation using Extremum Seeking Control with Power Hardware-in-the-Loop," IEEE Journal of Photovoltaics,
  vol. 8, no. 6, pp. 1824-1832, 2018.

* J. Johnson, S. Gonzalez, and D.B. Arnold, "Experimental Distribution Circuit Voltage Regulation using DER Power
  Factor, Volt-Var, and Extremum Seeking Control Methods," IEEE PVSC, Washington, DC, 25-30 June, 2017.

* D. B. Arnold, M. D. Sankur, M. Negrete-Pincetic and D. Callaway, "Model-Free Optimal Coordination of Distributed
  Energy Resources for Provisioning Transmission-Level Services," in IEEE Transactions on Power Systems, vol. 33,
  no. 1, pp. 817-828, 2017.

Comments to Jay Johnson, jjohns2@sandia.gov
"""

import sys
import os
import math
import numpy as np
import time
import matplotlib.pyplot as plt


# ES function - gets called every timestep
def es_function(t, T, hpf, lpf, f, c, a_param, Jk, Jkm1, sigmakm1, psikm1, gammakm1, uhatkm1, uhatk_lim=None):
    """
    ES control minimizing a quadratic function
    Dan Arnold, dbarnold@lbl.gov

    inputs:
    t: present time at this timestep
    T: distance between timesteps, delta_T
    hpf: high pass filter gain, usually make this an order of magnitude lower than w
    lpf: low pass filter gain, usually make this equal to hpf, but I usually end up adjusting this quite a bit
    f: ES probing frequency
    c: gain on the integrator - how much to value new measurements compared to old measurements
    a_param: the amplitude of the probing signal
    Jk, Jkm1: values of the objective function (metric we're optimizing) at the present and last timestep
    sigmakm1: output of highpass filter at last timestep
    psikm1: signal after demodulation at last timestep
    gammakm1: output of lowpass filter
    uhatkm1: output of integrator at last timestep

    outputs:
    uk: the control to be applied at the next timestep
    uhatk: the output of the integrator
    gammak: the output of the lowpass filter
    psik: signal after demodulation (mutliplication by cosine)
    sigmak: the output of the washout (highpass) filter
    """

    # calculate angular frequency:
    w = 2*np.pi*f
    # print("J: ", Jk)

    # extract the effect of the probing signal in the objective function
    # do this by passing the signal through a highpass filter
    sigmak = (Jk - Jkm1 - (hpf*T/2-1)*sigmakm1)/(1+hpf*T/2)
    # print("sigma: ", sigmak)

    # the resulting signal is a sinusoid, multiply by a sinusoid of the same frequency
    # this results in a cos**2 term, that has a DC component (we call this demodulation)
    psik = sigmak*np.cos(w*t)
    # print("psi: ", psik)

    # pass the demodulated signal through a lowpass filter, to eliminate noise and "jumpyness"
    gammak = (T*lpf*(psik + psikm1) - (T*lpf - 2)*gammakm1)/(2 + T*lpf)
    # print("gamma: ", gammak)

    # pass the resulting signal through an integrator
    uhatk = uhatkm1 + c*T/2*(gammak + gammakm1)
    if uhatk_lim is not None:
        if uhatk > uhatk_lim:
            uhatk = uhatk_lim
        if uhatk < -uhatk_lim:
            uhatk = -uhatk_lim

    # modulation - add the perturbation to the next control setpoint
    uk = (uhatk + a_param*np.cos(w*t))

    return uk, sigmak, psik, gammak, uhatk


def set_reactive_power(nameplate_va=None, p_lim=None, p_now=None, va_now=None, u=None, pf_lim=None, der_type='SunSpec'):
    """
    Method to find the power factor (PF) to hit a reactive power target, u.  The biggest challenge with generating a
    target reactive power level through the power factor function is that Q = f(PF, P_avail), e.g., reactive power is a
    function of power factor and available power (or irradiance). To further complicate things, the available
    power/irradiance is unknown when the PF setting is curtailing the output power. In that case, this code assumes the
    available power persists (is the same as the last measurement.  To illustrate this, imagine a DER that produces
    nameplate power at 1000 W/m2.  It's solar noon and the DER can produce 100% Prated. We need to absorb 44% Qrated so
    the PF is set to 0.90. During this time, if the irradiance changes anywhere between 1000 W/m2 and 900 W/m2, this
    change is unknown to the management system. So now we need to absorb 44% Qrated. What PF should be issued? This
    code assumes that the last P_avail measurement is the valid and will issue a PF based on 1000 W/m2. If that is no
    longer the case, the code will update the P_avail and re-issue the PF setting on the next iteration. This approach
    seems to be fairly robust and does converge.

    It should be noted that some inverters include a grid-support function that directly sets the reactive
    power level, e.g. IEC 61850-90-7 VV13 and the IEEE 1547-2018 constant reactive power mode, in which cases
    this calculation is performed internal to the DER.

    :param nameplate_va: DER nameplate apparent power
    :param nameplate_p: DER nameplate active power
    :param p_lim: last known active power limit of the DER
    :param p_now: active power output of the DER currently
    :param u: reactive power target from ES algorithm
    :param pf_lim: power factor limits for the DER (it's assumed to be symmetrical, e.g., 0.85 to -0.85)
    :param der_type: 'SunSpec' uses the SunSpec convention for PFs (Q1 = negative, Q4 = positive), any other string
                     reverses the convention

    :returns var_targ: updated reactive power target level
    :returns pf_targ: anticipated PF setpoint to achieve desired reactive power level
    :returns w_targ: active power expected at the PF setpoint
    :returns p_lim: update maximum power from the DER
    """

    var_targ = u
    if p_now > p_lim:  # irradiance has increased
        p_lim = p_now  # set new limit
    else:
        # DER output power is below the last known active power limit. If this new power is on the VA limit of the DER
        # we should not update p_lim because the active power is being limited by the rating of the DER, not the
        # available power. In order to determine if the current operating conditions are on the VA circle of the DER
        # use a 95% threshold.
        if va_now < nameplate_va*0.95:
            # Output power decreasing and DER operating point is not on VA circle in P-Q plane. Update p_lim.
            p_lim = p_now
        else:
            pass  # Below previously known power limit, but on the VA circle, so we can't update p_lim
    # print('p_now = %s, Power limit is %s' % (p_now, p_lim))

    # Now that p_lim has been calculated, determine the PF setpoint
    # Find Q at P-lim and VA circle intersection
    try:
        var_transition = math.sqrt(math.pow(nameplate_va, 2) - math.pow(p_lim, 2))
    except Exception, e:  # p_lim > nameplate_va
        print('Exception. p_lim (%s) > nameplate_va (%s): %s' % (p_lim, nameplate_va, e))
        var_transition = 0

    # Special case: reactive power target is larger than the VA limit of DER
    # Set u (var_targ) to nameplate VA
    if math.fabs(var_targ) > nameplate_va:
        if var_targ < 0:
            var_targ = -nameplate_va
        else:
            var_targ = nameplate_va

    if math.fabs(var_targ) >= var_transition:  # target operating point is on VA circle
        try:
            w_targ = math.sqrt(math.pow(nameplate_va, 2) - math.pow(var_targ, 2))
        except Exception, e:  # var_targ > nameplate_va
            w_targ = 0.001  # never set to 0 PF, because it's poorly defined
            # print('var_targ = %s, nameplate_va = %s' % (var_targ, nameplate_va))
            # print('var_targ > nameplate_va. %s' % e)
        if var_targ > 0:  # sunspec convention
            pf_targ = -w_targ/nameplate_va
        else:
            pf_targ = w_targ/nameplate_va
    else:
        va_on_p_lim = math.sqrt(math.pow(p_lim, 2) + math.pow(var_targ, 2))
        w_targ = p_lim
        if var_targ > 0:  # sunspec convention
            pf_targ = -p_lim/va_on_p_lim
        else:
            pf_targ = p_lim/va_on_p_lim
    # print('var_targ = %s, p_targ = %s, pf_targ = %s' % (var_targ, w_targ, pf_targ))

    # Note: if uhatk_lim is used correctly, these saturation limits will not be used
    if math.fabs(pf_targ) < math.fabs(pf_lim):  # check on PF limits
        # At PF limits
        if pf_targ > 0:
            if der_type == 'SunSpec':
                pf_targ = math.fabs(pf_lim)  # SunSpec convention
            else:
                pf_targ = -1*math.fabs(pf_lim)  # EPRI/OpenDSS/"IEEE" convention
        else:
            if der_type == 'SunSpec':
                pf_targ = -1*math.fabs(pf_lim)  # SunSpec convention
            else:
                pf_targ = math.fabs(pf_lim)  # EPRI/OpenDSS/"IEEE" convention
        print('At PF limits of the DER, using PF = %0.2f' % pf_targ)
    else:
        if pf_targ > 0:
            if der_type == 'SunSpec':
                pf_targ = math.fabs(pf_targ)  # SunSpec convention
            else:
                pf_targ = -1*math.fabs(pf_targ)  # EPRI/OpenDSS/"IEEE" convention
        else:
            if der_type == 'SunSpec':
                pf_targ = -1*math.fabs(pf_targ)  # SunSpec convention
            else:
                pf_targ = math.fabs(pf_targ)  # EPRI/OpenDSS/"IEEE" convention

    return var_targ, pf_targ, w_targ, p_lim


def simple_es_demo(plot=True):
    """
    Line search - the goal of this experiment is to minimize a quadratic function
    the initial value of the controller, u, is the starting position
    we want to drive this value to the minimum of the quadratic, or u=0

    :return: None
    """
    # Simulation

    # Setup time
    T = 0.01  # delta T: the length of each timestep
    time = np.arange(0., 600.)
    time = time*T

    # setup vectors to store past values of the ES control
    J = np.zeros(len(time))  # objective function
    sigma = np.zeros(len(time))  # value after highpass (washout) filter
    psi = np.zeros(len(time))  # value after demodulation
    gamma = np.zeros(len(time))  # value after lowpass filter
    uhat = np.zeros(len(time))  # value after integration
    u = np.zeros(len(time))  # control outputs of ES control (position)

    # initial conditions
    u[0] = 1  # choosing an initial condition - in this case its a position at these many units away from the origin
    J[0] = u[0]**2
    sigma[0] = 1
    psi[0] = 1
    gamma[0] = 1
    uhat[0] = 1

    # setup parameters for the ES controller
    f = 10
    c = -1
    lpf = 1
    hpf = 0.1
    a = 0.01

    print("program running")

    for i in range(0, len(time)):
        if i >= 1:  # don't do anything the first timestep
            # evaluate objective function value
            # minimize a quadratic, minimum value is 0
            J[i] = u[i-1]**2

            # call the ES controller
            uk, sigmak, psik, gammak, uhatk = es_function(time[i], T, hpf, lpf, f, c, a, J[i], J[i-1],
                sigma[i-1], psi[i-1], gamma[i-1], uhat[i-1])

            # store values for next timestep
            u[i] = uk
            sigma[i] = sigmak
            psi[i] = psik
            gamma[i] = gammak
            uhat[i] = uhatk
            # print("----------------------------")

    print("program complete")

    if plot:
        # this is the output of the ES controller
        plt.figure(1)
        plt.plot(time, u)
        plt.title('position')
        # plt.show()

        plt.figure(2)
        plt.plot(time, J, 'r')
        plt.title('objective function value')

        plt.figure(3)
        plt.plot(time, u, 'r', time, uhat, 'g', time, sigma, 'k')
        plt.title('u, u_hat, sigma')

        plt.show()


if __name__ == "__main__":

    # Setup example demonstration for ES Control of DER
    simulation_steps = 60
    n_der = 3  # Number of DER
    n_v_meas_points = 3  # Number of voltage measurement points

    # initial conditions
    sigma = []*n_der  # value after highpass (washout) filter
    psi = []*n_der  # value after demodulation
    gamma = []*n_der  # value after lowpass filter
    uhat = []*n_der  # value after integration
    u = []*n_der  # control outputs of ES control (position)
    pf_history = []*n_der  # history of the
    J = []  # objective function

    var_start = 0  # initial reactive power from DERs
    u.append([var_start]*n_der)
    sigma.append([var_start]*n_der)
    psi.append([var_start]*n_der)
    gamma.append([var_start]*n_der)
    uhat.append([var_start]*n_der)
    pf_history.append([1.]*n_der)
    J.append(0)  # objective function

    # Parameters for the ES controller
    # c: gain on the integrator - how much to value new measurements compared to old measurements
    c = [-258./2., -1.e4/2., -1.e3/2.]  # kW/2
    # a_param: the amplitude of the probing signal (in Var)
    a = [25800., 2.e5, 1.e5]
    # f: probing frequencies for each of the DERs
    f = [10/100., math.sqrt(2)/20., math.sqrt(3)/20., math.sqrt(5)/40.]
    # hpf: high pass filter gain, usually make this an order of magnitude lower than w
    hpf = f[1]/10.
    # lpf: low pass filter gain, usually make this equal to hpf, but I usually end up adjusting this quite a bit
    lpf = f[1]/10.
    # va_lim: nameplate apparent power of the DER
    va_lim = [258.e3, 1.e7, 1.e6]
    # known_p_lim: track the predicted maximum output power of the DER, limited by irradiance
    known_p_lim = [258.e3, 1.e7, 1.e6]  # start at VA limit
    # maximum communication speed of the DERs (in seconds)
    max_comm_rate = 0.2

    # setup time
    time_vector = []
    start_time = time.time()

    # Enter or read the Power Factor limits from the DER devices
    pf_lim = [0.8, 0.85, 0.85]

    # cap the reactive power request at the power factor limit minus the probing signal amplitude.
    # This allows the gradient to still be calculated without saturating the DER.
    uhatk_lim = []
    for i in range(len(pf_lim)):
        u_max_pu = math.sqrt(1 - pf_lim[i]**2)
        uhatk_lim.append(u_max_pu*va_lim[i] - a[i])
    print(uhatk_lim)

    v_nom = 240.  # nominal grid voltage

    print("Entering control loop...")
    for i in range(simulation_steps):
        loop_start_time = time.time()-start_time
        time_vector.append(loop_start_time)

        # Don't do anything the first timestep
        if i >= 1:
            T = time_vector[-1]-time_vector[-2]  # Time step

            # Measure the voltage from DER and/or other power meters
            v_measurement = []
            J.append(0)  # initialize objective function at 0 for this time step
            for j in range(n_v_meas_points):
                v_measurement.append(240.)  # imaginary voltage measurement  ^^^^ Add voltage measurements here!
                # objective function is the summation of the square voltage error
                J[i] += (v_measurement[j]-v_nom)**2

            # ts.log_debug('ES Control for SW inverters')
            uk = [None]*n_der       # u's for step k
            sigmak = [None]*n_der   # sigma's for step k
            psik = [None]*n_der     # sigma's for step k
            gammak = [None]*n_der   # gamma's for step k
            uhatk = [None]*n_der    # uhat's for step k
            var_targ = [0.0]*n_der  # target reactive power for the DERs
            pf_targ = [0.0]*n_der   # power factor to deliver the target reactive power
            w_targ = [0.0]*n_der    # active power that will provide the reactive power target

            for n in range(n_der):
                uk[n], sigmak[n], psik[n], gammak[n], uhatk[n] = \
                    es_function(time_vector[i], T, hpf, lpf, f[n], c[n], a[n], J[i],
                                J[i-1], sigma[i-1][n], psi[i-1][n], gamma[i-1][n], uhat[i-1][n], uhatk_lim[n])

                # Measure/read the power, apparent power, and PF limits of the DERs
                if n == 0:
                    p_now = 258.e3   # ^^^^ Add DER power read command here!
                    va_now = 258.e3  # ^^^^ Add DER VA read command here! (Or read Q and calculate VA)
                elif n == 1:
                    p_now = 1.e7     # ^^^^ Add DER power read command here!
                    va_now = 1.e7    # ^^^^ Add DER VA read command here! (Or read Q and calculate VA)
                else:
                    p_now = 1.e6     # ^^^^ Add DER power read command here!
                    va_now = 1.e6    # ^^^^ Add DER VA read command here! (Or read Q and calculate VA)

                var_targ[n], pf_targ[n], w_targ[n], known_p_lim[n] = \
                    set_reactive_power(nameplate_va=va_lim[n], p_lim=known_p_lim[n], p_now=p_now, va_now=va_now,
                                       u=uk[n], pf_lim=pf_lim[n], der_type='SunSpec')

                # Send the new PF setpoint to the DER ^^^^ Add DER write commands here!
                # pf_targ ---> DERn

            # store values for next timestep
            u.append(uk)   # Note that uk is the same at var_targ
            sigma.append(sigmak)
            psi.append(psik)
            gamma.append(gammak)
            uhat.append(uhatk)
            pf_history.append(pf_targ)

            # Check on the loop time.
            elapsed_time = time.time()-start_time

            print('Time: %0.2f, J_new = %0.3f, Set DER#1 PF = %0.3f (var = %0.3f), '
                  'Set DER#2 PF = %0.3f (var = %0.3f, Set DER#3 PF = %0.3f (var = %0.3f)' %
                  (elapsed_time, J[i], pf_targ[0], var_targ[0], pf_targ[1], var_targ[1], pf_targ[2], var_targ[2]))

            loop_time = elapsed_time - loop_start_time
            if loop_time < max_comm_rate:  # don't exceed 5 Hz update speed (DER limit)
                time.sleep(max_comm_rate-loop_time)

    print("program complete")

    # Transpose data arrays
    u_plot = map(list, zip(*u))
    uhat_plot = map(list, zip(*uhat))
    sigma_plot = map(list, zip(*sigma))
    pf_plot = map(list, zip(*pf_history))

    # this is the output of the ES controller
    fig, ax = plt.subplots()
    ax.plot(time_vector, u_plot[0], 'r', label='u_0')
    ax.plot(time_vector, u_plot[1], 'g', label='u_1')
    ax.plot(time_vector, u_plot[2], 'k', label='u_2')
    legend = ax.legend(loc='upper right', shadow=True, fontsize='x-large')
    plt.title('Reactive Power Set Points to the DER')

    plt.figure(2)
    plt.plot(time_vector, J, 'r')
    plt.title('Objective function value')

    fig, ax = plt.subplots()
    ax.plot(time_vector, u_plot[0], 'r', label='u_0')
    ax.plot(time_vector, uhat_plot[0], 'g', label='uhat_0')
    ax.plot(time_vector, sigma_plot[0], 'k', label='sigma_0')
    legend = ax.legend(loc='upper right', shadow=True, fontsize='x-large')
    plt.title('u, u_hat, sigma for DER 1')

    import pprint
    pprint.pprint(pf_plot)

    fig, ax = plt.subplots()
    ax.plot(time_vector, map(abs, pf_plot[0]), 'r', label='|PF_0|')
    ax.plot(time_vector, map(abs, pf_plot[1]), 'g', label='|PF_1|')
    ax.plot(time_vector, map(abs, pf_plot[2]), 'k', label='|PF_2|')
    legend = ax.legend(loc='upper right', shadow=True, fontsize='x-large')
    plt.title('Power Factor settings for DER')

    plt.show()
