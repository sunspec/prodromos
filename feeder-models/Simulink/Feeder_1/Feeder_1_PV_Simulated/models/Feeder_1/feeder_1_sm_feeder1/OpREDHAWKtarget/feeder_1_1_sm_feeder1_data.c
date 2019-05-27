/*
 * feeder_1_1_sm_feeder1_data.c
 *
 * Code generation for model "feeder_1_1_sm_feeder1".
 *
 * Model version              : 1.623
 * Simulink Coder version : 9.0 (R2018b) 24-May-2018
 * C source code generated on : Fri May 17 13:25:57 2019
 *
 * Target selection: rtlab_rtmodel.tlc
 * Note: GRT includes extra infrastructure and instrumentation for prototyping
 * Embedded hardware selection: 32-bit Generic
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#include "feeder_1_1_sm_feeder1.h"
#include "feeder_1_1_sm_feeder1_private.h"

/* Block parameters (default storage) */
P_feeder_1_1_sm_feeder1_T feeder_1_1_sm_feeder1_P = {
  0.0001,
  2.0,
  2.0,
  2.0,
  2.0,
  2.0,
  2.0,
  2.0,
  2.0,
  2.0,
  2.0,
  2.0,
  2.0,
  2.0,
  2.0,
  0.0,
  0.0,
  0.0,
  0.0,
  0.0,
  0.0,
  0.0,
  0.0,
  0.0,
  60.0,
  60.0,
  60.0,
  60.0,
  60.0,
  60.0,
  60.0,
  60.0,
  60.0,
  60.0,
  60.0,
  60.0,
  60.0,
  60.0,
  60.0,
  60.0,
  20.0,
  20.0,
  30.0,
  20.0,
  20.0,
  30.0,
  20.0,
  20.0,
  30.0,
  376.99111843077515,
  376.99111843077515,
  376.99111843077515,
  376.99111843077515,
  376.99111843077515,
  0.0,
  0.0,
  0.0,
  0.0,
  0.0,
  0.0,
  0.0,
  0.0,
  0.0,
  0.0,
  0.0,
  0.0,
  0.0,
  0.0,
  0.0,
  0.0,
  0.0,
  0.0,
  1.0,
  1.0,
  1.0,
  3200.0,
  3200.0,
  3200.0,
  1400.0,
  1400.0,
  180.0,
  180.0,
  180.0,
  60.0,
  60.0,
  100.0,
  100.0,
  100.0,
  100.0,
  100.0,
  100.0,
  100.0,
  100.0,
  100.0,
  2.0,
  2.0,
  10.0,
  2.0,
  2.0,
  10.0,
  2.0,
  2.0,
  10.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  0.0001,
  0.0001,
  0.0001,
  0.0001,
  0.0001,
  0.0001,
  0.0,
  0.0,
  60.0,
  60.0,
  1.0,
  2.0,
  1.0,
  2.0,
  1.0,
  2.0,
  1.0,
  2.0,
  1.0,
  2.0,
  1.0,
  2.0,
  1.0,
  2.0,
  1.0,
  2.0,
  1.0,
  2.0,
  1.0,
  2.0,
  1.0,
  2.0,
  1.0,
  2.0,
  1.0,
  2.0,
  1.0,
  2.0,
  0.5,
  0.5,
  0.5,
  1.0,
  2.0,
  1.2836049168437711,
  1.3,

  { 1.08702E+6, 1.05894E+6, 916380.0, 919620.0, 986580.0, 981720.0, 882360.0,
    884520.0, 921240.0, 957420.0, 1.03032E+6, 865620.0, 1.21878E+6, 1.2717E+6,
    1.1367E+6, 1.00548E+6, 1.06056E+6, 1.3203E+6, 1.18314E+6, 1.2096E+6,
    1.21662E+6, 1.09512E+6, 1.1313E+6, 1.14426E+6, 983880.0 },

  { 0.0, 900.0, 1800.0, 2700.0, 3600.0, 4500.0, 5400.0, 6300.0, 7200.0, 8100.0,
    9000.0, 9900.0, 10800.0, 11700.0, 12600.0, 13500.0, 14400.0, 15300.0,
    16200.0, 17100.0, 18000.0, 18900.0, 19800.0, 20700.0, 21600.0 },

  { 1.22796E+6, 1.21932E+6, 1.24254E+6, 1.2987E+6, 1.27224E+6, 1.20798E+6,
    1.34028E+6, 1.3392E+6, 1.37322E+6, 1.36944E+6, 1.35054E+6, 1.37862E+6,
    1.2906E+6, 1.24362E+6, 1.31976E+6, 1.4823E+6, 1.48878E+6, 1.36944E+6,
    1.36836E+6, 1.32732E+6, 1.35E+6, 1.37376E+6, 1.4148E+6, 1.3662E+6,
    1.45422E+6 },

  { 0.0, 900.0, 1800.0, 2700.0, 3600.0, 4500.0, 5400.0, 6300.0, 7200.0, 8100.0,
    9000.0, 9900.0, 10800.0, 11700.0, 12600.0, 13500.0, 14400.0, 15300.0,
    16200.0, 17100.0, 18000.0, 18900.0, 19800.0, 20700.0, 21600.0 },
  0.5,
  0.5,
  0.5,
  1.0,
  2.0,
  1.2836049168437711,
  1.3,

  { 27504.0, 38160.0, 37080.0, 38688.0, 37896.0, 39456.0, 37152.0, 39624.0,
    38760.0, 39336.0, 39792.0, 42792.0, 40824.0, 41016.0, 39432.0, 41808.0,
    45912.0, 41400.0, 40680.0, 48456.0, 41904.0, 42480.0, 39288.0, 44448.0,
    42672.0 },

  { 0.0, 900.0, 1800.0, 2700.0, 3600.0, 4500.0, 5400.0, 6300.0, 7200.0, 8100.0,
    9000.0, 9900.0, 10800.0, 11700.0, 12600.0, 13500.0, 14400.0, 15300.0,
    16200.0, 17100.0, 18000.0, 18900.0, 19800.0, 20700.0, 21600.0 },

  { 16800.0, 23952.0, 18336.0, 19872.0, 19056.0, 19056.0, 17760.0, 17088.0,
    17712.0, 18768.0, 17136.0, 17616.0, 17712.0, 17328.0, 15936.0, 16896.0,
    18912.0, 17616.0, 16752.0, 22320.0, 17472.0, 16800.0, 16032.0, 18576.0,
    17664.0 },

  { 0.0, 900.0, 1800.0, 2700.0, 3600.0, 4500.0, 5400.0, 6300.0, 7200.0, 8100.0,
    9000.0, 9900.0, 10800.0, 11700.0, 12600.0, 13500.0, 14400.0, 15300.0,
    16200.0, 17100.0, 18000.0, 18900.0, 19800.0, 20700.0, 21600.0 },
  0.0003333333333333523,
  -0.0016666666666667045,
  0.0003333333333333523,
  -0.0016666666666667045,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  -0.037690182669934541,
  0.9992894726405892,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  169.70562748477141,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  0.9992894726405892,
  0.037690182669934694,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  0.0,
  57.295779513082323,
  0.70710678118654746,
  -0.0016666666666667045,
  0.0003333333333333523,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  0.0,
  60.0,
  14400.0,
  0.0,
  0.0,
  0.0003333333333333523,
  -0.0016666666666667045,
  0.0003333333333333523,
  -0.0016666666666667045,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  -0.037690182669934541,
  0.9992894726405892,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  169.70562748477141,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  0.9992894726405892,
  0.037690182669934694,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  0.0,
  57.295779513082323,
  0.70710678118654746,
  -0.0016666666666667045,
  0.0003333333333333523,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  0.0,
  60.0,
  14400.0,
  0.0,
  0.0,
  0.0003333333333333523,
  -0.0016666666666667045,
  0.0003333333333333523,
  -0.0016666666666667045,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  -0.037690182669934541,
  0.9992894726405892,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  169.70562748477141,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  0.9992894726405892,
  0.037690182669934694,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  0.0,
  57.295779513082323,
  0.70710678118654746,
  -0.0016666666666667045,
  0.0003333333333333523,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  0.0,
  60.0,
  14400.0,
  0.0,
  0.0,
  0.0003333333333333523,
  -0.0016666666666667045,
  0.0003333333333333523,
  -0.0016666666666667045,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  -0.037690182669934541,
  0.9992894726405892,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  169.70562748477141,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  0.9992894726405892,
  0.037690182669934694,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  0.0,
  57.295779513082323,
  0.70710678118654746,
  -0.0016666666666667045,
  0.0003333333333333523,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  0.0,
  60.0,
  14400.0,
  0.0,
  0.0,
  0.0003333333333333523,
  -0.0016666666666667045,
  0.0003333333333333523,
  -0.0016666666666667045,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  -0.037690182669934541,
  0.9992894726405892,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  169.70562748477141,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  0.9992894726405892,
  0.037690182669934694,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  0.0,
  57.295779513082323,
  0.70710678118654746,
  -0.0016666666666667045,
  0.0003333333333333523,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  0.0,
  60.0,
  14400.0,
  0.0,
  0.0,
  0.0003333333333333523,
  -0.0016666666666667045,
  0.0003333333333333523,
  -0.0016666666666667045,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  -0.037690182669934541,
  0.9992894726405892,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  169.70562748477141,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  0.9992894726405892,
  0.037690182669934694,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  0.0,
  57.295779513082323,
  0.70710678118654746,
  -0.0016666666666667045,
  0.0003333333333333523,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  0.0,
  60.0,
  14400.0,
  0.0,
  0.0,
  0.0003333333333333523,
  -0.0016666666666667045,
  0.0003333333333333523,
  -0.0016666666666667045,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  -0.037690182669934541,
  0.9992894726405892,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  169.70562748477141,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  0.9992894726405892,
  0.037690182669934694,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  0.0,
  57.295779513082323,
  0.70710678118654746,
  -0.0016666666666667045,
  0.0003333333333333523,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  0.0,
  60.0,
  14400.0,
  0.0,
  0.0,
  0.0003333333333333523,
  -0.0016666666666667045,
  0.0003333333333333523,
  -0.0016666666666667045,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  -0.037690182669934541,
  0.9992894726405892,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  169.70562748477141,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  0.9992894726405892,
  0.037690182669934694,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  0.0,
  57.295779513082323,
  0.70710678118654746,
  -0.0016666666666667045,
  0.0003333333333333523,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  0.0,
  60.0,
  14400.0,
  0.0,
  0.0,
  0.0003333333333333523,
  -0.0016666666666667045,
  0.0003333333333333523,
  -0.0016666666666667045,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  -0.037690182669934541,
  0.9992894726405892,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  678.82250993908565,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  0.9992894726405892,
  0.037690182669934694,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  0.0,
  57.295779513082323,
  0.70710678118654746,
  -0.0016666666666667045,
  0.0003333333333333523,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  0.0,
  60.0,
  230400.0,
  0.0,
  0.0,
  0.0003333333333333523,
  -0.0016666666666667045,
  0.0003333333333333523,
  -0.0016666666666667045,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  -0.037690182669934541,
  0.9992894726405892,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  169.70562748477141,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  0.9992894726405892,
  0.037690182669934694,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  0.0,
  57.295779513082323,
  0.70710678118654746,
  -0.0016666666666667045,
  0.0003333333333333523,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  0.0,
  60.0,
  14400.0,
  0.0,
  0.0,
  0.0003333333333333523,
  -0.0016666666666667045,
  0.0003333333333333523,
  -0.0016666666666667045,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  -0.037690182669934541,
  0.9992894726405892,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  169.70562748477141,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  0.9992894726405892,
  0.037690182669934694,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  0.0,
  57.295779513082323,
  0.70710678118654746,
  -0.0016666666666667045,
  0.0003333333333333523,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  0.0,
  60.0,
  14400.0,
  0.0,
  0.0,
  0.0003333333333333523,
  -0.0016666666666667045,
  0.0003333333333333523,
  -0.0016666666666667045,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  -0.037690182669934541,
  0.9992894726405892,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  169.70562748477141,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  0.9992894726405892,
  0.037690182669934694,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  0.0,
  57.295779513082323,
  0.70710678118654746,
  -0.0016666666666667045,
  0.0003333333333333523,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  0.0,
  60.0,
  14400.0,
  0.0,
  0.0,
  0.0003333333333333523,
  -0.0016666666666667045,
  0.0003333333333333523,
  -0.0016666666666667045,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  -0.037690182669934541,
  0.9992894726405892,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  169.70562748477141,
  2.0,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  0.9992894726405892,
  0.037690182669934694,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  60.0,
  0.0,
  0.0,
  57.295779513082323,
  0.70710678118654746,
  -0.0016666666666667045,
  0.0003333333333333523,
  5.0E-5,
  0.0,
  0.0167,

  { 1.0, 1.0 },
  0.0169,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  0.0,
  60.0,
  14400.0,
  0.0,
  0.0,

  { 1.0, 1.0 },
  3.0,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  0.0001,
  0.0,
  0.0,
  0.0001,
  0.0,
  6.2831853071795862,

  { 1.0, -0.5, -0.5, 0.0, 0.8660254037844386, -0.8660254037844386, 1.0, 1.0, 1.0
  },
  0.0001,
  0.0,
  6.2831853071795862,

  { 1.0, -0.5, -0.5, 0.0, 0.8660254037844386, -0.8660254037844386, 1.0, 1.0, 1.0
  },
  0.0,
  0.0,
  0.0,
  93906.496517369174,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  -0.037690182669934541,
  0.9992894726405892,
  93906.496517369174,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  -0.84656497770613792,
  -0.53228539198573366,
  93906.496517369174,
  0.0,
  0.037690182669934541,
  0.9992894726405892,
  0.88425516037607244,
  -0.46700408065485521,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  0.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  5.0,

  { 1.0, 1.0 },
  1.0,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  2.0,
  1000.0,
  1000.0,

  { 1.0, 1.0 },
  1.0,

  { 1.0, 1.0 },
  1.0,

  { 1.0, 1.0 },
  1.0,

  { 1.0, 1.0 },
  2.0,

  { 1.0, 1.0 },
  3.0,

  { 1.0, 1.0 },
  4.0,

  { 1.0, 1.0 },
  5.0,

  { 1.0, 7.0 },

  { 115.0, 116.0, 114.0, 105.0, 110.0, 103.0, 49.0 },

  { 1.0, 7.0 },

  { 115.0, 116.0, 114.0, 105.0, 110.0, 103.0, 50.0 },

  { 1.0, 7.0 },

  { 115.0, 116.0, 114.0, 105.0, 110.0, 103.0, 51.0 },

  { 1.0, 7.0 },

  { 115.0, 116.0, 114.0, 105.0, 110.0, 103.0, 52.0 },

  { 1.0, 7.0 },

  { 115.0, 116.0, 114.0, 105.0, 110.0, 103.0, 53.0 },
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  0.57735026918962584,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  0.57735026918962584,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  1.0,
  0.57735026918962584,
  1.0,
  1.0,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 32.0 },

  { 109.0, 121.0, 95.0, 101.0, 118.0, 101.0, 110.0, 116.0, 95.0, 110.0, 97.0,
    109.0, 101.0, 44.0, 97.0, 110.0, 111.0, 116.0, 104.0, 101.0, 114.0, 95.0,
    101.0, 118.0, 101.0, 110.0, 116.0, 95.0, 110.0, 97.0, 109.0, 101.0 },
  60.0,
  60.0,
  60.0,

  { 1.0, 1.0 },
  1.0,
  1.0,
  10000.0,
  1.0,
  0.0,

  { 1.0, 1.0 },
  1.0,

  { 1.0, 1.0 },
  1.0,

  { 1.0, 1.0 },
  3.0,

  { 1.0, 1.0 },
  1.0,

  { 1.0, 1.0 },
  2.0,

  { 1.0, 1.0 },
  3.0,

  { 1.0, 1.0 },
  4.0,

  { 1.0, 1.0 },
  5.0,

  { 1.0, 7.0 },

  { 115.0, 116.0, 114.0, 105.0, 110.0, 103.0, 49.0 },

  { 1.0, 7.0 },

  { 115.0, 116.0, 114.0, 105.0, 110.0, 103.0, 50.0 },

  { 1.0, 7.0 },

  { 115.0, 116.0, 114.0, 105.0, 110.0, 103.0, 51.0 },

  { 1.0, 7.0 },

  { 115.0, 116.0, 114.0, 105.0, 110.0, 103.0, 52.0 },

  { 1.0, 7.0 },

  { 115.0, 116.0, 114.0, 105.0, 110.0, 103.0, 53.0 },

  { 1.0, 1.0 },
  1.0,

  { 1.0, 1.0 },
  12.0,

  { 1.0, 1.0 },
  7.0,

  { 1.0, 1.0 },
  6.0,

  { 1.0, 1.0 },
  7.0,

  { 1.0, 1.0 },
  2.0,

  { 1.0, 1.0 },
  1.0,

  { 1.0, 1.0 },
  6340.0,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,

  { 1.0, 1.0 },
  1.0,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 4.0 },

  { 101.0, 116.0, 104.0, 48.0 },

  { 1.0, 8.0 },

  { 49.0, 48.0, 46.0, 49.0, 46.0, 50.0, 46.0, 50.0 },

  { 0.0, 0.0 },

  { 0.0, 0.0 },

  { 0.0, 0.0 },

  { 0.0, 0.0 },

  { 0.0, 0.0 },

  { 0.0, 0.0 },

  { 0.0, 0.0 },

  { 0.0, 0.0 },

  { 0.0, 0.0 },

  { 0.0, 0.0 },

  { 1.0, 13.0 },

  { 65.0, 115.0, 121.0, 110.0, 99.0, 69.0, 116.0, 104.0, 101.0, 114.0, 110.0,
    101.0, 116.0 },

  { 1.0, 1.0 },
  0.0,
  6.2831853071795862,
  0.0,
  0.0,
  0.0,
  3.1415926535897931,
  1.0,
  0.0,
  0.0,
  0.022222222222222445,
  0.0,
  0.0,
  0.016666666666666666,
  0.0,
  -10000.0,
  -1.0E+8,
  10000.0,
  0.0,
  0.0,
  0.15915494309189535,
  12.0,
  -12.0,
  0.0024317084074161068,
  0.0,
  0.0,
  1.0,
  -24674.011002723397,
  -222.11060060879836,
  0.0,
  1.0,
  24674.011002723397,
  0.0,
  0.0,
  1.0E+6,
  2.2204460492503131E-16,

  { 1.0, 0.0, 0.5, -0.5, 0.8660254037844386, 0.5, -0.5, -0.8660254037844386, 0.5
  },
  0.66666666666666663,
  6.2831853071795862,
  0.0,
  0.0,
  0.0,
  3.1415926535897931,
  1.0,
  0.0,
  0.0,
  0.022222222222222445,
  0.0,
  0.0,
  0.016666666666666666,
  0.0,
  -10000.0,
  -1.0E+8,
  10000.0,
  0.0,
  0.0,
  0.15915494309189535,
  12.0,
  -12.0,
  0.0024317084074161068,
  0.0,
  0.0,
  1.0,
  -24674.011002723397,
  -222.11060060879836,
  0.0,
  1.0,
  24674.011002723397,
  0.0,
  0.0,
  1.0E+6,
  2.2204460492503131E-16,

  { 1.0, 0.0, 0.5, -0.5, 0.8660254037844386, 0.5, -0.5, -0.8660254037844386, 0.5
  },
  0.66666666666666663,
  6.2831853071795862,
  0.0,
  0.0,
  0.0,
  3.1415926535897931,
  1.0,
  0.0,
  0.0,
  0.022222222222222445,
  0.0,
  0.0,
  0.016666666666666666,
  0.0,
  -10000.0,
  -1.0E+8,
  10000.0,
  0.0,
  0.0,
  0.15915494309189535,
  12.0,
  -12.0,
  0.0024317084074161068,
  0.0,
  0.0,
  1.0,
  -24674.011002723397,
  -222.11060060879836,
  0.0,
  1.0,
  24674.011002723397,
  0.0,
  0.0,
  1.0E+6,
  2.2204460492503131E-16,

  { 1.0, 0.0, 0.5, -0.5, 0.8660254037844386, 0.5, -0.5, -0.8660254037844386, 0.5
  },
  0.66666666666666663,
  3.8759689922480621E-6,
  0.0025515518153991436,

  { 1.0, 0.0, 0.5, -0.5, 0.8660254037844386, 0.5, -0.5, -0.8660254037844386, 0.5
  },
  0.66666666666666663,
  0.0,
  1.0,
  0.1,
  0.0022785951095657467,

  { 1.0, 0.0, 0.5, -0.5, 0.8660254037844386, 0.5, -0.5, -0.8660254037844386, 0.5
  },
  0.66666666666666663,
  3.8759689922480621E-6,
  -1.0,
  0.79997711680551331,
  0.79997711680551331,
  0.0,

  { 1.0, -0.5, -0.5, 0.0, 0.8660254037844386, -0.8660254037844386, 1.0, 1.0, 1.0
  },
  391.91835884530855,
  376.99111843077515,
  0.15915494309189535,
  1.0E-7,
  9.8215306446799435E-5,

  { 1.0, 0.0, 0.5, -0.5, 0.8660254037844386, 0.5, -0.5, -0.8660254037844386, 0.5
  },
  0.66666666666666663,
  0.0,
  1.0,
  0.1,
  0.0015272568546253113,

  { 1.0, 0.0, 0.5, -0.5, 0.8660254037844386, 0.5, -0.5, -0.8660254037844386, 0.5
  },
  0.66666666666666663,
  1.0E-7,
  -1.0,
  0.080004082987401234,
  0.080004082987401234,
  0.0,

  { 1.0, -0.5, -0.5, 0.0, 0.8660254037844386, -0.8660254037844386, 1.0, 1.0, 1.0
  },
  10181.712364168745,
  376.99111843077515,
  0.15915494309189535,
  1.0E-7,
  9.8215306446799435E-5,

  { 1.0, 0.0, 0.5, -0.5, 0.8660254037844386, 0.5, -0.5, -0.8660254037844386, 0.5
  },
  0.66666666666666663,
  0.0,
  1.0,
  0.1,
  0.0015272568546253113,

  { 1.0, 0.0, 0.5, -0.5, 0.8660254037844386, 0.5, -0.5, -0.8660254037844386, 0.5
  },
  0.66666666666666663,
  1.0E-7,
  -1.0,
  0.80004082987401237,
  0.80004082987401237,
  0.0,

  { 1.0, -0.5, -0.5, 0.0, 0.8660254037844386, -0.8660254037844386, 1.0, 1.0, 1.0
  },
  10181.712364168745,
  376.99111843077515,
  0.15915494309189535,
  1.0,
  1.0,
  1.0,
  1.0,
  0.0001,
  471.23889803846896,
  282.74333882308133,
  2.5515518153991436E-6,
  5.0E-5,
  0.0,
  60.0,
  1.0E+6,
  1.0E-6,
  0.0,
  0.0,
  1.0,
  0.5,
  471.23889803846896,
  282.74333882308133,
  0.15915494309189535,
  0.001,
  -0.001,

  { 0.977912228775521, -2.4401514047614183, 9.8895611438776042E-5,
    0.99987799242976183 },

  { 0.98895611438776054, 4.9447805719388021E-5 },

  { 0.0001220075702380709, 2.4672505794658162 },
  6.100378511903545E-5,

  { 0.0, 24.317084074161063 },
  0.016666666666666666,
  1.0E+6,
  2.2204460492503131E-16,
  0.0,
  5.0E-5,
  0.0,

  { 1.0, 1.0 },
  0.022322222222222222,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  1.0,
  0.016666666666666666,
  1.0E+6,
  2.2204460492503131E-16,
  0.0,
  5.0E-5,
  0.0,

  { 1.0, 1.0 },
  0.022322222222222222,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  0.0,
  1.0,
  0.7,
  10000.0,
  1.0,
  0.7,
  3000.0,
  1.0,
  0.5,
  587877.53826796263,
  0.0001,
  471.23889803846896,
  282.74333882308133,
  2.5515518153991436E-6,
  5.0E-5,
  0.0,
  60.0,
  1.0E+6,
  1.0E-6,
  0.0,
  0.0,
  1.0,
  0.5,
  471.23889803846896,
  282.74333882308133,
  0.15915494309189535,
  0.001,
  -0.001,

  { 0.977912228775521, -2.4401514047614183, 9.8895611438776042E-5,
    0.99987799242976183 },

  { 0.98895611438776054, 4.9447805719388021E-5 },

  { 0.0001220075702380709, 2.4672505794658162 },
  6.100378511903545E-5,

  { 0.0, 24.317084074161063 },
  0.016666666666666666,
  1.0E+6,
  2.2204460492503131E-16,
  0.0,
  5.0E-5,
  0.0,

  { 1.0, 1.0 },
  0.022322222222222222,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  1.0,
  0.016666666666666666,
  1.0E+6,
  2.2204460492503131E-16,
  0.0,
  5.0E-5,
  0.0,

  { 1.0, 1.0 },
  0.022322222222222222,

  { 1.0, 1.0 },
  0.0001,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,
  0.0,
  1.0,
  0.7,
  10000.0,
  1.0,
  0.7,
  3000.0,
  1.0,
  0.5,
  587877.53826796263,

  { 1.0, 13.0 },

  { 77.0, 76.0, 54.0, 48.0, 53.0, 69.0, 88.0, 49.0, 32.0, 67.0, 116.0, 114.0,
    108.0 },

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  1.0,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  0.0,

  { 1.0, 1.0 },
  -1.0,

  { 1.0, 1.0 },
  -1.0,

  { 0.017010345435994296, -0.0051031036307982881 },

  { 0.017010345435994296, -0.0051031036307982881 },

  /* Start of '<S1438>/Subsystem1' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S1438>/Subsystem1' */

  /* Start of '<S1438>/Subsystem - pi//2 delay' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S1438>/Subsystem - pi//2 delay' */

  /* Start of '<S1432>/Subsystem1' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S1432>/Subsystem1' */

  /* Start of '<S1432>/Subsystem - pi//2 delay' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S1432>/Subsystem - pi//2 delay' */

  /* Start of '<S1328>/Subsystem1' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S1328>/Subsystem1' */

  /* Start of '<S1328>/Subsystem - pi//2 delay' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S1328>/Subsystem - pi//2 delay' */

  /* Start of '<S1103>/Subsystem1' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S1103>/Subsystem1' */

  /* Start of '<S1103>/Subsystem - pi//2 delay' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S1103>/Subsystem - pi//2 delay' */

  /* Start of '<S1097>/Subsystem1' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S1097>/Subsystem1' */

  /* Start of '<S1097>/Subsystem - pi//2 delay' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S1097>/Subsystem - pi//2 delay' */

  /* Start of '<S993>/Subsystem1' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S993>/Subsystem1' */

  /* Start of '<S993>/Subsystem - pi//2 delay' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S993>/Subsystem - pi//2 delay' */

  /* Start of '<S768>/Subsystem1' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S768>/Subsystem1' */

  /* Start of '<S768>/Subsystem - pi//2 delay' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S768>/Subsystem - pi//2 delay' */

  /* Start of '<S762>/Subsystem1' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S762>/Subsystem1' */

  /* Start of '<S762>/Subsystem - pi//2 delay' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S762>/Subsystem - pi//2 delay' */

  /* Start of '<S658>/Subsystem1' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S658>/Subsystem1' */

  /* Start of '<S658>/Subsystem - pi//2 delay' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S658>/Subsystem - pi//2 delay' */

  /* Start of '<S452>/Subsystem1' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S452>/Subsystem1' */

  /* Start of '<S452>/Subsystem - pi//2 delay' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S452>/Subsystem - pi//2 delay' */

  /* Start of '<S429>/Automatic Gain Control' */
  {
    2.0,
    1.0,
    2.0,
    1.0,
    0.022222222222222445,
    0.0,
    0.0,
    0.016666666666666666,
    1.0,
    0.022222222222222445,
    0.0,
    0.0,
    0.016666666666666666,
    0.0,
    0.0,
    2.2204460492503131E-16,
    1.0E+6,
    2.2204460492503131E-16,
    1.0E+6,
    2.2204460492503131E-16,
    57.295779513082323,

    { 1.0, 0.0, 0.5, -0.5, 0.8660254037844386, 0.5, -0.5, -0.8660254037844386,
      0.5 },
    0.66666666666666663,

    /* Start of '<S383>/Subsystem1' */
    {
      { 0.0, 0.0 }
    }
    ,

    /* End of '<S383>/Subsystem1' */

    /* Start of '<S383>/Subsystem - pi//2 delay' */
    {
      { 0.0, 0.0 }
    }
    /* End of '<S383>/Subsystem - pi//2 delay' */
  }
  ,

  /* End of '<S429>/Automatic Gain Control' */

  /* Start of '<S423>/Subsystem1' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S423>/Subsystem1' */

  /* Start of '<S423>/Subsystem - pi//2 delay' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S423>/Subsystem - pi//2 delay' */

  /* Start of '<S400>/Automatic Gain Control' */
  {
    2.0,
    1.0,
    2.0,
    1.0,
    0.022222222222222445,
    0.0,
    0.0,
    0.016666666666666666,
    1.0,
    0.022222222222222445,
    0.0,
    0.0,
    0.016666666666666666,
    0.0,
    0.0,
    2.2204460492503131E-16,
    1.0E+6,
    2.2204460492503131E-16,
    1.0E+6,
    2.2204460492503131E-16,
    57.295779513082323,

    { 1.0, 0.0, 0.5, -0.5, 0.8660254037844386, 0.5, -0.5, -0.8660254037844386,
      0.5 },
    0.66666666666666663,

    /* Start of '<S383>/Subsystem1' */
    {
      { 0.0, 0.0 }
    }
    ,

    /* End of '<S383>/Subsystem1' */

    /* Start of '<S383>/Subsystem - pi//2 delay' */
    {
      { 0.0, 0.0 }
    }
    /* End of '<S383>/Subsystem - pi//2 delay' */
  }
  ,

  /* End of '<S400>/Automatic Gain Control' */

  /* Start of '<S394>/Subsystem1' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S394>/Subsystem1' */

  /* Start of '<S394>/Subsystem - pi//2 delay' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S394>/Subsystem - pi//2 delay' */

  /* Start of '<S371>/Automatic Gain Control' */
  {
    2.0,
    1.0,
    2.0,
    1.0,
    0.022222222222222445,
    0.0,
    0.0,
    0.016666666666666666,
    1.0,
    0.022222222222222445,
    0.0,
    0.0,
    0.016666666666666666,
    0.0,
    0.0,
    2.2204460492503131E-16,
    1.0E+6,
    2.2204460492503131E-16,
    1.0E+6,
    2.2204460492503131E-16,
    57.295779513082323,

    { 1.0, 0.0, 0.5, -0.5, 0.8660254037844386, 0.5, -0.5, -0.8660254037844386,
      0.5 },
    0.66666666666666663,

    /* Start of '<S383>/Subsystem1' */
    {
      { 0.0, 0.0 }
    }
    ,

    /* End of '<S383>/Subsystem1' */

    /* Start of '<S383>/Subsystem - pi//2 delay' */
    {
      { 0.0, 0.0 }
    }
    /* End of '<S383>/Subsystem - pi//2 delay' */
  }
  ,

  /* End of '<S371>/Automatic Gain Control' */

  /* Start of '<S109>/Subsystem1' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S109>/Subsystem1' */

  /* Start of '<S109>/Subsystem - pi//2 delay' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S109>/Subsystem - pi//2 delay' */

  /* Start of '<S80>/Subsystem1' */
  {
    { 0.0, 0.0 }
  }
  ,

  /* End of '<S80>/Subsystem1' */

  /* Start of '<S80>/Subsystem - pi//2 delay' */
  {
    { 0.0, 0.0 }
  }
  /* End of '<S80>/Subsystem - pi//2 delay' */
};