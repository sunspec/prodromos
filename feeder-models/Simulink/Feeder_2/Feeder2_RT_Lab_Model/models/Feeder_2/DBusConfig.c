/*-------------------------------------------------------------------
 *  OPAL-RT Technologies inc
 *
 *  Copyright (C) 2014. All rights reserved.
 *
 *  File name =         DBusConfig.c
 *  Last modified by =  Julien Darrah
 *
 *	This file is used to configure the DBus Communication
 *	It is suggested to make a backup copy before modifying
 *  Follow Step1 through 4
 *
 *-----------------------------------------------------------------*/
 
 #include "DBusConfig.h"
 
 
 /*******************************************************************************************************************************/
 /* STEP 1																														*/
 /* - Select the Component Type:																								*/
 /*	  Slave -> 				DBUS_COMPONENT_TYPE_SLAVE																			*/
 /*   Single Master -> 		DBUS_COMPONENT_TYPE_MASTER_SINGLE   																*/
 /*   Mutliple Master -> 	DBUS_COMPONENT_TYPE_MASTER_MULTI																	*/
 /*   Suppervisor ->		DBUS_COMPONENT_TYPE_SUPERVISOR					 													*/
 /*																																*/
 /* - Name the Component Ex: "OPAL-RT_HIL"																						*/
 /*																																*/
 /*******************************************************************************************************************************/
 /* Function 0x0A - Register Components Definition 																				*/
 /*******************************************************************************************************************************/				

  
 /* Component Type */
 DBUS_u8PayloadDataType			DBUS_u8ComponentType = DBUS_COMPONENT_TYPE_SLAVE ;
 
 /* Component Name */
 DBUS_u8ComponentNameType		DBUS_au8ComponentName[] = "OpenDSS";
 
 #define DBUS_COMPONENT_DEFINITION_SIZE (sizeof(DBUS_u8ComponentType))
 const unsigned int DBUS_u32ComponentTypeDefinitionSize = DBUS_COMPONENT_DEFINITION_SIZE;
 
 #define DBUS_COMPONENT_NAME_DEFINITION_SIZE (sizeof(DBUS_au8ComponentName)-1)
 const unsigned int DBUS_u32ComponentNameDefinitionSize = DBUS_COMPONENT_NAME_DEFINITION_SIZE;
 
 /*******************************************************************************************************************************/
 /* STEP 2																														*/
 /* - Specify the Number of Variables for the Component																			*/
 /*	- Specify each Variable Names seperated by a comma with no spaces Ex: "Va,Vb,Vc,"											*/
 /* - Specify the Data Type for each Variables:																					*/
 /*   Integer -> 		DBUS_COMPONENT_VARIABLE_INTERGER_TYPE   																*/
 /*   Double -> 		DBUS_COMPONENT_VARIABLE_DOUBLE_TYPE																		*/
 /*   Float ->			DBUS_COMPONENT_VARIABLE_SINGLE_TYPE					 													*/
 /*   Bool ->			DBUS_COMPONENT_VARIABLE_BOOL_TYPE					 													*/
 /*																																*/
 /*																																*/
 /*******************************************************************************************************************************/
 /* Function 0x0B - Register Component Variables Definition 																		*/
 /*******************************************************************************************************************************/
 
 /* Number of Variables */
 DBUS_u16ComponentVariableCountType		DBUS_u16ComponentVariableCount = 64U;
 
 /* Variable Names */
 DBUS_u8PayloadDataType					DBUS_au8ComponentVariableName[] = "Va1,Vb1,Vc1,F1,Va2,F2,Va3,F3,Vc4,F4,Va5,F5,Vb6,F6,Vc7,F7,Va8,F8,Vb9,F9,Vc10,F10,Va11,F11,Vb12,F12,Vc13,F13,Va14,F14,Vb15,F15,Vc16,F16,Va17,F17,Vb18,F18,Vc19,F19,Va20,F20,Vb21,F21,Vc22,F22,Va23,F23,Vb24,F24,Vc25,F25,Va26,F26,Vb27,F27,Vc28,F28,Va29,F29,Vb30,F30,Vc31,F31,";
 
 /* Variables Data Types */
 DBUS_u8PayloadDataType					DBUS_au8ComponentVariableType[] = {  DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,


 
 
 
                                              };
 
 #define DBUS_COMPONENT_VARIABLE_COUNT_SIZE (sizeof(DBUS_u16ComponentVariableCount))
 const unsigned int DBUS_u32ComponentVariableCountSize = DBUS_COMPONENT_VARIABLE_COUNT_SIZE;
 
 #define DBUS_COMPONENT_VARIABLE_NAME_SIZE (sizeof(DBUS_au8ComponentVariableName)-1)
 const unsigned int DBUS_u32ComponentVariableNameSize = DBUS_COMPONENT_VARIABLE_NAME_SIZE;

 #define DBUS_COMPONENT_VARIABLE_TYPE_SIZE (sizeof(DBUS_au8ComponentVariableType))
 const unsigned int DBUS_u32ComponentVariableTypeSize = DBUS_COMPONENT_VARIABLE_TYPE_SIZE; 
  
  
  
 /*******************************************************************************************************************************/
 /* STEP 3																														*/
 /* - Specify the Number of Components to Subscribe to																			*/
 /*	- Specify each Component Names seperated by a comma with no spaces Ex: "M01,SL01,"											*/
 /* - Specify the Number of Variables per Components Ex: { 0001U, 0001U }														*/
 /*	- Specify each Variable Names per Component seperated by a comma with no spaces	Ex: "time,voltage,"							*/
 /*	- Select the Subscribe or poll option by changing the < #define DBUS_SUBSCRIPTION_ENABLE > in the .h file					*/
 /* - Specify the Data Type for each Variables:																					*/
 /*   Integer -> 		DBUS_COMPONENT_VARIABLE_INTERGER_TYPE   																*/
 /*   Double -> 		DBUS_COMPONENT_VARIABLE_DOUBLE_TYPE																		*/
 /*   Float ->			DBUS_COMPONENT_VARIABLE_SINGLE_TYPE					 													*/
 /*   Bool ->			DBUS_COMPONENT_VARIABLE_BOOL_TYPE					 													*/
 /*																																*/
 /*******************************************************************************************************************************/
 /* Both Functions have the same format	only the function changes																*/																						
 /* Function 0x0D - Subscripbe to Component Variables Definition 																*/
 /* Function 0x0E - Request the Content of a Component Variables																*/
 /*******************************************************************************************************************************/
 
 /* Number of Components */
 DBUS_u8PayloadDataType					DBUS_u8SubscriptionComponentCounts = 1U;
 
 /* Component Name */
 DBUS_u8PayloadDataType					DBUS_au8SubscriptionComponentNames[] = "PVSIM,";
 
 /* Number of Variables per Components */
 DBUS_u16ComponentVariableCountType		DBUS_au8SubscriptionVariableCount[]	= { 62U };
 
 /* Variable Names */
 DBUS_u8PayloadDataType					DBUS_au8SubscriptionComponentVariableName[] = "P1,Q1,P2,Q2,P3,Q3,P4,Q4,P5,Q5,P6,Q6,P7,Q7,P8,Q8,P9,Q9,P10,Q10,P11,Q11,P12,Q12,P13,Q13,P14,Q14,P15,Q15,P16,Q16,P17,Q17,P18,Q18,P19,Q19,P20,Q20,P21,Q21,P22,Q22,P23,Q23,P24,Q24,P25,Q25,P26,Q26,P27,Q27,P28,Q28,P29,Q29,P30,Q30,P31,Q31,";
 
 /* Variables Data Types */
 DBUS_u8PayloadDataType					DBUS_au8SubscriptionComponentVariableType[] = {  DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,
 DBUS_COMPONENT_VARIABLE_SINGLE_TYPE,

 
 
 
 
                                                   };
 
 #define DBUS_SUBSCRIBE_COMPONENT_COUNT_SIZE (sizeof(DBUS_u8SubscriptionComponentCounts))
 const unsigned int DBUS_u32SubscribeComponentCountSize = DBUS_SUBSCRIBE_COMPONENT_COUNT_SIZE;
 
 #define DBUS_SUBSCRIBE_COMPONENT_NAME_SIZE (sizeof(DBUS_au8SubscriptionComponentNames)-1)
 const unsigned int DBUS_u32SubscribeComponentNameSize = DBUS_SUBSCRIBE_COMPONENT_NAME_SIZE;

 #define DBUS_SUBSCRIBE_COMPONENT_VARIABLE_COUNT_SIZE (sizeof(DBUS_au8SubscriptionVariableCount)/sizeof(DBUS_au8SubscriptionVariableCount[0]))
 const unsigned int DBUS_u32SubscribeComponentVariableCountSize = DBUS_SUBSCRIBE_COMPONENT_VARIABLE_COUNT_SIZE; 
 
 #define DBUS_SUBSCRIBE_COMPONENT_VARIABLE_NAME_SIZE (sizeof(DBUS_au8SubscriptionComponentVariableName)-1)
 const unsigned int DBUS_u32SubscribeComponentVariableNameSize = DBUS_SUBSCRIBE_COMPONENT_VARIABLE_NAME_SIZE;
 
 #define DBUS_SUBSCRIBE_COMPONENT_VARIABLE_TYPE_SIZE (sizeof(DBUS_au8SubscriptionComponentVariableType)/sizeof(DBUS_au8SubscriptionComponentVariableType[0]))
 const unsigned int DBUS_u32SubscribeComponentVariableTypeSize = DBUS_SUBSCRIBE_COMPONENT_VARIABLE_TYPE_SIZE;
 
  /* This value is computed once during the init part, tells the total size in bytes of all the variables to be received*/
 unsigned int DBUS_SubscribeComponentVariableTotalSize = 0;
 

 /*******************************************************************************************************************************/
 /* STEP 4																														*/
 /* - Declare the Component Variables with their data type																		*/
 /* 	Data Types:																												*/
 /*					Bool ->			DBUS_u8DataTypeBoolType																		*/
 /*					Integer ->		DBUS_i32DataTypeIntegerType;																*/
 /*					Float ->		DBUS_f32DataTypeFloatType;																	*/
 /*					Double ->		DBUS_f64DataTypeDoubleType;																	*/
 /*																																*/
 /*	- Populate the DBUS_astUpdateVariables[] Array																				*/
 /* - Specify the Data Type for each Variables:																					*/
 /*   Integer -> 		DBUS_COMPONENT_VARIABLE_INTERGER_TYPE   																*/
 /*   Double -> 		DBUS_COMPONENT_VARIABLE_DOUBLE_TYPE																		*/
 /*   Float ->			DBUS_COMPONENT_VARIABLE_SINGLE_TYPE					 													*/
 /*   Bool ->			DBUS_COMPONENT_VARIABLE_BOOL_TYPE					 													*/
 /*																																*/
 /*******************************************************************************************************************************/
 /* Function 0x0F - Component Variable Update 																					*/
 /*******************************************************************************************************************************/
 
 /* This value is computed once during the init part, tells the total size in bytes of all the variables */
 unsigned int DBUS_UpdateVariablesTotalSize = 0;
 
 // /* Make sure the declared order and the data type is the same as when the Registration was done using Function 0x0B */
 // /* Variable Declarations */
// /*  DBUS_f64DataTypeDoubleType		DBUS_u64Va;
 // DBUS_f64DataTypeDoubleType		DBUS_u64Vb;
 // DBUS_f64DataTypeDoubleType		DBUS_u64Vc; */ 

// #define DBUS_MACRO_VARIABLE_POINTER(variable)				(DBUS_u8PayloadDataType*)(&variable)
// #define DBUS_MACRO_VARIABLE_SIZE(variable)					(DBUS_u8PayloadDataType)(sizeof(variable))

 // DBUS_stUpdateVariablesType			DBUS_astUpdateVariables[] =
 // {	/* Variable */												/* Variable Size */
	// {	DBUS_MACRO_VARIABLE_SIZE(DBUS_f64DataTypeDoubleType),		DBUS_COMPONENT_VARIABLE_DOUBLE_TYPE					},
	// {	DBUS_MACRO_VARIABLE_SIZE(DBUS_f64DataTypeDoubleTy62pe),		DBUS_COMPONENT_VARIABLE_DOUBLE_TYPE					},
	// {	DBUS_MACRO_VARIABLE_SIZE(DBUS_f64DataTypeDoubleType),		DBUS_COMPONENT_VARIABLE_DOUBLE_TYPE					}
	
 // };
 
// #define DBUS_UPDATE_VARIABLE_TABLE_SIZE (sizeof(DBUS_astUpdateVariables)/sizeof(DBUS_astUpdateVariables[0]))
 // const unsigned int DBUS_u32UpdateVariableTableSize = DBUS_UPDATE_VARIABLE_TABLE_SIZE;
 
 /* Flag indicating the DBUS Component was initialized */
 unsigned int DBUS_ConfigInitFlagDone;
 