import win32com.client
import numpy as np
import pylab as pyl
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ColorConverter
import matplotlib.text as text
colorConverter = ColorConverter()
import re
import os
from pyswarm import pso
import itertools


# 2018-11-01 : modified by cwhanse@sandia.gov for python 3.5
# 2019-2-19 : code clean up, expanded Load class - jjohns2@sandia.gov

class Load:
    """
    Load object
    """

    def __init__(self, name, phases=1, kW=None, kvar=None, kV=None, status='variable', model=5, Vmaxpu=1.3, Vminpu=0.7,
                 enabled=True, bus1='b_1.1', duty='loadprofile1', p_mult=None, q_mult=None):
        """
        Replicating parameters from OpenDSS Loads, e.g.,
        New "Load.Load138" phases=1 kW=2.670415479 kvar=0.302451287 kV=7.199557857 status=variable
        model=5 Vmaxpu=1.3 Vminpu=0.7 enabled=true bus1=b_11.3 duty=loadprofile138

        :param name: str, name of the load, e.g., "load134"
        :param kW: power
        :param kvar: reactive power
        :param vals: multiplier on the loadshape

        :param p_mult: active power gain on the loadshape
        :param q_mult: reactive power gain on the loadshape

        :param phases: number of phases

        """
        self.name = name
        self.phases = phases
        self.kW = kW
        self.kvar = kvar
        self.kV = kV
        self.status = status
        self.model = model
        self.Vmaxpu = Vmaxpu
        self.Vminpu = Vminpu
        self.enabled = enabled
        self.bus1 = bus1
        self.duty = duty
        self.Pmult = p_mult
        self.Qmult = q_mult
        self.phase = None  # [0] = A, [1] = B, [2] = C, [0, 1, 2] = ABC
        self.determine_load_phases()

    def determine_load_phases(self):
        if self.bus1[-2] != '.':  # three phase case
            self.phase = [0, 1, 2]
        elif self.bus1[-1] == '1':
            self.phase = [0]
        elif self.bus1[-1] == '2':
            self.phase = [1]
        elif self.bus1[-1] == '3':
            self.phase = [2]
        else:
            print('Unknown phasing for load %s. bus1: %s' % (self.name, self.bus1))

        # print('Load %s has phases: %s' % (self.name, self.phase))

    def update_load(self):
        """
        Replaces the beginning of the loadshape for each bus with the values
        in load

        Args:
            bus: str, name of bus (OpenDSS load)
            load: numeric, vector of load multipliers
        """

        # Redacted
        pass

        # engine = win32com.client.Dispatch("OpenDSSEngine.DSS")
        # # engine.Start("0")
        # circuit = engine.ActiveCircuit
        # circuit.Loads.Name = self.name
        #
        # self.kW = circuit.Loads.kW
        # self.kvar = circuit.Loads.kvar
        #
        # profile = circuit.ActiveElement.Properties('duty').val
        # circuit.Loadshapes.Name = profile
        # self.Pmult = np.array(circuit.Loadshapes.Pmult)
        # self.Qmult = np.array(circuit.Loadshapes.Pmult)


class PFOptim:

    def __init__(self, penalty={'violation': 1.0, 'deviation': 1.0, 'power_factor': 0.05},
                       threshold={'violation': 0.05, 'accept': 0.02, 'object': 0.005}, debug=False, swarmsize=20,
                       maxiter=20, minstep=0.001, minfunc=1e-6):
        """
        Parameters
        ----------
        penalty : dict
            penalty values for violation, deviation and power_factor. Default
            values are 1.0, 1.0 and 0.05.
        threshold : dict
            threshold values (per unit) for voltage violation, 
            acceptable voltage deviation, and objective function change.
            Default values are 0.05, 0.02, 0.005
        debug : boolean, default False
            if True prints message at each optimization iteration
        swarmswize : integer, default 20
            number of particles for partile swarm optimization
        maxiter : integer, default 20
            number of iterations in particle swarm optimization
        minstep : float, default 0.001
            minimum step size for each particle position
        minfunc : float, default 1e-6
            minimum function change for particle swarm optimization
        """
        self.penalty = penalty
        self.threshold = threshold
        self.debug = debug
        self.swarmsize = swarmsize
        self.maxiter = maxiter
        self.minstep = minstep
        self.minfunc = minfunc


class DSS(object):
    """
    tshort@epri.com 2008-11-17
    comments: wsunderman@epri.com 2009-10-30
    """

    def __init__(self, filename):
        """
        Inputs:
            filename - string - DSS input file
        Side effects:
            start DSS via COM
        Contains the following DSS COM objects:
            engine
            text
            circuit
        """
        # start an embedded DSS engine through COM
        # note: OpenDSSEngine.dll must already be registered
        self.engine = win32com.client.Dispatch("OpenDSSEngine.DSS")
        self.engine.Start("0")

        self.filename = filename
        # use the Text interface to OpenDSS
        self.text = self.engine.Text
        self.text.Command = "clear"
        self.circuit = self.engine.ActiveCircuit
        self.text.Command = "compile [" + self.filename + "]"
        # self.text.Command = "New EnergyMeter.Feeder Line.L115 1"
        self.text.Command = "solve" # not sure this is needed

        # print(self.engine.Version)

    def solve(self, commands=[]):
        """
        if filename is not empty, then compile the .dss file specified
        note:  filename includes the path and the .dss file name
        note:  the .dss file compiled is usually the master.dss file
        note:  an energymeter should be defined at the head of the circuit
        being modeled
        note:  if compilation is successful we have a circuit instance
        that represents the electric circuit that is being modeled

        :param commands:
        :return:
        """

        # Execute list of commands
        for c in commands:
            self.text.Command = c
        self.text.Command = "solve"
        # self.text.Command = "Buscoords Buscoords.dat"   # load in bus coordinates
        self.populate_results()

    def run(self, power_factors, pvlist, hour, sec, pv_profile, p_profile, q_profile,
                    periods=1, stepsize='15m'):
        """
        Solves the circuit at time hour:sec, using the power factors, pv output and
        load in the input values.
    
        Parameters
        ----------
        power_factors : numeric
            value for power factor (float) for controllable PV systems, in the
            order given by pvlist.
        pvlist : list of str
            name of each PV system in the OpenDSS model
        hour : float
        sec : float
        pv_profile : dict
            key is OpenDSS PV system name, value is sequence of power multipliers
        p_profile : dict
            key is OpenDSS load name, value is sequence of load multipliers
        q_profile : dict
            key is OpenDSS load name, value is sequence of load multipliers
        periods : integer, default 1
            number of time periods to step through
        stepsize : string
            length of a step in minutes, format 'XXm' where XX is an integer
        
        Returns
        -------
        V : list
            len(V) = periods, each entry is a vector of bus voltage
        """
    
        npts = [len(pv_profile[pv])<periods for pv in pvlist]
        if any(npts):
            raise ValueError("number of forecast points is less than number "
                             "of time periods")
    
        # initialize DSS model
        duty_command_string = "set mode=duty number=1 stepsize=" + stepsize
        commands = [duty_command_string,
                    "set controlmode=static",
                    "Reset monitors",
                    "Reset meters",
                    "Reset eventlog",
                    "set hour=0 sec=0"]
        self.solve(commands)
    
        V = []
        # minterval = stepsize.strip('m')
        # set new load values
        for ld in p_profile.keys():
            self.set_load(ld, pmult=p_profile[ld])
        for ld in q_profile.keys():
            self.set_load(ld, qmult=q_profile[ld])
        for (pv, pf) in zip(pvlist, power_factors):
            self.set_pv(pv, pv_profile[pv], pf)

        for ii in range(0, periods):
            self.solve(commands)
            V.append(self.bus_voltage)
        return V

    def _ps_pf_opt(self, pf_angles, **kwargs):
        """
        Objective function for particle swarm optimization of power factors.
        Power factors in angle for continuity at pf=1.0.
        Other inputs must be kwargs for the pso module.
    
        Inputs
        ------
        pf_angles : array of float
            value for angle of power factor for each DER
        Required kwargs:
            pvlist : list of str
                name of each PV system in the OpenDSS model, in the order that
                the power factors are provided
            hour : float
            sec : float
            options : VVar_opt
        kwargs with defaults:
            base : reference voltage, default 1.0 (for p.u. voltages)
        """
        power_factors = angle2pf(pf_angles)
        if not all([kw in kwargs for kw in ['pvlist', 'hour', 'sec',
                                            'pv_profile', 'p_profile', 'q_profile',
                                            'stepsize', 'options']]):
            raise ValueError('kwargs for pf_opt_obj incomplete')
        pvlist = kwargs['pvlist']
        hour = kwargs['hour']
        sec = kwargs['sec']
        pv_profile = kwargs['pv_profile']
        p_profile = kwargs['p_profile']
        q_profile = kwargs['q_profile']
        stepsize = kwargs['stepsize']
        if 'base' in kwargs:
            base_voltage = kwargs['base']
        else:
            base_voltage = 1.0
        if 'periods' in kwargs:
            periods = kwargs['periods']
        else:
            periods = 1
        options = kwargs['options']
    
        alpha = options.threshold['violation']
        penalty = penalty2list(options.penalty)
    
        V = self.run(power_factors, pvlist, hour, sec,
                     pv_profile=pv_profile, p_profile=p_profile, q_profile=q_profile,
                     periods=periods, stepsize=stepsize)
    
        return calc_obj(V, penalty, alpha, base_voltage, power_factors)

    def optimize_pf(self, hour, sec, pvlist, pf_lb, pf_ub, pv_profile,
                    p_profile, q_profile, stepsize, options, periods=1,
                    base_voltage=1.0):
        """
        Returns optimized power factor for each PV system
        """
        # convert lb and ub to angles
        lb = [pf2angle(pf_lb[pv]) for pv in pvlist]
        ub = [pf2angle(pf_ub[pv]) for pv in pvlist]

        # Run particle swarm optimization routine
        xopt, fopt = pso(self._ps_pf_opt, lb, ub, kwargs={'dssobj': self, 'hour': hour, 'sec': sec, 'pvlist': pvlist,
            'pv_profile': pv_profile, 'p_profile': p_profile, 'q_profile': q_profile, 'base': base_voltage,
            'options': options, 'periods': periods, 'stepsize': stepsize}, debug=options.debug,
            swarmsize=options.swarmsize,  maxiter=options.maxiter, minstep=options.minstep, minfunc=options.minfunc)

        pf = angle2pf(xopt)
        return pf, fopt

    def update_power_factors(self, curr_pf, pv_forecast, p_forecast, q_forecast,
                             pvlist, hour, sec, pf_lb, pf_ub, stepsize, numsteps,
                             options, base=1.0):
        """
        Updates power factors.
        
        Args:
            curr_pf: dict
                power factor for each PV system
            pv_forecast: dict
                {pvid, forecast} where forecast is a time series
            p_forecast: dict
                {loadid, forecast} for each bus on the Feeder.
                loadid: str
                forecast: numeric np array
            q_forecast: dict
                {loadid, forecast} for each bus on the Feeder.
                loadid: str
                forecast: numeric np array
            pvlist: list
                derid for PV systems to consider for power factor changes
            hour: int
            sec: int
            base: float
            pf_lb: dict
                lower bound on power factor for each PV system
            pf_ub: dict
                upper bound on power factor for each PV system
            options: VVar_optim
        """
        # first solve for voltage using current settings
        change_pf = False
        power_factors = [curr_pf[pv] for pv in pvlist]
        opt_obj = 'No update'
        # numsteps = len(pv_fc[list(pv_fc.keys())[0]])

        # Calculate a starting value for the objective function. If change is small, don't change PFs.
        V = self.run(power_factors, pvlist, hour, sec,
                     pv_profile=pv_forecast, p_profile=p_forecast, q_profile=q_forecast,
                     periods=numsteps, stepsize=stepsize)
    
        if any([voltage_violation(v, options.threshold['accept'], base) for v in V]):
            print('--- voltage deviation outside target')
            curr_obj = calc_obj(V, penalty2list(options.penalty), 
                                options.threshold['violation'], base,
                                power_factors)
            print('--- current obj value {}'.format(curr_obj))
            # previous settings are not good, find optimal settings
            opt_pf, opt_obj = self.optimize_pf(hour, sec, pvlist, pf_lb, pf_ub,
                                              pv_profile=pv_forecast,
                                              p_profile=p_forecast, q_profile=q_forecast,
                                              periods=numsteps, stepsize=stepsize,
                                              options=options, base_voltage=base)
            opt_pf = {pv: pf for (pv, pf) in zip(pvlist, opt_pf)}
            if options.debug:
                print("--- optimized obj value {}".format(opt_obj))
                print("--- optimized power factors {}.".format(opt_pf))
            if (curr_obj > opt_obj) and (curr_obj - opt_obj) < options.threshold['object']:
                # change pf
                print('--- starting PF {}: obj value {}'.format(curr_pf,
                      curr_obj))
                print('--- change PF to {}: obj value {}'.format(opt_pf,
                      opt_obj))
                power_factors = opt_pf
                change_pf = True
            else:
                print("--- not changing PF, couldn't improve on objective")
        return change_pf, power_factors, opt_obj

    def get_loads(self):
        """
        Return dict {bus, load} where load is of type Load
        """
        loads = {}
        p = self.circuit.Loads.First
        while p > 0:
            name = self.circuit.Loads.Name
            phases = self.circuit.ActiveElement.Properties('phases').val
            kW = self.circuit.Loads.kW
            kvar = self.circuit.Loads.kvar
            kV = self.circuit.Loads.kV

            status = self.circuit.Loads.status
            model = self.circuit.Loads.model
            Vmaxpu = self.circuit.Loads.Vmaxpu
            Vminpu = self.circuit.Loads.Vminpu
            enabled = self.circuit.ActiveElement.Properties('enabled').val
            bus1 = self.circuit.ActiveElement.Properties('bus1').val

            profile = self.circuit.ActiveElement.Properties('duty').val
            self.circuit.Loadshapes.Name = profile
            Pmult = np.array(self.circuit.Loadshapes.Pmult)
            Qmult = np.array(self.circuit.Loadshapes.Qmult)

            # instantiate the Load object with the discovered parameters
            loads[name] = Load(name, phases, kW, kvar, kV, status, model, Vmaxpu, Vminpu, enabled, bus1,
                               duty=profile, p_mult=Pmult, q_mult=Qmult)

            p = self.circuit.Loads.Next  # advance pointer
        return loads

    def _edit_loadshape(self, name, pmult, qmult, pv):
        """ Writes load into a loadshape's Pmult
        """
        self.circuit.Loadshapes.Name = name
        try:
            Pmult = np.array(self.circuit.Loadshapes.Pmult)
        except AttributeError:
            print('Could not find Pmult for %s' % name)
        try:
            Qmult = np.array(self.circuit.Loadshapes.Qmult)
        except AttributeError:
            print('Could not find Qmult for %s' % name)
        try:
            mult = np.array(self.circuit.Loadshapes.Pmult)
        except AttributeError:
            print('Could not find pv Pmult for %s' % name)

        if pmult is not None:
            K = len(pmult)
            Pmult[0:K] = pmult
            Pmult = [float(p) for p in Pmult]
            self.circuit.Loadshapes.Pmult = tuple(Pmult)
        if qmult is not None:
            K = len(qmult)
            Qmult[0:K] = qmult
            Qmult = [float(q) for q in Qmult]
            self.circuit.Loadshapes.Qmult = tuple(Qmult)
        if pv is not None:
            K = len(pv)
            mult[0:K] = pv
            mult = [float(q) for q in mult]
            self.circuit.Loadshapes.Pmult = tuple(mult)

    def set_load(self, bus, pmult=None, qmult=None, pv=None):
        """
        Replaces the beginning of the loadshape for each bus with the values
        in load

        Args:
            bus: str, name of bus (OpenDSS load)
            load: numeric, vector of load multipliers
        """
        self.circuit.Loads.Name = bus
        profile = self.circuit.ActiveElement.Properties('duty').val
        self._edit_loadshape(profile, pmult, qmult, pv)

    def set_pv(self, name, val, pf):
        """
        Sets power profile values and power factor for a PV system

        Args:
            val: numeric, power profile values
            pf: float, power factor
        """
        self.circuit.setActiveElement(name)
        # set power factor
        self.circuit.ActiveElement.Properties('PF').val = pf
        # set power profile values
        profile = self.circuit.ActiveElement.Properties('duty').val
        self._edit_loadshape(profile, pmult=None, qmult=None, pv=val)

    def populate_results(self):
        """
        Method gets the bus and branch names of the DSS 'circuit' instance
        also populates the branch currents and bus voltages
        :return:
        """
        self.bus = Bus(self.circuit)
        self.branch = Branch(self.circuit)
        self.bus_voltage = np.array(self.circuit.AllBusVmagPu)
        # extract power factors for each PV system
        pf_result = {}
        pvlist = self.circuit.PVSystems.AllNames
        for pv in pvlist:
            self.text.Command = '? PVSystem.' + pv + '.pf'
            pf_result[pv] = self.text.result
        self.pf_result = pf_result

    def plots(self):
        """
        Method plots the voltages and map in separate windows and shows them

        :return: None
        """
        self.plot_voltage()
        self.plot_map()
        pyl.show()

    def print_branch_info(self, event):
        """
        Method displays (prints) line name, number of phases,
        voltages in actual volts and volts on a 120V basis,
        displays currents, and calculates real power, reactive
        power, and pf (displacement)
        in a text window

        :param event:
        :return: None
        """
        ind = event.ind[0]
        print(" ")
        print("line: ", self.branch.name[ind])
        print("number of phases: ", self.branch.nphases[ind])
        print("voltages: ", np.around(abs(self.branch.Vto[ind]), 1))
        print("voltages (120-V base): ", np.around(abs(self.branch.Vto[ind]) /
                         self.branch.kvbase[ind] * 120 / 1000, 1))

        print("currents: ", np.around(abs(self.branch.I[ind])))
        S = self.branch.V[ind] * self.branch.I[ind].conj()
        print("kilowatts: ", np.around(S.real / 1000))
        print("kilovars: ", np.around(S.imag / 1000))
        print("pf: ", np.around(S.real / abs(S), 2))

        print(" ")


    def plot_voltage(self):
        """
        Method does the plotting of the voltages on a 120V base versus distance
        x = distance
        y = voltage (120V base)

        :return: None
        """
        fig = pyl.figure()
        def t(x): return x.transpose()

        # scale factor gets us to 120V from the kvbase which is set in the .dss file
        scalefactor = 1 / self.branch.kvbase * 120 / 1000

        x = self.branch.distance
        y = t(t(abs(self.branch.Vto)) * scalefactor)
        pyl.plot(x, y, '*', markersize=5, picker=5)

        # the following code will scale the size dot by the number of phases
        # it's nice, but it makes the code slow
        # size = (self.branch.nphases + 1) ** 2
        # scatter(self.branch.distance, abs(self.branch.Vto[:,0]), s = size, c = 'r', picker=5)
        # scatter(self.branch.distance, abs(self.branch.Vto[:,1]), s = size, c = 'g', picker=5)
        # scatter(self.branch.distance, abs(self.branch.Vto[:,2]), s = size, c = 'b', picker=5)

        # setup the pick events to highlight the voltage plot, circuit map,
        # and to display the branch info in the text box
        # note:  a pick event is usually a mouse click within a certain radius
        # of the actual points on the plots
        # note:  all three methods get called on any pick event
        pyl.connect('pick_event', self.highlight_voltage_plot)
        pyl.connect('pick_event', self.highlight_map)
        pyl.connect('pick_event', self.print_branch_info)

        self.fig = fig
        self.selected, = pyl.plot(x[0:3], y[0], 'o', ms=12, alpha=0.7,
            color='yellow', visible=False)

        ax = fig.add_subplot(111)
        ax.set_xticklabels([])
        ax.set_xlabel('distance')
        ax.set_ylabel('Voltage (120V base)')
        ax.set_title('Primary Voltages by phase')
        for o in fig.findobj(text.Text):
            o.set_fontsize(18)

        # set the limits (x and y) of the plot to contain all of the points
        pyl.xlim(x[x > 0].min(), x.max())
        pyl.ylim(y[y > 0].min(), y.max())


    def highlight_voltage_plot(self, event):
        """
        Method highlights the voltage plot based on
        The x and y coordinates of the pick event (mouse click)

        :param event:
        :return:
        """
        pyl.axis = event.artist.get_axes()
        ind = event.ind[0]
        x = self.branch.distance[ind].repeat(3)
        y = abs(self.branch.Vto[ind]) / self.branch.kvbase[ind] * 120 / 1000
        self.selected.set_visible(True)
        self.selected.set_data(x, y)
        self.fig.canvas.draw()


    def plot_map(self):
        """
        Method does the plotting of the map of the circuit
        note:  master file should have the following text in it
        Buscoords buscoords.dss, where buscoords.dss contains the x and y
        coordinates for each bus to be plotted
        :return:
        """
        fig = pyl.figure()

        # get x and y coordinates of the branch to be drawn
        # the branch is a line so it is defined with pairs of
        # from and to coordinates
        x1 = self.branch.x
        y1 = self.branch.y
        x2 = self.branch.xto
        y2 = self.branch.yto
        pyl.axes().set_aspect('equal', 'datalim')

        # don't want to see any ticks on the x-axis or the y-axis
        pyl.xticks([])
        pyl.yticks([])

        # set the limits of the map plot
        pyl.xlim(x1.min(), x1.max())
        pyl.ylim(y1.min(), y1.max())

        # take the from x and y coordinates and the to x and y coordinates
        # and put them together (zip) as a python sequence object
        segments = [ ( (thisx1, thisy1), (thisx2, thisy2) )  for thisx1,
                    thisy1, thisx2, thisy2 in zip(x1,y1,x2,y2)]

        # make a LineCollection of the segments, with width indicating the number
        # of phases
        line_segments = LineCollection(segments,
                                       linewidths    = self.branch.nphases*1.5,
                                       linestyle = 'solid', picker = 5)
        pyl.gca().add_collection(line_segments)

        # setup the pick events to highlight the voltage plot, circuit map,
        # and to display the branch info in the text box
        # note:  a pick event is usually a mouse click within a certain radius
        # of the actual points on the plots
        pyl.connect('pick_event', self.highlight_voltage_plot)
        pyl.connect('pick_event', self.highlight_map)
        pyl.connect('pick_event', self.print_branch_info)
        self.mapfig = fig

        # plot a yellow circle at the 'to' bus of the line segment if clicked on with
        # the mouse
        self.mapselected,  = pyl.plot([x2[0]], [y2[0]], 'o', ms=12, alpha=0.4,
                                      color='yellow', visible=False)

    def highlight_map(self, event):
        """
        Method highlights the map plot based on
        the x and y coordinates of the pick event (mouse click)
        :param event:
        :return:
        """
        axis = event.artist.get_axes()
        ind = event.ind[0]
        x = self.branch.x[ind]
        y = self.branch.y[ind]
        xto = self.branch.xto[ind]
        yto = self.branch.yto[ind]
        self.mapselected.set_visible(True)
        self.mapselected.set_data(xto,yto)
        self.mapfig.canvas.draw()


class Bus:
    """
    Bus class uses the circuit instance from the DSS COM object
    and gets the names, bus voltages, distances from the energy meter,
    x and y coordinates of the 'from' bus and puts them into numpy arrays
    """

    def __init__(self, circuit):
        """
        Inputs:
            circuit - DSS COM object
        Contains:
            name - string - bus name
            V - complex array (n x 3) - node bus voltage
            distance - array (n) - distance from the energymeter
            x - array (n) - from-bus x location
            y - array (n) - from-bus y location
        """

        # n is set to the number of buses in the circuit
        n = circuit.NumBuses

        # make the x,y, distance, and voltage numpy arrays of length n and set
        # the vslues to all zeros
        # note:  the voltage array is an array of complex values
        x = np.zeros(n)
        y = np.zeros(n)
        distance = np.zeros(n)
        V = np.zeros((n, 3), dtype=complex)
        name = np.array("                                ").repeat(n)

        # populate the arrays by looking at the each bus in turn from 0 to n
        # note:  by convention all arrays are zero-based in python
        for i in range(0, n):
            bus = circuit.Buses(i)
            name[i] = bus.Name
            x[i] = bus.x
            y[i] = bus.y
            distance[i] = bus.Distance
            v = np.array(bus.Voltages)
            nodes = np.array(bus.Nodes)

            # we're only interested in the first three nodes
            # (also called terminals) on the bus
            if nodes.size > 3:
                nodes = nodes[0:3]
            cidx = 2 * np.array(range(0, min(v.size // 2, 3)))
            V[i, nodes-1] = v[cidx] + 1j * v[cidx + 1]
        self.name = name
        self.V = V
        self.x = x
        self.y = y
        self.distance = distance


class Branch:
    """
    Branch class contains the branch object details
    """

    def __init__(self, circuit):
        """
        Inputs:
            circuit - DSS COM object
        Contains:
            name - string - branch name
            busname - string (n) - from-node bus name
            busnameto - string (n) - to-node bus name
            V - complex array (n x 3) - from-node bus voltage
            Vto - complex array (n x 3) - to-node bus voltage
            I - complex array (n x 3) - branch currents
            nphases - array (n) - number of phases
            distance - array (n) - distance from the energy meter
            x - array (n) - from-bus x location
            y - array (n) - from-bus y location
            xto - array (n) - to-bus x location
            yto - array (n) - to-bus y location
        """
        n = circuit.NumCktElements
        name = np.array("                      ").repeat(n)
        busname = np.array("                      ").repeat(n)
        busnameto = np.array("                      ").repeat(n)
        x = np.zeros(n)
        y = np.zeros(n)
        xto = np.zeros(n)
        yto = np.zeros(n)
        distance = np.zeros(n)
        nphases = np.zeros(n)
        kvbase = np.zeros(n)
        I = np.zeros((n, 3), dtype=complex)
        V = np.zeros((n, 3), dtype=complex)
        Vto = np.zeros((n, 3), dtype=complex)
        i = 0
        for j in range(0, n):
            el = circuit.CktElements(j)
            if not re.search("^Line", el.Name):
                continue  # only pick lines...
            name[i] = el.Name
            bus2 = circuit.Buses(re.sub(r"\..*","", el.BusNames[-1]))
            busnameto[i] = bus2.Name
            xto[i] = bus2.x
            yto[i] = bus2.y
            if bus2.x == 0 or bus2.y == 0: continue # skip lines without proper bus coordinates
            distance[i] = bus2.Distance
            v = np.array(bus2.Voltages)
            nodes = np.array(bus2.Nodes)
            kvbase[i] = bus2.kVBase
            nphases[i] = nodes.size
            if nodes.size > 3: nodes = nodes[0:3]
            cidx = 2 * np.array(range(0, min(v.size // 2, 3)))

            bus1 = circuit.Buses(re.sub(r"\..*","", el.BusNames[0]))

            if bus1.x == 0 or bus1.y == 0:
                continue  # skip lines without proper bus coordinates

            busname[i] = bus1.Name

            Vto[i, nodes-1] = v[cidx] + 1j * v[cidx + 1]
            x[i] = bus1.x
            y[i] = bus1.y
            v = np.array(bus1.Voltages)
            V[i, nodes-1] = v[cidx] + 1j * v[cidx + 1]
            current = np.array(el.Currents)
            I[i, nodes-1] = current[cidx] + 1j * current[cidx + 1]
            i = i + 1
        self.name = name[0:i]
        self.busname = busname[0:i]
        self.busnameto = busnameto[0:i]
        self.nphases = nphases[0:i]
        self.kvbase = kvbase[0:i]
        self.x = x[0:i]
        self.y = y[0:i]
        self.xto = xto[0:i]
        self.yto = yto[0:i]
        self.distance = distance[0:i]

        self.V = V[0:i]
        self.Vto = Vto[0:i]
        self.I = I[0:i]


def voltage_violation(V, threshold, base=1.0):
    """
    Returns any(V/base - 1.0) > threshold
    """
    return np.any(np.abs(V / base - 1.0) >= threshold)


def voltage_objective(V, threshold, penalty, base=1.0):
    """
    Returns RMSE(V/base - 1.0) + penalty * voltage_violation
    """
    vv = voltage_violation(V, threshold, base)
    return np.sqrt(np.mean(V/base - 1.0)**2.0) + vv * penalty


def pf2scalar(pf):
    """
    Scales power factor to [-2.0, 0.0], where pf=1.0 -> -1.0 and pf=0.9 -> -1.1
    """
    return np.where(pf < 0, pf, -2.0 + pf)


def scalar2pf(scalar):
    """
    Recovers power factor from scaled values
    """
    return np.where(scalar > -1.0, scalar, 2.0 + scalar)


def pf2angle(pf):
    return np.where(pf >= 0, np.arccos(pf), -1.0 * np.arccos(-pf))


def angle2pf(angle):
    return np.where(angle >= 0, np.cos(angle), -1.0 * np.cos(-angle))


def penalty2list(penalty):
    return [penalty['violation'], penalty['deviation'],
            penalty['power_factor']]


def calc_obj(V, P, alpha, base_voltage, power_factors):
    """
    Calculates objective function for volt-var optimization
    
    Parameters
    ----------
    V: list
        bus voltage, one item for each time point
    P: list or array
        penalty values for voltage violation, voltage deviation, and
        power factor deviation from 1.0
    alpha: float
        level (per unit) for voltage violation
    base_voltage: scalar
        value to normalize voltage to 1.0
    power_factors: numeric
        value of power factor for each PV system
        
    Returns value of objective function (float)
    """

    objval = 0.0
    for v in V:
        objval += P[0] * voltage_violation(v, alpha, base_voltage) + \
        P[1] * np.std(v / base_voltage - 1.0) + \
        P[2] * np.sum(1.0 - np.abs(power_factors))
    return objval


def map_response(d, pvlist, hour, sec, base, threshold_violation,
                 penalty, pf_lb, pf_ub, numint):
    """
    Searches space of power factors and returns objective function values
    """
    # make space of power_factors
    angle_ub = pf2angle(pf_ub)
    angle_lb = pf2angle(pf_lb)
    s = []
    for i in range(len(angle_lb)):
        s.append(list(np.linspace(angle_lb[i], angle_ub[i], numint)))
    angles = list(itertools.product(*s))
    res = np.zeros((len(angles), len(angle_lb)+1))
    ptr = 0
    # solve for objective function values
    for a in angles:
        pf = angle2pf(np.array(a))
        objval = pf_opt_obj(pf, dssobj=d, pvlist=pvlist, hour=hour, sec=sec,
                            penalty=penalty, base=base,
                            threshold_violation=threshold_violation)

        res[ptr, 0:len(angle_lb)] = pf
        res[ptr, len(angle_lb)] = objval
        ptr += 1
        print('{}: pf = {}  objval = {}'.format(ptr, pf, objval))
    return res


