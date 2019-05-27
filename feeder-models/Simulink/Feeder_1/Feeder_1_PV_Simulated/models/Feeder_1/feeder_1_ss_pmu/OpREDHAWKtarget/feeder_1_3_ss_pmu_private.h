/*
 * feeder_1_3_ss_pmu_private.h
 *
 * Code generation for model "feeder_1_3_ss_pmu".
 *
 * Model version              : 1.623
 * Simulink Coder version : 9.0 (R2018b) 24-May-2018
 * C source code generated on : Fri May 17 13:27:24 2019
 *
 * Target selection: rtlab_rtmodel.tlc
 * Note: GRT includes extra infrastructure and instrumentation for prototyping
 * Embedded hardware selection: 32-bit Generic
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#ifndef RTW_HEADER_feeder_1_3_ss_pmu_private_h_
#define RTW_HEADER_feeder_1_3_ss_pmu_private_h_
#include "rtwtypes.h"
#include "builtin_typeid_types.h"
#include "multiword_types.h"
#include "zero_crossing_types.h"

extern real_T rt_hypotd_snf(real_T u0, real_T u1);
extern real_T rt_atan2d_snf(real_T u0, real_T u1);
extern void sfun_discreteVariableDelay(SimStruct *rts);
extern void recv_rt(SimStruct *rts);
extern void sfun_c37_118_sampler(SimStruct *rts);
extern void sfun_send_async(SimStruct *rts);
extern void sfun_gen_async_ctrl(SimStruct *rts);
extern void opwritefile(SimStruct *rts);

#endif                                 /* RTW_HEADER_feeder_1_3_ss_pmu_private_h_ */
