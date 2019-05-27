/*-------------------------------------------------------------------
 *  OPAL-RT Technologies inc
 *
 *  Copyright (C) 2014. All rights reserved.
 *
 *  File name =         DBusConfig.h
 *  Last modified by =  Julien Darrah
 *
 *	This file is used to configure the DBus Communication
 *
 *
 *
 *-----------------------------------------------------------------*/
 
 
 
 #define DBUS_MAX_DATA_PAYLOAD_SIZE						65535U
 
 
 /* Funtion 0x0A - Register Components */
 #define DBUS_FUNCTION_REGISTER_COMPONENT				0x0AU
 /* Type of components definition */
 #define DBUS_COMPONENT_TYPE_SLAVE  		 			0x01U
 #define DBUS_COMPONENT_TYPE_MASTER_SINGLE   			0x0FU
 #define DBUS_COMPONENT_TYPE_MASTER_MULTI				0xFFU
 #define DBUS_COMPONENT_TYPE_SUPERVISOR					0xAFU 
 
 /* Funtion 0x0B - Register Component Variable */
 #define DBUS_FUNCTION_REGISTER_COMPONENT_VARIABLE		0x0BU
 /* Type of Variable definition */
 #define DBUS_COMPONENT_VARIABLE_INTERGER_TYPE  		0x01U
 #define DBUS_COMPONENT_VARIABLE_DOUBLE_TYPE  			0x02U
 #define DBUS_COMPONENT_VARIABLE_SINGLE_TYPE  			0x03U
 #define DBUS_COMPONENT_VARIABLE_BOOL_TYPE  			0x04U
 
  /* Funtion 0x0D - Subscripbe Component Variable */
 #define DBUS_FUNCTION_SUBSCRIBE_COMPONENT_VARIABLE		0x0DU
 
  /* Funtion 0x0E - Request the Content of Component Variables */
 #define DBUS_FUNCTION_REQUEST_CONTENT_COMPONENT_VARIABLE		0x0EU

  /* Funtion 0x0F - Component Variable Update */
 #define DBUS_FUNCTION_UPDATE_COMPONENT_VARIABLE		0x0FU

 
 /* Variable Data Types */
 typedef unsigned char				DBUS_u8DataTypeBoolType;	
 typedef int						DBUS_i32DataTypeIntegerType;
 typedef float						DBUS_f32DataTypeFloatType;
 typedef double						DBUS_f64DataTypeDoubleType;
   
 typedef unsigned char				DBUS_u8PayloadDataType;
 typedef unsigned char 				DBUS_u8FunctionType;
 typedef unsigned int 				DBUS_u32SizeType;
 
 typedef DBUS_u8PayloadDataType		DBUS_u8ComponentNameType;
 typedef unsigned short				DBUS_u16ComponentVariableCountType;

 
 /* DBUS Packet structure definition */
 typedef struct
 {
	 DBUS_u32SizeType			u32Size;
	 DBUS_u8FunctionType		u8Function;
	 DBUS_u8PayloadDataType		u8Data[DBUS_MAX_DATA_PAYLOAD_SIZE];
	 
 } DBUS_stPacketConfigType;
 
 
  /* Funtion 0x0F - Component Variable Update */
 typedef struct
 {
	// DBUS_u8PayloadDataType					*pu8VariableContent;
	 DBUS_u8PayloadDataType					u8VariableSize;
	 DBUS_u8PayloadDataType					u8VariableDataType;
	 
 } DBUS_stUpdateVariablesType;
 
 #define DBUS_COMPONENT_INIT_FLAG_DONE			1U
 #define DBUS_COMPONENT_INIT_FLAG_NO_DONE		0U
 
 /***********************************************************************************************************/
 /* FUNCTIONS Declarations																					*/
 /***********************************************************************************************************/
 
 

 /***********************************************************************************************************/
 /* EXTERN VARIABLES Declarations																			*/
 /***********************************************************************************************************/ 
  
  
 /***********************************************************************************************************/
 /* Funtion 0x0A - Register Components Definition 															*/
 /***********************************************************************************************************/ 
 
 extern  unsigned int DBUS_ConfigInitFlagDone;
  
 /* Component Name */
 extern DBUS_u8ComponentNameType		DBUS_au8ComponentName[];
 /* Component Type */
 extern DBUS_u8PayloadDataType			DBUS_u8ComponentType;
  
 extern  const unsigned int DBUS_u32ComponentTypeDefinitionSize;
 extern  const unsigned int DBUS_u32ComponentNameDefinitionSize;
 
 /************************************************************************************************************/
 /* Funtion 0x0B - Register Component Variables Definition 													 */
 /************************************************************************************************************/
 
 /* Number of Variables */
 extern DBUS_u16ComponentVariableCountType		DBUS_u16ComponentVariableCount;
 /* Variable Names */
 extern DBUS_u8PayloadDataType					DBUS_au8ComponentVariableName[];
 /* Variables Data Types */
 extern DBUS_u8PayloadDataType					DBUS_au8ComponentVariableType[];

 extern const unsigned int DBUS_u32ComponentVariableCountSize;
 extern const unsigned int DBUS_u32ComponentVariableNameSize;
 extern const unsigned int DBUS_u32ComponentVariableTypeSize; 
  
 /*******************************************************************************************************************************/
 /* Funtion 0x0D or 0x0E - Subscripbe to Component Variables Definition 														*/
 /*******************************************************************************************************************************/
 
 /* To enable subscription change value to 1, to use polling mode change to 0 */
 #define DBUS_SUBSCRIPTION_ENABLE				1
 
 /* Number of Components */
 extern DBUS_u8PayloadDataType					DBUS_u8SubscriptionComponentCounts;
 /* Component Name */
 extern DBUS_u8PayloadDataType					DBUS_au8SubscriptionComponentNames[];
 /* Number of Variables per Components */
 extern DBUS_u16ComponentVariableCountType		DBUS_au8SubscriptionVariableCount[];
 /* Variable Names */
 extern DBUS_u8PayloadDataType					DBUS_au8SubscriptionComponentVariableName[];
 
 extern DBUS_u8PayloadDataType					DBUS_au8SubscriptionComponentVariableType[];
 
 extern const unsigned int DBUS_u32SubscribeComponentCountSize;
 extern const unsigned int DBUS_u32SubscribeComponentNameSize;
 extern const unsigned int DBUS_u32SubscribeComponentVariableCountSize; 
 extern const unsigned int DBUS_u32SubscribeComponentVariableNameSize;
 extern const unsigned int DBUS_u32SubscribeComponentVariableTypeSize;
 
 /*******************************************************************************************************************************/
 /* Function 0x0F - Component Variable Update 																					*/
 /*******************************************************************************************************************************/

 /* This value is computed once during the init part, tells the total size in bytes of all the variables */
 extern unsigned int DBUS_UpdateVariablesTotalSize;
 
 /* Component Variable Update Table */
 extern DBUS_stUpdateVariablesType				DBUS_astUpdateVariables[];
 
 extern const unsigned int DBUS_u32UpdateVariableTableSize;
   /* This value is computed once during the init part, tells the total size in bytes of all the variables to be received*/
 extern unsigned int DBUS_SubscribeComponentVariableTotalSize;
 
 
 
 
 