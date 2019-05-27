# File    : TARGET.tmf
#
# $Revision 1.1 $
#
# Abstract:
#       Real-Time Workshop template makefile for building a Neutrino-based 
#       stand-alone real-time version of SIMULINK model using 
#       generated C code.
#
#       Note that this template is automatically customized by the Real-Time
#       Workshop build procedure to create "<model>.mk"
#
#       The following defines can be used to modify the behavior of the
#       build:
#         OPTS           - User specific compile options, such as 
#                          OPTS=-DMULTITASKING to enable multitasking mode.
#         OPT_OPTS       - Optimization options. Default is -Oatx. To enable
#                          debugging define DEBUG.
#         USER_SRCS      - Additional user sources, such as files needed by
#                          S-functions.
#         USER_INCS  - Additional include paths 
#                          (i.e. USER_INCS="-Iwhere-ever -Iwhere-ever2")


#------------------------ Macros read by make_rtw -----------------------------
#
# The following macros are read by the Real-Time Workshop build procedure:
#
#  MAKE            - This is the command used to invoke the make utility
#  HOST            - What platform this template makefile is targeted for 
#                    (i.e. PC or UNIX)
#  BUILD           - Invoke make from the Real-Time Workshop build procedure 
#                    (yes/no)?
#  SYS_TARGET_FILE - Name of system target file.

MAKE            = make
HOST            = PC
BUILD           = no
SYS_TARGET_FILE = rtlab_rtmodel.tlc

#---------------------- Tokens expanded by make_rtw ---------------------------
#
# The following tokens, when wrapped with "|>" and "|<" are expanded by the 
# Real-Time Workshop build procedure.
#   
#  MODEL_NAME    - Name of the SIMULINK block diagram
#  MODEL_MODULES - Any additional generated source modules
#  MAKEFILE_NAME - Name of makefile created from template makefile <model>.mk
#  MATLAB_ROOT   - Path to were MATLAB is installed. 
#  S_FUNCTIONS   - List of S-functions.
#  SOLVER        - Solver source file name
#  NUMST         - Number of sample times
#  TID01EQ       - yes (1) or no (0): Are sampling rates of continuous task 
#                  (tid=0) and 1st discrete task equal.
#  NCSTATES      - Number of continuous states
#  MAT_FILE            - yes (1) or no (0): Should mat file logging be done
#  COMPUTER      - Computer type. See the MATLAB computer command.
#  BUILDARGS     - Options passed in at the command line.

MODEL           = feeder_1_3_ss_pmu
MODULES         = rt_matrx.c rt_printf.c rt_logging.c feeder_1_3_ss_pmu_data.c feeder_1_3_ss_pmu_offsets.c rtGetInf.c rtGetNaN.c rt_nonfinite.c
MAKEFILE        = feeder_1_3_ss_pmu.mk
MATLAB_ROOT     = C:\Program Files\MATLAB\R2018b
ALT_MATLAB_ROOT = C:\PROGRA~1\MATLAB\R2018b
S_FUNCTIONS     = opwritefile.c recv_rt.c sfun_c37_118_sampler.c sfun_discreteVariableDelay.c sfun_gen_async_ctrl.c sfun_send_async.c
SOLVER          = 
NUMST           = 1
TID01EQ         = 0
NCSTATES        = 0
COMPUTER        = PCWIN64
BUILDARGS       =  EXT_MODE=0 EXTMODE_STATIC_ALLOC=0 TMW_EXTMODE_TESTING=0 EXTMODE_STATIC_ALLOC_SIZE=1000000 EXTMODE_TRANSPORT=0 INCLUDE_MDL_TERMINATE_FCN=1 ISPROTECTINGMODEL=NOTPROTECTING
MULTITASKING    = 0
MAT_FILE        = 1

CLASSIC_INTERFACE    = 1
# Optional for GRT
ONESTEPFCN           = 0
TERMFCN              = 1
MULTI_INSTANCE_CODE  = 0

MODELREFS                 = 
MODELLIB                  = feeder_1_3_ss_pmulib.lib
MODELREF_LINK_LIBS        = 
MODELREF_LINK_RSPFILE     = feeder_1_3_ss_pmu_ref.rsp
MODELREF_INC_PATH        =  
RELATIVE_PATH_TO_ANCHOR   = ..
MODELREF_TARGET_TYPE      = NONE

SHARED_SRC      = 
SHARED_SRC_DIR  = 
SHARED_BIN_DIR  = 
SHARED_LIB      = 

# SHARED_BIN_DIR = unused
# SHARED_LIB = unused
UNAME = $(shell uname)

ifeq "$(UNAME)" "QNX"		##### nto
	ifeq ($(MODELREF_TARGET_TYPE), NONE)
		SHARED_SRC      		:= _sharedutils\*.c*
		SHARED_SRC_DIR			:= _sharedutils
		RELATIVE_PATH_TO_ANCHOR	:=
		MODELREF_LINK_LIBS 		:= $(MODELREF_LINK_LIBS:.lib=.a)
		MODELLIB 				:= $(MODELLIB:.lib=.a)
		
	else
		SHARED_SRC      		:= ..\_sharedutils\*.c*
		SHARED_SRC_DIR			:= ..\_sharedutils
		RELATIVE_PATH_TO_ANCHOR	:= ..
		MODELREF_LINK_LIBS 		:= $(MODELREF_LINK_LIBS:.lib=.a)
		MODELLIB 				:= $(MODELLIB:.lib=.a)
	endif	
else
	ifeq "$(UNAME)" "Linux"	##### Linux (RedHawk)
		ifeq ($(MODELREF_TARGET_TYPE), NONE)
			SHARED_SRC      		:= _sharedutils\*.c*
			SHARED_SRC_DIR			:= _sharedutils
			RELATIVE_PATH_TO_ANCHOR	:=
			MODELREF_LINK_LIBS 		:= $(MODELREF_LINK_LIBS:.lib=.a)
			MODELLIB 				:= $(MODELLIB:.lib=.a)
		else
			SHARED_SRC      		:= ..\_sharedutils\*.c*
			SHARED_SRC_DIR			:= ..\_sharedutils
			RELATIVE_PATH_TO_ANCHOR	:= ..
			MODELREF_LINK_LIBS 		:= $(MODELREF_LINK_LIBS:.lib=.a)
			MODELLIB 				:= $(MODELLIB:.lib=.a)
		endif		
	else
		ifeq ($(MODELREF_TARGET_TYPE), NONE)
			SHARED_SRC				:= $(SHARED_SRC)
			SHARED_SRC_DIR			:= $(SHARED_SRC_DIR)
			RELATIVE_PATH_TO_ANCHOR	:= $(RELATIVE_PATH_TO_ANCHOR)
			MODELREF_LINK_LIBS		:= $(MODELREF_LINK_LIBS)
			MODELLIB				:= $(MODELLIB)
		else
			SHARED_SRC				:= $(SHARED_SRC)
			SHARED_SRC_DIR			:= $(SHARED_SRC_DIR)
			RELATIVE_PATH_TO_ANCHOR	:= $(RELATIVE_PATH_TO_ANCHOR)
			MODELREF_LINK_LIBS		:= $(MODELREF_LINK_LIBS)
			MODELLIB				:= $(MODELLIB)
		endif
	endif
endif




#----------------------------- Source Files ------------------------------
MOD_TMP1 = $(MODULES:blms_an_wn_cc_rt.c= )
MOD_TMP2 = $(MOD_TMP1:blms_an_wn_dd_rt.c= )
MOD_TMP3 = $(MOD_TMP2:blms_an_wn_rr_rt.c= )
MOD_TMP4 = $(MOD_TMP3:blms_an_wn_zz_rt.c= )
MOD_TMP5 = $(MOD_TMP4:blms_an_wy_cc_rt.c= )
MOD_TMP6 = $(MOD_TMP5:blms_an_wy_dd_rt.c= )
MOD_TMP7 = $(MOD_TMP6:blms_an_wy_rr_rt.c= )
MOD_TMP8 = $(MOD_TMP7:blms_an_wy_zz_rt.c= )
MOD_TMP9 = $(MOD_TMP8:blms_ay_wn_cc_rt.c= )
MOD_TMP10 = $(MOD_TMP9:blms_ay_wn_dd_rt.c= )
MOD_TMP11 = $(MOD_TMP10:blms_ay_wn_rr_rt.c= )
MOD_TMP12 = $(MOD_TMP11:blms_ay_wn_zz_rt.c= )
MOD_TMP13 = $(MOD_TMP12:blms_ay_wy_cc_rt.c= )
MOD_TMP14 = $(MOD_TMP13:blms_ay_wy_dd_rt.c= )
MOD_TMP15 = $(MOD_TMP14:blms_ay_wy_rr_rt.c= )
MOD_TMP16 = $(MOD_TMP15:blms_ay_wy_zz_rt.c= )
MOD_TMP17 = $(MOD_TMP16:is_little_endian_rt.c= )
MOD_TMP18 = $(MOD_TMP17:eph_zc_fcn_rt.c= )
MOD_TMP19 = $(MOD_TMP18:2chabank_fr_df_cc_rt.c= )
MOD_TMP20 = $(MOD_TMP19:2chabank_fr_df_cr_rt.c= )
MOD_TMP21 = $(MOD_TMP20:2chabank_fr_df_dd_rt.c= )
MOD_TMP22 = $(MOD_TMP21:2chabank_fr_df_rr_rt.c= )
MOD_TMP23 = $(MOD_TMP22:2chabank_fr_df_zd_rt.c= )
MOD_TMP24 = $(MOD_TMP23:2chabank_fr_df_zz_rt.c= )
MOD_TMP25 = $(MOD_TMP24:2chsbank_df_cc_rt.c= )
MOD_TMP26 = $(MOD_TMP25:2chsbank_df_cr_rt.c= )
MOD_TMP27 = $(MOD_TMP26:2chsbank_df_dd_rt.c= )
MOD_TMP28 = $(MOD_TMP27:2chsbank_df_rr_rt.c= )
MOD_TMP29 = $(MOD_TMP28:2chsbank_df_zd_rt.c= )
MOD_TMP30 = $(MOD_TMP29:2chsbank_df_zz_rt.c= )
MOD_TMP31 = $(MOD_TMP30:ic_copy_channel_rt.c= )
MOD_TMP32 = $(MOD_TMP31:ic_copy_matrix_rt.c= )
MOD_TMP33 = $(MOD_TMP32:ic_copy_scalar_rt.c= )
MOD_TMP34 = $(MOD_TMP33:ic_copy_vector_rt.c= )
MOD_TMP35 = $(MOD_TMP34:ic_old_copy_fcns_rt.c= )
MOD_TMP36 = $(MOD_TMP35:mmpcmaudio_rt.c= )
MOD_TMP37 = $(MOD_TMP36:mmrgb24convert2gray_rt.c= )
MOD_TMP38 = $(MOD_TMP37:mmrgb24convert_rt.c= )
MOD_TMP39 = $(MOD_TMP38:mmrgb24output_rt.c= )
MOD_TMP40 = $(MOD_TMP39:mmrgb24paddedoutput_rt.c= )
MOD_TMP41 = $(MOD_TMP40:polyval_cc_rt.c= )
MOD_TMP42 = $(MOD_TMP41:polyval_cr_rt.c= )
MOD_TMP43 = $(MOD_TMP42:polyval_dd_rt.c= )
MOD_TMP44 = $(MOD_TMP43:polyval_dz_rt.c= )
MOD_TMP45 = $(MOD_TMP44:polyval_rc_rt.c= )
MOD_TMP46 = $(MOD_TMP45:polyval_rr_rt.c= )
MOD_TMP47 = $(MOD_TMP46:polyval_zd_rt.c= )
MOD_TMP48 = $(MOD_TMP47:polyval_zz_rt.c= )
MOD_TMP49 = $(MOD_TMP48:sort_ins_idx_d_rt.c= )
MOD_TMP50 = $(MOD_TMP49:sort_ins_idx_r_rt.c= )
MOD_TMP51 = $(MOD_TMP50:sort_ins_idx_s08_rt.c= )
MOD_TMP52 = $(MOD_TMP51:sort_ins_idx_s16_rt.c= )
MOD_TMP53 = $(MOD_TMP52:sort_ins_idx_s32_rt.c= )
MOD_TMP54 = $(MOD_TMP53:sort_ins_idx_u08_rt.c= )
MOD_TMP55 = $(MOD_TMP54:sort_ins_idx_u16_rt.c= )
MOD_TMP56 = $(MOD_TMP55:sort_ins_idx_u32_rt.c= )
MOD_TMP57 = $(MOD_TMP56:sort_ins_val_d_rt.c= )
MOD_TMP58 = $(MOD_TMP57:sort_ins_val_r_rt.c= )
MOD_TMP59 = $(MOD_TMP58:sort_ins_val_s08_rt.c= )
MOD_TMP60 = $(MOD_TMP59:sort_ins_val_s16_rt.c= )
MOD_TMP61 = $(MOD_TMP60:sort_ins_val_s32_rt.c= )
MOD_TMP62 = $(MOD_TMP61:sort_ins_val_u08_rt.c= )
MOD_TMP63 = $(MOD_TMP62:sort_ins_val_u16_rt.c= )
MOD_TMP64 = $(MOD_TMP63:sort_ins_val_u32_rt.c= )
MOD_TMP65 = $(MOD_TMP64:sort_qk_idx_d_rt.c= )
MOD_TMP66 = $(MOD_TMP65:sort_qk_idx_r_rt.c= )
MOD_TMP67 = $(MOD_TMP66:sort_qk_idx_s08_rt.c= )
MOD_TMP68 = $(MOD_TMP67:sort_qk_idx_s16_rt.c= )
MOD_TMP69 = $(MOD_TMP68:sort_qk_idx_s32_rt.c= )
MOD_TMP70 = $(MOD_TMP69:sort_qk_idx_u08_rt.c= )
MOD_TMP71 = $(MOD_TMP70:sort_qk_idx_u16_rt.c= )
MOD_TMP72 = $(MOD_TMP71:sort_qk_idx_u32_rt.c= )
MOD_TMP73 = $(MOD_TMP72:sort_qk_val_d_rt.c= )
MOD_TMP74 = $(MOD_TMP73:sort_qk_val_r_rt.c= )
MOD_TMP75 = $(MOD_TMP74:sort_qk_val_s08_rt.c= )
MOD_TMP76 = $(MOD_TMP75:sort_qk_val_s16_rt.c= )
MOD_TMP77 = $(MOD_TMP76:sort_qk_val_s32_rt.c= )
MOD_TMP78 = $(MOD_TMP77:sort_qk_val_u08_rt.c= )
MOD_TMP79 = $(MOD_TMP78:sort_qk_val_u16_rt.c= )
MOD_TMP80 = $(MOD_TMP79:sort_qk_val_u32_rt.c= )
MOD_TMP81 = $(MOD_TMP80:srt_qid_findpivot_d_rt.c= )
MOD_TMP82 = $(MOD_TMP81:srt_qid_findpivot_r_rt.c= )
MOD_TMP83 = $(MOD_TMP82:srt_qid_partition_d_rt.c= )
MOD_TMP84 = $(MOD_TMP83:srt_qid_partition_r_rt.c= )
MOD_TMP85 = $(MOD_TMP84:srt_qkrec_c_rt.c= )
MOD_TMP86 = $(MOD_TMP85:srt_qkrec_d_rt.c= )
MOD_TMP87 = $(MOD_TMP86:srt_qkrec_r_rt.c= )
MOD_TMP88 = $(MOD_TMP87:srt_qkrec_z_rt.c= )
MOD_TMP89 = $(MOD_TMP88:randsrccreateseeds_32_rt.c= )
MOD_TMP90 = $(MOD_TMP89:randsrccreateseeds_64_rt.c= )
MOD_TMP91 = $(MOD_TMP90:randsrcinitstate_gc_32_rt.c= )
MOD_TMP92 = $(MOD_TMP91:randsrcinitstate_gc_64_rt.c= )
MOD_TMP93 = $(MOD_TMP92:randsrcinitstate_gz_rt.c= )
MOD_TMP94 = $(MOD_TMP93:randsrcinitstate_u_32_rt.c= )
MOD_TMP95 = $(MOD_TMP94:randsrcinitstate_u_64_rt.c= )
MOD_TMP96 = $(MOD_TMP95:randsrc_gc_c_rt.c= )
MOD_TMP97 = $(MOD_TMP96:randsrc_gc_d_rt.c= )
MOD_TMP98 = $(MOD_TMP97:randsrc_gc_r_rt.c= )
MOD_TMP99 = $(MOD_TMP98:randsrc_gc_z_rt.c= )
MOD_TMP100 = $(MOD_TMP99:randsrc_gz_c_rt.c= )
MOD_TMP101 = $(MOD_TMP100:randsrc_gz_d_rt.c= )
MOD_TMP102 = $(MOD_TMP101:randsrc_gz_r_rt.c= )
MOD_TMP103 = $(MOD_TMP102:randsrc_gz_z_rt.c= )
MOD_TMP104 = $(MOD_TMP103:randsrc_u_c_rt.c= )
MOD_TMP105 = $(MOD_TMP104:randsrc_u_d_rt.c= )
MOD_TMP106 = $(MOD_TMP105:randsrc_u_r_rt.c= )
MOD_TMP107 = $(MOD_TMP106:randsrc_u_z_rt.c= )
MOD_TMP108 = $(MOD_TMP107:buf_copy_frame_to_mem_OL_1ch_rt.c= )
MOD_TMP109 = $(MOD_TMP108:buf_copy_frame_to_mem_OL_rt.c= )
MOD_TMP110 = $(MOD_TMP109:buf_copy_input_to_output_1ch_rt.c= )
MOD_TMP111 = $(MOD_TMP110:buf_copy_input_to_output_rt.c= )
MOD_TMP112 = $(MOD_TMP111:buf_copy_scalar_to_mem_OL_1ch_rt.c= )
MOD_TMP113 = $(MOD_TMP112:buf_copy_scalar_to_mem_OL_rt.c= )
MOD_TMP114 = $(MOD_TMP113:buf_copy_scalar_to_mem_UL_1ch_rt.c= )
MOD_TMP115 = $(MOD_TMP114:buf_copy_scalar_to_mem_UL_rt.c= )
MOD_TMP116 = $(MOD_TMP115:buf_output_frame_1ch_rt.c= )
MOD_TMP117 = $(MOD_TMP116:buf_output_frame_rt.c= )
MOD_TMP118 = $(MOD_TMP117:buf_output_scalar_1ch_rt.c= )
MOD_TMP119 = $(MOD_TMP118:buf_output_scalar_rt.c= )
MOD_TMP120 = $(MOD_TMP119:svd_c_rt.c= )
MOD_TMP121 = $(MOD_TMP120:svd_d_rt.c= )
MOD_TMP122 = $(MOD_TMP121:svd_helper_rt.c= )
MOD_TMP123 = $(MOD_TMP122:svd_r_rt.c= )
MOD_TMP124 = $(MOD_TMP123:rt_matrx.c= )
MOD_TMP125 = $(MOD_TMP124:svd_z_rt.c= )
ifeq "$(UNAME)" "Linux"
	MOD_TMP126 = $(MOD_TMP125:pm_printf.c= )
else
	MOD_TMP126 = $(MOD_TMP125)
endif
MOD_TMP127 = $(MOD_TMP126:HostLib_rtw.c= )
MOD_TMP128 = $(MOD_TMP127:rt_backsubrr_dbl.c= )
MOD_TMP129 = $(MOD_TMP128:rt_forwardsubrr_dbl.c= )
MOD_TMP130 = $(MOD_TMP129:rt_lu_real.c= )
MOD_TMP131 = $(MOD_TMP130:rt_matrixlib_dbl.c= )
MODULES_SRCS = $(MOD_TMP131:HostLib_FFT.c= )

# Remove Opal-RT block sources from the list of S-Functions: they are provided with RT-LAB
# Leave any other S-Functions.
SFS_TMP1 = $(S_FUNCTIONS:recv_param.c=)
SFS_TMP1a = $(SFS_TMP1:RECV_Param.c=)
SFS_TMP2 = $(SFS_TMP1a:recv_rt.c=)
SFS_TMP3 = $(SFS_TMP2:op_send.c=)
SFS_TMP3a = $(SFS_TMP3:OP_SEND.c=)
SFS_TMP4 = $(SFS_TMP3a:send_rt.c=)
SFS_TMP10 = $(SFS_TMP4:sfun_timing.c=)
SFS_TMP11 = $(SFS_TMP10:optrigger.c=)
SFS_TMP19 = $(SFS_TMP11:opsnapshot.c=)
SFS_TMP20 = $(SFS_TMP19:opwritefile.c=)
SFS_TMP21 = $(SFS_TMP20:send_fw.c=)
SFS_TMP22 = $(SFS_TMP21:recv_fw.c=)
SFS_TMP23 = $(SFS_TMP22:simulation_info.c=)
SFS_TMP25 = $(SFS_TMP23:usr_delay.c=)
SFS_TMP26 = $(SFS_TMP25:simulation_events2.c=)


SFS_TMP56 = $(SFS_TMP26:sfun_opfromfile.c=)
SFS_TMP78 = $(SFS_TMP56:sfun_opexternvar.c=)
SFS_TMP79 = $(SFS_TMP78:sfun_time_factor.c=)
SFS_TMP80 = $(SFS_TMP79:sfun_ohci_info.c=)
SFS_TMP84 = $(SFS_TMP80:simulation_events.c=)
SFS_TMP88 = $(SFS_TMP84:sfun_sync_vme200_2.c=)
SFS_TMP92 = $(SFS_TMP88:read_dinamo.c=)
SFS_TMP93 = $(SFS_TMP92:sfun_subsystem_trigger.c=)
SFS_TMP110 = $(SFS_TMP93:sfun_async_st_emit.c=)
SFS_TMP111 = $(SFS_TMP110:sfun_interp_save_disc.c= )
SFS_TMP112 = $(SFS_TMP111:sfun_discreteVariableDelay.c= )

SFS_TMP127 = $(SFS_TMP112:recv_ohci.c=)
SFS_TMP128 = $(SFS_TMP127:send_ohci.c=)
SFS_TMP129 = $(SFS_TMP128:error_status.c=)
SFS_TMP130 = $(SFS_TMP129:fake_io.c=)
SFS_TMP131 = $(SFS_TMP130:op_getpid.c=)
SFS_TMP132 = $(SFS_TMP131:print_msg.c=)
SFS_TMP133 = $(SFS_TMP132:read_pport.c=)
SFS_TMP134 = $(SFS_TMP133:run_model.c=)

SFS_TMP138 = $(SFS_TMP134:opAssertion.c=)
SFS_TMP139 = $(SFS_TMP138:checkoutputwidth.c=)
SFS_TMP140 = $(SFS_TMP139:signalCompression.c=)
SFS_TMP141 = $(SFS_TMP140:signalUncompression.c=)   
SFS_TMP142 = $(SFS_TMP141:opendianswapper.c=)
SFS_TMP143 = $(SFS_TMP142:signalcompression.c=)
SFS_TMP144 = $(SFS_TMP143:signaluncompression.c=)   

SFS_TMP182 = $(SFS_TMP144:pause_model.c=)
SFS_TMP183 = $(SFS_TMP182:opmonitor.c=)

SFS_TMP215 = $(SFS_TMP183:mstack_ccp_cal.c=)
SFS_TMP216 = $(SFS_TMP215:mstack_ccp_in.c=)
SFS_TMP217 = $(SFS_TMP216:mstack_analog_in.c=)
SFS_TMP218 = $(SFS_TMP217:mstack_digital_in.c=)
SFS_TMP219 = $(SFS_TMP218:mstack_ccp_ctl.c=)

SFS_TMP229 = $(SFS_TMP219:pycall.c=)

SFS_TMP238 = $(SFS_TMP229:sfun_opdataset.c=)
SFS_TMP239 = $(SFS_TMP238:sfun_opinterpol.c=)
SFS_TMP240 = $(SFS_TMP239:nrt.c=)
SFS_TMP241 = $(SFS_TMP240:opplotfile.c=)
SFS_TMP242 = $(SFS_TMP241:pubhlaclassattr.c=)
SFS_TMP243 = $(SFS_TMP242:subhlaclassattr.c=)
SFS_TMP244 = $(SFS_TMP243:pubhlainteraction.c=)
SFS_TMP245 = $(SFS_TMP244:subhlainteraction.c=)
SFS_TMP246 = $(SFS_TMP245:pubentitytype.c=)
SFS_TMP247 = $(SFS_TMP246:hlafedoptions.c=)

SFS_TMP260 = $(SFS_TMP247:sfun_xplane.c=)
SFS_TMP261 = $(SFS_TMP260:sfun_opjoystick.c=)

SFS_TMP262 = $(SFS_TMP261:fts2abcd.c=)
SFS_TMP263 = $(SFS_TMP262:fts2flux.c=)
SFS_TMP264 = $(SFS_TMP263:fts2dla.c=)
SFS_TMP265 = $(SFS_TMP264:fts2hfun.c=)
SFS_TMP266 = $(SFS_TMP265:fts2abcd_dtc.c=)

SFS_TMP270 = $(SFS_TMP266:sfun_conversion.c=)
SFS_TMP271 = $(SFS_TMP270:sfun_elements_demux.c=)
SFS_TMP272 = $(SFS_TMP271:sfun_blob_decimation.c=)
SFS_TMP273 = $(SFS_TMP272:sfun_dynamic_rescale.c=)
SFS_TMP274 = $(SFS_TMP273:sfun_DBL2SFP.c=)
SFS_TMP275 = $(SFS_TMP274:sfun_SFP2DBL.c=)
SFS_TMP276 = $(SFS_TMP275:OpDVP.c=)
SFS_TMP277 = $(SFS_TMP276:OpRfm.c=)
SFS_TMP278 = $(SFS_TMP277:OpHei.c=)
SFS_TMP279 = $(SFS_TMP278:OpPickeringBattSim.c=)
SFS_TMP280 = $(SFS_TMP279:OpOutput.c=)
SFS_TMP281 = $(SFS_TMP280:OpInput.c=)
SFS_TMP282 = $(SFS_TMP281:sfun_arincEncoder.c=)
SFS_TMP283 = $(SFS_TMP282:sfun_arincDecoder.c=)

S_FUNC_SRCS = $(SFS_TMP283:optaketime.c=)


#############################################################################
#
#    For CarSim/VehSim/TruckSim by Mechanical SImulation Corp.
#
#    The product name: MSC_PRODUCT_ID         carsim, vehsim, trucksim
#    The product type: MSC_PRODUCT_TYPE       i_i, i_s__ss, s_ss ...
#    Version Number:   MSC_PRODUCT_VERSION    5.25, 6.02, 3.04 ...
#
#############################################################################
ifeq "$(MSC_PRODUCT_TYPE)" ""
# 	Do nothing here
else
  include /usr/$(MSC_PRODUCT_ID)/$(MSC_PRODUCT_VERSION)/$(MSC_PRODUCT_ID).opt
endif
#
#############################################################################
#                 End CarSim/TruckSim/VehSim
#############################################################################

SHARED_SRC := $(subst \,/,$(SHARED_SRC))
SHARED_SRC := $(wildcard $(SHARED_SRC))

SHARED_SRC_DIR := $(subst \,/,$(SHARED_SRC_DIR))

MACHINE = $(shell uname -m)
ifneq (,$(findstring arm, $(MACHINE)))   ### find arm string in the machine type
	# compile the simulink model as a shared library
	# FIXME: we should have a way in the future to select which version of the code to use (RTMAIN vs SimulinkMain) for now force RTMAIN
	WRAPPER_FILE = model_main.c
else
	# compile the simulink model as a binary
	WRAPPER_FILE = model_main.c
endif

ifeq ($(MODELREF_TARGET_TYPE), NONE)
  # Top model for RTW  
  SRCS1               += $(MODEL).c $(WRAPPER_FILE) rt_sim.c $(RTWLOG)  $(SOLVER) $(EXT_SRC) $(MODULES_SRCS) $(SHARED_SRC)
  SRCS1               += $(INTERNAL_ADD_SOURCE_FILE)  $(S_FUNC_SRCS) $(USER_SRCS) 
  SRCS                = $(filter-out $(INTERNAL_IGN_SOURCE_FILE), $(sort $(SRCS1)))

else
  # sub-model for RTW
  SRCS1               += $(MODULES_SRCS)
  SRCS1               += $(INTERNAL_ADD_SOURCE_FILE)  $(S_FUNC_SRCS) $(USER_SRCS) 
  SRCS                = $(filter-out $(INTERNAL_IGN_SOURCE_FILE), $(sort $(SRCS1)))
endif


ifeq "$(UNAME)" "QNX"		##### nto
	ifeq ($(MODELREF_TARGET_TYPE), NONE)
		include qnxnto.opt
	else
		include $(RELATIVE_PATH_TO_ANCHOR)/qnxnto.opt
	endif	
else
	ifeq "$(UNAME)" "Linux"	##### Linux : RedHawk OR Petalinux
		MACHINE = $(shell uname -m)
		ifeq "$(MACHINE)" "x86_64"		#### RedHawk 64
			ifeq ($(MODELREF_TARGET_TYPE), NONE)
				include linux64.opt
			else
				include $(RELATIVE_PATH_TO_ANCHOR)/linux64.opt
			endif			
		else
			ifneq (,$(findstring arm, $(MACHINE)))		#### Petalinux
				ifeq ($(MODELREF_TARGET_TYPE), NONE)
					include petalinux.opt
				else
					include $(RELATIVE_PATH_TO_ANCHOR)/petalinux.opt
				endif
			else	#### RedHawk 32x
				ifeq ($(MODELREF_TARGET_TYPE), NONE)
					include linux32.opt
				else
					include $(RELATIVE_PATH_TO_ANCHOR)/linux32.opt
				endif
			endif
		endif
	else
		ifeq ($(MODELREF_TARGET_TYPE), NONE)
			include win32.opt
		else
			include $(RELATIVE_PATH_TO_ANCHOR)/OpNTtarget/win32.opt
		endif
	endif
endif

#------------------------------ Include Path -----------------------------

MATLAB_INCLUDES = -I$(TARGET_MATLAB_ROOT)/simulink/include \
-I$(TARGET_MATLAB_ROOT)/extern/include \
-I$(TARGET_MATLAB_ROOT)/rtw/c/src \
-I$(TARGET_MATLAB_ROOT)/rtw/c/src/matrixmath \

ifeq "$(UNAME)" "QNX"		##### nto
	MATLAB_INCLUDES += -I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/drive \
	-I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/mech \
	-I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/foundation \
	-I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/math \
	-I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/lang \
	-I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/external \
	-I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/network_engine \
	-I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/ne_sli \
	-I$(TARGET_MATLAB_ROOT)/toolbox/dspblks/include \
    -I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/compiler/core/c \
    -I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/engine/sli/c \
    -I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/engine/core/c \
    -I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/utils \
    -I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/pm_math
else
	ifeq "$(UNAME)" "Linux"	##### Linux (RedHawk)
		MATLAB_INCLUDES += -I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/drive \
		-I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/mech \
		-I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/foundation \
		-I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/math \
		-I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/lang \
		-I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/external \
		-I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/network_engine \
		-I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/ne_sli \
		-I$(TARGET_MATLAB_ROOT)/toolbox/dspblks/include \
		-I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/compiler/core/c \
		-I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/engine/sli/c \
		-I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/engine/core/c \
		-I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/utils \
		-I$(TARGET_MATLAB_ROOT)/toolbox/simscape/include/pm_math
	else
		MATLAB_INCLUDES += -I$(TARGET_MATLAB_ROOT)/toolbox/physmod/drive/c \
		-I$(TARGET_MATLAB_ROOT)/toolbox/physmod/mech/c \
		-I$(TARGET_MATLAB_ROOT)/toolbox/physmod/foundation/c \
		-I$(TARGET_MATLAB_ROOT)/toolbox/physmod/ne_sli/c \
		-I$(TARGET_MATLAB_ROOT)/toolbox/physmod/simscape/engine/sli/c \
		-I$(TARGET_MATLAB_ROOT)/toolbox/physmod/simscape/engine/sli/c/win64 \
		-I$(TARGET_MATLAB_ROOT)/toolbox/physmod/simscape/engine/core/c \
		-I$(TARGET_MATLAB_ROOT)/toolbox/physmod/simscape/engine/core/c/win64 \
		-I$(TARGET_MATLAB_ROOT)/toolbox/physmod/network_engine/c \
		-I$(TARGET_MATLAB_ROOT)/toolbox/physmod/network_engine/c/win64 \
		-I$(TARGET_MATLAB_ROOT)/toolbox/physmod/common/foundation/core/c \
		-I$(TARGET_MATLAB_ROOT)/toolbox/physmod/common/foundation/core/c/win64 \
		-I$(TARGET_MATLAB_ROOT)/toolbox/physmod/common/math/core/c \
		-I$(TARGET_MATLAB_ROOT)/toolbox/physmod/common/math/core/c/win64 \
		-I$(TARGET_MATLAB_ROOT)/toolbox/physmod/common/lang/core/c \
		-I$(TARGET_MATLAB_ROOT)/toolbox/physmod/common/lang/core/c/win64 \
		-I$(TARGET_MATLAB_ROOT)/toolbox/physmod/simscape/compiler/core/c \
		-I$(TARGET_MATLAB_ROOT)/toolbox/physmod/simscape/compiler/core/c/win64 \
		-I$(TARGET_MATLAB_ROOT)/toolbox/physmod/extern/include \
		-I$(TARGET_MATLAB_ROOT)/toolbox/dsp/include \
		-I$(TARGET_MATLAB_ROOT)/toolbox/shared/dspblks/extern/include \
		-I$(TARGET_MATLAB_ROOT)/toolbox/shared/dspblks/extern/src \
		-I$(TARGET_MATLAB_ROOT)/toolbox/shared/spc/src_ml/extern/include \
		-I$(TARGET_MATLAB_ROOT)/toolbox/shared/spc/src_ml/extern/src \
		-I$(TARGET_MATLAB_ROOT)/toolbox/dsp/extern/src 
	endif
endif

RTLAB_INCLUDES = \
	-I$(TARGET_RTLAB_ROOT)/common/include \
	-I$(TARGET_RTLAB_ROOT)/common/include_target \
	-I$(TARGET_RTLAB_ROOT)/RT-LAB/include
    
SHARED_INCLUDES =
ifneq ($(SHARED_SRC_DIR),)
    SHARED_INCLUDES = -I$(SHARED_SRC_DIR) 
endif

INCLUDES = -I. $(MATLAB_INCLUDES) $(RTLAB_INCLUDES) $(INTERNAL_INCLUDE_PATH) $(USER_INCS) $(MODELREF_INC_PATH) $(SHARED_INCLUDES)


#------------------------ rtModel ---------------------------------------------- 
#define USE_RTMODEL	1
RTM_CC_OPTS = -DUSE_RTMODEL
ifeq ($(OP_DISCRETE_SOLVER),1)
RTM_CC_OPTS = -DUSE_RTMODEL -DDISCRETE_SOLVER
endif

#-------------------------------- C Flags --------------------------------
# General User Options
#OLDMATLABVERSION = 0

ifeq ($(OP_MATLABR2011A),1)
MATLABVERSION_CFLAGS = -DOP_MATLABR2011A
endif
ifeq ($(OP_MATLABR2011B),1)
MATLABVERSION_CFLAGS = -DOP_MATLABR2011B
endif
ifeq ($(OP_MATLABR2012A),1)
MATLABVERSION_CFLAGS = -DOP_MATLABR2012A
endif
ifeq ($(OP_MATLABR2012B),1)
MATLABVERSION_CFLAGS = -DOP_MATLABR2012B
endif
ifeq ($(OP_MATLABR2013A),1)
MATLABVERSION_CFLAGS = -DOP_MATLABR2013A
endif
ifeq ($(OP_MATLABR2013B),1)
MATLABVERSION_CFLAGS = -DOP_MATLABR2013B
endif
ifeq ($(OP_MATLABR2014A),1)
MATLABVERSION_CFLAGS = -DOP_MATLABR2014A
endif
ifeq ($(OP_MATLABR2014B),1)
MATLABVERSION_CFLAGS = -DOP_MATLABR2014B
endif
ifeq ($(OP_MATLABR2015A),1)
MATLABVERSION_CFLAGS = -DOP_MATLABR2015A
endif
ifeq ($(OP_MATLABR2015B),1)
MATLABVERSION_CFLAGS = -DOP_MATLABR2015B
endif
ifeq ($(OP_MATLABR2016A),1)
MATLABVERSION_CFLAGS = -DOP_MATLABR2016A
endif
ifeq ($(OP_MATLABR2016B),1)
MATLABVERSION_CFLAGS = -DOP_MATLABR2016B
endif
ifeq ($(OP_MATLABR2017A),1)
MATLABVERSION_CFLAGS = -DOP_MATLABR2017A
endif
ifeq ($(OP_MATLABR2017B),1)
MATLABVERSION_CFLAGS = -DOP_MATLABR2017B
endif
ifeq ($(OP_MATLABR2018A),1)
MATLABVERSION_CFLAGS = -DOP_MATLABR2018A
endif
ifeq ($(OP_MATLABR2018B),1)
MATLABVERSION_CFLAGS = -DOP_MATLABR2018B
endif
OPTS =

ANSI_OPTS =

CC_OPTS   = -c  $(OPT_OPTS) $(OPTS) $(ANSI_OPTS) $(EXT_CC_OPTS) $(RTM_CC_OPTS)
CC_OPTS77 = -c  $(OPT_OPTS77) $(OPTS) $(ANSI_OPTS) $(EXT_CC_OPTS) $(RTM_CC_OPTS)

CPP_REQ_DEFINES = -DMODEL=$(MODEL) -DRT=RT -DNUMST=$(NUMST) \
                  -DTID01EQ=$(TID01EQ) -DNCSTATES=$(NCSTATES) \
                  -DMT=$(MULTITASKING) \
                  -DTERMFCN=$(TERMFCN) \
                  -DMULTITASKING=$(MULTITASKING) -D_SIMULINK -DRTLAB $(MATLABVERSION_CFLAGS)	

# Skip variables that have not been expanded (they contain |>)

ifeq (,$(findstring |>,$(MAT_FILE)))
CPP_REQ_DEFINES += -DMAT_FILE=$(MAT_FILE)
endif
ifeq (,$(findstring |>,$(CLASSIC_INTERFACE)))
CPP_REQ_DEFINES += -DCLASSIC_INTERFACE=$(CLASSIC_INTERFACE)
endif
ifeq (,$(findstring |>,$(ONESTEPFCN)))
CPP_REQ_DEFINES += -DONESTEPFCN=$(ONESTEPFCN)
endif
ifeq (,$(findstring |>,$(MULTI_INSTANCE_CODE)))
CPP_REQ_DEFINES += -DMULTI_INSTANCE_CODE=$(MULTI_INSTANCE_CODE)
endif
                  
CFLAGS   = $(CC_OPTS) $(CPP_REQ_DEFINES) $(TARGET_CFLAGS) $(INCLUDES)
CFLAGS77 = $(CC_OPTS77) $(CPP_REQ_DEFINES) $(TARGET_CFLAGS) $(INCLUDES)

#------------------------------- LD Flags --------------------------------
### SHARED_LIB_FLAG is only defined in petalinux.opt because it is required to compile the model as a shared library
LDFLAGS = $(SHARED_LIB_FLAG) $(LD_DEBUG_OPTS) $(LIBPATH) $(EXT_LD_OPTS) $(RTLAB_LDFLAGS)


#--------------------------------- Rules ---------------------------------

ifeq "$(UNAME)" "QNX"		##### nto
		ifeq ($(MODELREF_TARGET_TYPE), NONE)
			include posix.rules
		else
			include $(RELATIVE_PATH_TO_ANCHOR)/posix.rules
		endif
else
	ifeq "$(UNAME)" "Linux"	##### Linux (RedHawk)
		ifeq ($(MODELREF_TARGET_TYPE), NONE)
			include posix.rules
		else
			include $(RELATIVE_PATH_TO_ANCHOR)/posix.rules
		endif		
	else
		ifeq ($(MODELREF_TARGET_TYPE), NONE)
			include win32.rules
		else
			include $(RELATIVE_PATH_TO_ANCHOR)/OpNTtarget/win32.rules
		endif


# Libraries:
ifeq ($(USE_EXPAND_RTWLIB),1)

else

MODULES_rtwlib = rt_backsubcc_dbl.obj \
		 rt_backsubcc_sgl.obj \
		 rt_backsubrc_dbl.obj \
		 rt_backsubrc_sgl.obj \
		 rt_backsubrr_dbl.obj \
		 rt_backsubrr_sgl.obj \
		 rt_forwardsubcc_dbl.obj \
		 rt_forwardsubcc_sgl.obj \
		 rt_forwardsubcr_dbl.obj \
		 rt_forwardsubcr_sgl.obj \
		 rt_forwardsubrc_dbl.obj \
		 rt_forwardsubrc_sgl.obj \
		 rt_forwardsubrr_dbl.obj \
		 rt_forwardsubrr_sgl.obj \
		 rt_lu_cplx.obj \
		 rt_lu_cplx_sgl.obj \
		 rt_lu_real.obj \
		 rt_lu_real_sgl.obj \
		 rt_matdivcc_dbl.obj \
		 rt_matdivcc_sgl.obj \
		 rt_matdivcr_dbl.obj \
		 rt_matdivcr_sgl.obj \
		 rt_matdivrc_dbl.obj \
		 rt_matdivrc_sgl.obj \
		 rt_matdivrr_dbl.obj \
		 rt_matdivrr_sgl.obj \
		 rt_matmultandinccc_dbl.obj \
		 rt_matmultandinccc_sgl.obj \
		 rt_matmultandinccr_dbl.obj \
		 rt_matmultandinccr_sgl.obj \
		 rt_matmultandincrc_dbl.obj \
		 rt_matmultandincrc_sgl.obj \
		 rt_matmultandincrr_dbl.obj \
		 rt_matmultandincrr_sgl.obj \
		 rt_matmultcc_dbl.obj \
		 rt_matmultcc_sgl.obj \
		 rt_matmultcr_dbl.obj \
		 rt_matmultcr_sgl.obj \
		 rt_matmultrc_dbl.obj \
		 rt_matmultrc_sgl.obj \
		 rt_matmultrr_dbl.obj \
		 rt_matmultrr_sgl.obj
endif

$(RTWLIB) : 
	@echo ### Creating $@
	-@md $(RTW_PROGRAMDATA_PATH)
	-@md $(RTWLIB_PATH)

ifeq ($(USE_EXPAND_RTWLIB),1)
	$(CC) $(CFLAGS) $(ALT_MATLAB_ROOT)\rtw\c\src\*.c
else
	$(CC) $(CFLAGS) $(ALT_MATLAB_ROOT)\rtw\c\src\matrixmath\*.c
endif
	$(LIBCMD) /nologo /out:$@ $(MODULES_rtwlib)
	@echo ### Created $@

endif
endif



ifeq "$(UNAME)" "QNX"		##### nto
MODELREF_LINK_LIBS_MAIN :
	@for A in $(MODELREFS); do $(MAKE)  -C $(SHARED_SRC_DIR)/../$$A -f $$A.mk; done
else
ifeq "$(UNAME)" "Linux"	##### Linux (RedHawk)
MODELREF_LINK_LIBS_MAIN :
	@for A in $(MODELREFS); do $(MAKE)  -C $(SHARED_SRC_DIR)/../$$A -f $$A.mk; done
else
MODELREF_LINK_LIBS_MAIN :
	@FOR %A IN ($(MODELREFS)) DO $(MAKE) -C $(SHARED_SRC_DIR)/../%A -f %A.mk
endif
endif