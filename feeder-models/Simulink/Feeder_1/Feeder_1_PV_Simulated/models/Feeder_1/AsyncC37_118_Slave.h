/*-------------------------------------------------------------------
 *  OPAL-RT Technologies inc
 *
 *  Copyright (C) 2015. All rights reserved.
 *
 *  File name =         AsyncC37_118_Slave.h
 *  Last modified by =  Simon Labbé
 *
 *
 *-----------------------------------------------------------------*/

#ifndef OPAL_IP_H
#define OPAL_IP_H

#ifndef PROGNAME
#define PROGNAME "AsyncIPUtils"
#endif
/* Modify this version line if you make changes to this file */
#define VERSION  "Opal-RT_20060524"

#include <errno.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/time.h>
#include <sys/socket.h>
#include <netinet/in.h>

#ifndef RT
#define RT
#endif
#include "OpalPrint.h"
#include "AsyncApi.h"
#include "OpalGenAsyncParamCtrl.h"
#pragma pack()

#define  ASYNC_C37_118_NBR_SEND_BLOCK               6   
#define  ASYNC_C37_118_NBR_TS_INPUTS                3   

#define  ASYNC_C37_118_PARAM_IX_DEV_FNCT            0
#define  ASYNC_C37_118_PARAM_IX_PROTO               1
#define  ASYNC_C37_118_PARAM_IX_PORT_LOCAL          2
#define  ASYNC_C37_118_PARAM_IX_DATA_RATE           3
#define  ASYNC_C37_118_PARAM_IX_TIMEBASE            4
#define  ASYNC_C37_118_PARAM_IX_TS_INPUT            5
#define  ASYNC_C37_118_PARAM_IX_UDP_DATA_PORT       6
#define  ASYNC_C37_118_PARAM_IX_CORE_NBR            7

#define  ASYNC_C37_118_PARAM_IX_NIC_NAME            0
#define  ASYNC_C37_118_PARAM_IX_IP_ADDR_LOCAL       1
#define  ASYNC_C37_118_PARAM_IX_PMU_NAME            2
#define  ASYNC_C37_118_PARAM_IX_NOMINAL_FREQ        3
#define  ASYNC_C37_118_PARAM_IX_CFG_NAME            4

#define  ASYNC_C37_118_DEV_FNCT_SLAVE               1
#define  ASYNC_C37_118_DEV_FNCT_MASTER              2
                           
#define  ASYNC_C37_118_MAX_CFG_FILE_NAME_LEN       40     


#define	EOK		                                    0

#endif
