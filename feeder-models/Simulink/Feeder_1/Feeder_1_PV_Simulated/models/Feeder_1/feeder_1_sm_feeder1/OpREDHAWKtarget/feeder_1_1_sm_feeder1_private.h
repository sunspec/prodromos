/*
 * feeder_1_1_sm_feeder1_private.h
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

#ifndef RTW_HEADER_feeder_1_1_sm_feeder1_private_h_
#define RTW_HEADER_feeder_1_1_sm_feeder1_private_h_
#include "rtwtypes.h"
#include "builtin_typeid_types.h"
#include "multiword_types.h"
#include "zero_crossing_types.h"
#include <math.h>
#include <stdlib.h>
#include "feeder_1_1_sm_feeder1.h"
#define MAX_DELAY_BUFFER_SIZE          32768
#ifndef ssGetFixedStepSize
#define ssGetFixedStepSize(S)          (S).stepSize
#endif                                 /* ssGetFixedStepSize */

extern real_T rt_hypotd_snf(real_T u0, real_T u1);
extern real_T rt_atan2d_snf(real_T u0, real_T u1);
extern real_T rt_modd_snf(real_T u0, real_T u1);
extern real_T rt_powd_snf(real_T u0, real_T u1);
real_T rt_VTDelayfindtDInterpolate(
  real_T x,real_T* tBuf,real_T* uBuf,real_T* xBuf,int_T bufSz,int_T head,int_T
  tail,int_T* pLast,real_T t,real_T tStart,boolean_T discrete,boolean_T
  minorStepAndTAtLastMajorOutput,real_T initOutput,real_T* appliedDelay);
real_T rt_TDelayInterpolate(
  real_T tMinusDelay,                  /* tMinusDelay = currentSimTime - delay */
  real_T tStart,
  real_T *tBuf,
  real_T *uBuf,
  int_T bufSz,
  int_T *lastIdx,
  int_T oldestIdx,
  int_T newIdx,
  real_T initOutput,
  boolean_T discrete,
  boolean_T minorStepAndTAtLastMajorOutput)
  ;
extern real_T look1_binlcpw(real_T u0, const real_T bp0[], const real_T table[],
  uint32_T maxIndex);
extern int32_T div_s32(int32_T numerator, int32_T denominator);
extern void mul_wide_s32(int32_T in0, int32_T in1, uint32_T *ptrOutBitsHi,
  uint32_T *ptrOutBitsLo);
extern int32_T mul_s32_sat(int32_T a, int32_T b);
extern void sfun_discreteVariableDelay(SimStruct *rts);
extern void send_rt(SimStruct *rts);
extern void ssn_sfun_v1(SimStruct *rts);
extern void sfun_tsync_pcie_ctrl(SimStruct *rts);
extern void sfun_recv_async(SimStruct *rts);
extern void opmonitor(SimStruct *rts);
extern void OP_SEND(SimStruct *rts);
extern void sfun_send_async(SimStruct *rts);
extern void sfun_gen_async_ctrl(SimStruct *rts);
extern void sfun_ctrl_ml605ex1(SimStruct *rts);
extern void feeder_1_Subsystempi2delay_Init(B_Subsystempi2delay_feeder_1__T
  *localB, P_Subsystempi2delay_feeder_1__T *localP);
extern void feeder_1_1_sm_Subsystempi2delay(uint8_T rtu_Enable, real_T rtu_dq,
  real_T rtu_dq_a, real_T rtu_wt, B_Subsystempi2delay_feeder_1__T *localB);
extern void feeder_1_1_sm_f_Subsystem1_Init(B_Subsystem1_feeder_1_1_sm_fe_T
  *localB, P_Subsystem1_feeder_1_1_sm_fe_T *localP);
extern void feeder_1_1_sm_feeder_Subsystem1(uint8_T rtu_Enable, real_T rtu_dq,
  real_T rtu_dq_b, real_T rtu_wt, B_Subsystem1_feeder_1_1_sm_fe_T *localB);
extern void feeder_Subsystempi2delay_h_Init(B_Subsystempi2delay_feeder__b_T
  *localB, P_Subsystempi2delay_feeder__d_T *localP);
extern void feede_Subsystempi2delay_Disable(DW_Subsystempi2delay_feeder_c_T
  *localDW);
extern void feeder_1_1__Subsystempi2delay_a(RT_MODEL_feeder_1_1_sm_feeder1_T *
  const feeder_1_1_sm_feeder1_M, uint8_T rtu_Enable, const real_T
  rtu_alpha_beta[2], real_T rtu_wt, B_Subsystempi2delay_feeder__b_T *localB,
  DW_Subsystempi2delay_feeder_c_T *localDW);
extern void feeder_1_1_sm_Subsystem1_k_Init(B_Subsystem1_feeder_1_1_sm__m_T
  *localB, P_Subsystem1_feeder_1_1_sm__b_T *localP);
extern void feeder_1_1_s_Subsystem1_Disable(DW_Subsystem1_feeder_1_1_sm_c_T
  *localDW);
extern void feeder_1_1_sm_feed_Subsystem1_b(RT_MODEL_feeder_1_1_sm_feeder1_T *
  const feeder_1_1_sm_feeder1_M, uint8_T rtu_Enable, const real_T
  rtu_alpha_beta[2], real_T rtu_wt, B_Subsystem1_feeder_1_1_sm__m_T *localB,
  DW_Subsystem1_feeder_1_1_sm_c_T *localDW);
extern void feede_AutomaticGainControl_Init(B_AutomaticGainControl_feeder_T
  *localB, DW_AutomaticGainControl_feede_T *localDW,
  P_AutomaticGainControl_feeder_T *localP, X_AutomaticGainControl_feeder_T
  *localX);
extern void feed_AutomaticGainControl_Start(RT_MODEL_feeder_1_1_sm_feeder1_T *
  const feeder_1_1_sm_feeder1_M, DW_AutomaticGainControl_feede_T *localDW,
  P_AutomaticGainControl_feeder_T *localP);
extern void feed_AutomaticGainControl_Deriv(B_AutomaticGainControl_feeder_T
  *localB, DW_AutomaticGainControl_feede_T *localDW,
  P_AutomaticGainControl_feeder_T *localP, XDot_AutomaticGainControl_fee_T
  *localXdot);
extern void fe_AutomaticGainControl_Disable(DW_AutomaticGainControl_feede_T
  *localDW);
extern void fee_AutomaticGainControl_Update(RT_MODEL_feeder_1_1_sm_feeder1_T *
  const feeder_1_1_sm_feeder1_M, B_AutomaticGainControl_feeder_T *localB,
  DW_AutomaticGainControl_feede_T *localDW, X_AutomaticGainControl_feeder_T
  *localX);
extern void feeder_1_1_AutomaticGainControl(RT_MODEL_feeder_1_1_sm_feeder1_T *
  const feeder_1_1_sm_feeder1_M, real_T rtu_Enable, real_T rtu_Freq, real_T
  rtu_wt, const real_T rtu_Vabc[3], B_AutomaticGainControl_feeder_T *localB,
  DW_AutomaticGainControl_feede_T *localDW, P_AutomaticGainControl_feeder_T
  *localP, X_AutomaticGainControl_feeder_T *localX);
extern void feeder_Subsystempi2delay_b_Init(B_Subsystempi2delay_feeder__k_T
  *localB, P_Subsystempi2delay_feeder__p_T *localP);
extern void fee_Subsystempi2delay_j_Disable(DW_Subsystempi2delay_feeder_g_T
  *localDW);
extern void feeder_1_1__Subsystempi2delay_g(RT_MODEL_feeder_1_1_sm_feeder1_T *
  const feeder_1_1_sm_feeder1_M, uint8_T rtu_Enable, real_T rtu_dq, real_T
  rtu_dq_i, real_T rtu_wt, B_Subsystempi2delay_feeder__k_T *localB,
  DW_Subsystempi2delay_feeder_g_T *localDW);
extern void feeder_1_1_sm_Subsystem1_l_Init(B_Subsystem1_feeder_1_1_sm__p_T
  *localB, P_Subsystem1_feeder_1_1_sm__m_T *localP);
extern void feeder_1_1_Subsystem1_c_Disable(DW_Subsystem1_feeder_1_1_sm_l_T
  *localDW);
extern void feeder_1_1_sm_feed_Subsystem1_h(RT_MODEL_feeder_1_1_sm_feeder1_T *
  const feeder_1_1_sm_feeder1_M, uint8_T rtu_Enable, real_T rtu_dq, real_T
  rtu_dq_o, real_T rtu_wt, B_Subsystem1_feeder_1_1_sm__p_T *localB,
  DW_Subsystem1_feeder_1_1_sm_l_T *localDW);

/* private model entry point functions */
extern void feeder_1_1_sm_feeder1_derivatives(void);

#endif                                 /* RTW_HEADER_feeder_1_1_sm_feeder1_private_h_ */
