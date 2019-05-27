/*-------------------------------------------------------------------
 *  OPAL-RT Technologies inc
 *
 *  Copyright (C) 2015. All rights reserved.
 *
 *  File name =         AsyncC37_118_Slave.c
 *  Last modified by =  Simon Labbé
 *
 *  This is code example of an asynchronous program to control 
 *  C37.118 communication. It is started by the asynchronous
 *  controller and waiting for a connection incoming from
 *  an external.  C37.118 master.
 *
 *  The code is only implementing basic communication. Feel free
 *  to use it as a starting point for your own asynchronous
 *  application. 
 *-----------------------------------------------------------------*/
#ifndef WIN32
#define PROGNAME "AsyncC37_118_Slave"

// Standard ANSI C headers needed for this program
#include <stdio.h>
#include <stdarg.h>

#if defined(__QNXNTO__)
// For QNX v6.x threads
#include <process.h>
#include <sys/sched.h>
#include <pthread.h>
#include <devctl.h>
#include <sys/dcmd_chr.h>
#elif defined(__linux__)
#define _GNU_SOURCE   1
#include <sched.h>
#if defined(__redhawk__)
#include <cpuset.h>
#include <mpadvise.h>
#endif
#endif
// Define RTLAB before including OpalPrint.h for messages to be sent
// to the OpalDisplay. Otherwise stdout will be used.

#ifndef RTLAB
#define RTLAB
#endif

#include "OpalPrint.h"
#include "OpalGenAsyncParamCtrl.h"
#include "AsyncC37_118_Slave.h"
#include "Opal_C37_118.h"


// This is just for initializing the shared memory access to communicate
// with the RT-LAB model. It's easier to remember the arguments like this
#define ASYNC_SHMEM_NAME argv[1]
#define ASYNC_SHMEM_SIZE atoi(argv[2])
#define PRINT_SHMEM_NAME argv[3]

// Use the smallest possible memory footprint to store the data_out
// and data_in structures.
#pragma pack(1)

// ****** FORMAT TO SPECIFIC PROTOCOL HERE ******************************
//
// Define the structure of the data that we exchange between send/recv threads


struct data_in_out
{  
  int                   dev_id;     
  int                   dev_fnct;     
  int                   dev_protocol;
  int                   phasor_rep; 
  int                   nominal_freq;
  int                   data_rate; 
  int                   timebase;
  int                   ts_input;
  int                   port_local;
  int                   udp_data_port;
  int                   nbr_double_values;
  int                   offset;
  int                   core_nbr;
  char                  ip_addr_local[20];
  char                  channel_name[C37_118_MAX_CHANNEL_NAME_LEN * 4];
  char                  cfg_name[ASYNC_C37_118_MAX_CFG_FILE_NAME_LEN];
  char                  pmu_name[C37_118_MAX_PMU_NAME_LEN * 4];
  pthread_mutex_t       fifo_lock;
  C37_118_FIFO_BUF      fifo_buffer;
  C37_118_STATE         state;
  C37_118_INPUT_DATA    data_buffer[C37_118_BUF_MAX];
  C37_118_INPUT_CFG     inputs_cfg;
  C37_118_SLV_SESSION  *p_session;
};
// **********************************************************************


/************************************************************************/
/* Defines
/************************************************************************/

#define  PMU_HEADER  "This is a simple PMU header."


/************************************************************************/
/* Pragma definitions
/************************************************************************/
#pragma pack()                              


/************************************************************************/
/* Global variables
/************************************************************************/
struct   data_in_out SRStruct;


/************************************************************************/
/* Local threads and functions
/************************************************************************/
        void *async_C37_118_read_model_data    (void         *p_arg);                                                 
        void *async_C37_118_init_session       (void         *p_arg);                                                 
                                
static  int   async_C37_118_get_block_param    (void);
static  int   async_C37_118_get_inputs_param   (char         *argv[]);  		
static  int   async_C37_118_print_inputs_param (void);		
static  int   async_C37_118_validate_model     (void);		
		                                       
static  void  async_C37_118_cfg_print          (void);

static  void  async_C37_118_ext_frm_cb         (void         *p_data,
                                                int           data_len);

static  void  async_C37_118_close_shm          (char         *argv[]);
												
static  void  OpalTrace                        (const char   *format, ...);    

static  int   AssignProcToCpu                  (int cpu);                           
                                                                         

/************************************************************************/
/* Main
/************************************************************************/
int main (int argc, char *argv[]) 
{
    pthread_t                 tid_read;
    pthread_t                 tid_c37_118;
    pthread_attr_t            attr_read;
    pthread_attr_t            attr_c37_118;  
    int                       model_state;
	int                       rc;
	int                       err;
    int                       num_cpu_max;
	volatile C37_118_FIFO_DATA data_store[C37_118_MAX_TX_FIFO_SIZE];		

  
    /* Check for the proper arguments to the program. */ 
    if (argc < 4)
    {
        printf("Invalid Arguments: 1-AsyncShmemName 2-AsyncShmemSize 3-PrintShmemName\n");
        exit(0);
    }
    
    /* Enable the OpalPrint function. This prints to the OpalDisplay. */ 
    if (OpalSystemCtrl_Register(PRINT_SHMEM_NAME) != EOK)
    {
        printf("%s: ERROR: OpalPrint() access not available\n", PROGNAME);
        exit(-1);    
    }
    
    /* Open Share Memory created by the model. */ 
    if((OpalOpenAsyncMem (ASYNC_SHMEM_SIZE, ASYNC_SHMEM_NAME)) != EOK)
    {
        OpalPrint("%s-> ERROR: Model shared memory not available\n", PROGNAME);
        exit(-1);
    }
    /* Get block parameters. */
    rc = async_C37_118_get_block_param();
	if (rc != EOK)
	{
        OpalPrint("%s-> Error while trying to get block parameters -> %d\n", PROGNAME, rc);
		async_C37_118_close_shm(argv);
        exit(-1);	
	}
	
	/* Extract the number of available CPUs. */
    num_cpu_max = sysconf( _SC_NPROCESSORS_ONLN );
	
	if ((SRStruct.core_nbr  < 0)             || \
	     (SRStruct.core_nbr >= num_cpu_max)) {
        OpalPrint("%s [ID #%d] -> Configuration error: invalid core number (%d)\n", SRStruct.pmu_name, SRStruct.dev_id);
        OpalPrint("%s [ID #%d] -> Configuration error: this system has a maximum of %d online cores (from 0 to %d)\n", SRStruct.pmu_name,  SRStruct.dev_id, num_cpu_max, (num_cpu_max -1));		
		async_C37_118_close_shm(argv);
        exit(-1);			 
	}

	/* Assign process to a given CPU order to support partial XHP. */
    AssignProcToCpu(SRStruct.core_nbr); 	   
	 
    /* Get inputs parameters. */
    rc = async_C37_118_get_inputs_param(argv);
	if (rc != EOK)
	{
        OpalPrint("%s [ID #%d] -> Error while trying to get file parameters -> %d\n", SRStruct.pmu_name,  SRStruct.dev_id, rc);
		async_C37_118_close_shm(argv);
        exit(-1);	
	}
	
	/* Validate the model inputs. */
	rc = async_C37_118_validate_model();
	if (rc != EOK)
	{
        OpalPrint("%s [ID #%d] -> Error while validating the model -> %d\n", SRStruct.pmu_name,  SRStruct.dev_id, rc);        
		async_C37_118_close_shm(argv);		
        exit(-1);	
	}
	
	/* Display the configuration parameters. */
    async_C37_118_cfg_print();
	
    /* Print inputs parameters. */
    rc = async_C37_118_print_inputs_param();
	if (rc != EOK)
	{
        OpalPrint("%s [ID #%d] -> Error while printing inputs parameters -> %d\n", SRStruct.pmu_name,  SRStruct.dev_id, rc);
		async_C37_118_close_shm(argv);		
        exit(-1);	
	}
		
	/* Initialize FIFO. */
	C37_118_sfifo_init(&SRStruct.fifo_buffer, &data_store[0], C37_118_MAX_TX_FIFO_SIZE);
	
    /* Initialize lock mutex.  */
    if(pthread_mutex_init(&SRStruct.fifo_lock, NULL) != 0)
	{
        OpalPrint("%s [ID #%d] -> Error while initializing FIFO lock (errno %d)\n", SRStruct.pmu_name,  SRStruct.dev_id, errno);        
		async_C37_118_close_shm(argv);		
        exit(-1);	
    }			
	

    do
    { 	
         usleep(1000);
		 /* Get model state. */
        model_state = OpalGetAsyncModelState();
	} while (model_state == STATE_PAUSE);	

	/* Get model state. */
	model_state = OpalGetAsyncModelState();
	if ((model_state != STATE_RESET) && (model_state != STATE_STOP))
	{            
		/* Start C37.118 session thread. */
		pthread_attr_init (&attr_c37_118);
		if ((pthread_create (&tid_c37_118, &attr_c37_118, async_C37_118_init_session, NULL)) == -1)
		{
			OpalPrint("%s [ID #%d] -> Error while creating session thread (errno %d)\n", SRStruct.pmu_name,  SRStruct.dev_id, errno);
		}  
		
     	/* Start read thread. */
		pthread_attr_init (&attr_read);
		if ((pthread_create (&tid_read, &attr_read, async_C37_118_read_model_data, NULL)) == -1)
		{
			OpalPrint("%s [ID #%d] -> Error while creating shared memory thread (errno %d)\n", SRStruct.pmu_name,  SRStruct.dev_id, errno);
		}            
		
		/* Wait for C37.118 thread to finish. */
		if ((err = pthread_join (tid_c37_118, NULL)) != 0)
		{
			OpalPrint("%s [ID #%d] -> Error while waiting for session thread to finish (errno %d)\n", SRStruct.pmu_name,  SRStruct.dev_id, errno);
		}   	
		
		/* Wait for read thread to finish. */
		if ((err = pthread_join (tid_read, NULL)) != 0)
		{
			OpalPrint("%s [ID #%d] -> Error while waiting for shared memory thread to finish (errno %d)\n", SRStruct.pmu_name,  SRStruct.dev_id, errno);
		}       		    		

	}       
  
	async_C37_118_close_shm(argv);	

    return(0);
}


/* =================================================================================
 * Name:          async_C37_118_read_model_data()
 *
 * Description:   Read the data stored into the asynchronous memory by the model.
 *
 * Argument(s):   p_arg    Pointer to the shared memory structure.
 *
 * Return:        none.
 *
 * Caller(s):     main().
 *
 * Note(s):       none.
 * =================================================================================
 */
void  *async_C37_118_read_model_data (void *p_arg)
{
	int  n;
    int  model_state;		
    int  send_id;
	int  first_second_detected;
	int  epoch_index;
	int  us_index;
    int  saved_sec;
    int  new_sec;
	int item_cnt;
	int fifo_empty;
	unsigned fifo_cnt;
	   
	/* Check the variable to change the thread priority */
	int priority = 98;
	
	/* Raise priority. */
	int policy;
	struct sched_param param;
	pthread_getschedparam(pthread_self(),&policy,& param );
	param.sched_priority = priority;
	policy=SCHED_FIFO;
	pthread_setschedparam(pthread_self(), policy,& param );
	
	first_second_detected = 0;
	us_index = (SRStruct.inputs_cfg.phasor.nbr * 2) +   \
	              (SRStruct.inputs_cfg.analog.nbr)  +   \
	              (SRStruct.inputs_cfg.digital.nbr) +   \
				  2 + SRStruct.offset;
				 
	epoch_index = us_index + 1;
	item_cnt   = 0;
	fifo_empty = 1;
    do
    { 	
        /* Get model state. */
        model_state = OpalGetAsyncModelState();
        if(model_state == STATE_PAUSE)
        {
		    usleep(1000);
            continue;
        }		

        send_id = 0;
		do {
			if((n = OpalWaitForAsyncSendRequest ((unsigned int *)&send_id)) != EOK)
			{
				model_state = OpalGetAsyncModelState();
				if ((model_state != STATE_RESET) && (model_state != STATE_STOP))
				{
					OpalSetAsyncSendIconError(n, send_id);
				} else {
                    return ((void *)0);
				}
			}	
		} while (send_id != SRStruct.dev_id);	
		
		/* Read data from the model and copy data in common structure */    
		saved_sec = SRStruct.data_buffer[epoch_index];
		OpalGetAsyncSendIconData (&SRStruct.data_buffer[0], (SRStruct.nbr_double_values  * sizeof(double)), SRStruct.dev_id);
		
		/* Save second to detect the next second change. */
		new_sec  = SRStruct.data_buffer[epoch_index];		

		if (SRStruct.state == C37_118_STATE_TX_DATA)  {
			if (first_second_detected == 0) {
				
				if (new_sec != saved_sec) {
					//OpalPrint("First second detected -> %d (us = %d)\n", new_sec, SRStruct.data_buffer[us_index]);
					first_second_detected = 1;
				}
			}
			
			if (first_second_detected == 1) {
				pthread_mutex_lock(&SRStruct.fifo_lock);
				C37_118_sfifo_add(SRStruct.p_session, (C37_118_FIFO_DATA *)&SRStruct.data_buffer[0]);
				pthread_mutex_unlock(&SRStruct.fifo_lock);
				item_cnt++;
			}
			
			
		}  else {
			first_second_detected = 0;
			pthread_mutex_lock(&SRStruct.fifo_lock);
			if (!C37_118_sfifo_empty(&SRStruct.fifo_buffer)) {	
				do {
					item_cnt--;
					fifo_empty = C37_118_sfifo_clear(SRStruct.p_session, C37_118_NO);
				} while (fifo_empty != 1);
			}
			pthread_mutex_unlock(&SRStruct.fifo_lock);
		}			
		
		/* Extract number of data in the FIFO. */
		fifo_cnt = C37_118_sfifo_count(&SRStruct.fifo_buffer);		
        OpalSetAsyncSendIconError(fifo_cnt, SRStruct.dev_id);
        
		OpalAsyncSendRequestDone(SRStruct.dev_id);		
		
        /* Before continuing, we make sure that the real-time model ...       */
        /* ... has not been stopped. If it has, we stop the receive thread.   */
        model_state = OpalGetAsyncModelState();
    } while ((model_state != STATE_RESET) && (model_state != STATE_STOP) && (model_state != STATE_ERROR));
  
			   	
    return ((void *)0);
}

/* =================================================================================
 * Name:          async_C37_118_init_session()
 *
 * Description:   Init C37.118 session.
 *
 * Argument(s):   p_arg    Pointer to the shared memory structure.
 *
 * Return:        none.
 *
 * Caller(s):     main().
 *
 * Note(s):       Only one session can be opened by asynchronous process.
 * =================================================================================
 */
void  *async_C37_118_init_session (void *p_arg)
{
    C37_118_SLV_SESSION  session;
	C37_118_DATA_BUF     rx_buf[C37_118_MAX_RX_BUF_LEN];
	C37_118_ERR          err;
    int                  model_state;		
	
	/* Session pointer. */
	SRStruct.p_session = &session;
	
    /* Set C37.118 session parameters. */
	session.cfg.bind_to_device_en = C37_118_ENABLED;
	session.cfg.bind_to_device_en = C37_118_ENABLED;
	session.cfg.keep_alive_en     = C37_118_ENABLED;
	session.cfg.tcp_no_delay_en   = C37_118_ENABLED;
	session.cfg.non_blocking_en   = C37_118_ENABLED;
	
	session.cfg.id                = SRStruct.dev_id;
	session.cfg.nominal_freq      = SRStruct.nominal_freq;
	session.cfg.data_rate         = SRStruct.data_rate;
	session.cfg.timebase          = SRStruct.timebase;	
	session.cfg.port_local        = SRStruct.port_local;	
	session.cfg.udp_data_port     = SRStruct.udp_data_port;	
    session.cfg.protocol          = SRStruct.dev_protocol;
	session.cfg.cfg_cnt           = 1;	
	
	strcpy((char *)&session.cfg.ip_addr_local[0], &SRStruct.ip_addr_local[0]);            
	strcpy((char *)&session.cfg.nic_name[0],      &SRStruct.channel_name[0]);            
	strcpy((char *)&session.cfg.pmu_name[0],      &SRStruct.pmu_name[0]);       
	
	session.p_input     = &SRStruct.inputs_cfg;	                    
	session.p_buf       = &SRStruct.data_buffer[0];
	session.p_fifo      = &SRStruct.fifo_buffer;
	session.p_fifo_lock = &SRStruct.fifo_lock;

	/* Set C37.118 trace parameters:                                                 */
	/*     C37_118_TRACE_LVL_NONE -> No output traces                                */
	/*     C37_118_TRACE_LVL_INFO -> Output useful information                       */
	/*     C37_118_TRACE_LVL_DBG  -> Output debug  information                       */
	/*     C37_118_TRACE_LVL_ALL  -> Output debug  information and message exchanges */
	C37_118_slv_set_trace_level(C37_118_TRACE_LVL_INFO, &err);
	
    /* Initialize C37.118 session. */	
    C37_118_slv_session_init(&session, &err);
	if (err != C37_118_ERR_NONE)
	{
	    OpalPrint("%s [ID #%d] -> Error during C37.118 session initialization: %d\n", SRStruct.pmu_name,  SRStruct.dev_id, err);
		OpalPrint("%s [ID #%d] -> Stopping C37.118 thread\n",                         SRStruct.pmu_name,  SRStruct.dev_id);
		return ((void *)0);
	}

	/* Register extended frame callback .*/
	C37_118_slv_register_cb(&session, async_C37_118_ext_frm_cb, &err);
	if (err != C37_118_ERR_NONE)
	{
	    OpalPrint("%s [ID #%d] -> Error while registering extended frame callback: %d\n", SRStruct.pmu_name,  SRStruct.dev_id, err);
	}
	
	/* Set C37.118 header frame message. */
	C37_118_slv_set_hdr_frame(&session, (C37_118_HDR *)PMU_HEADER, sizeof(PMU_HEADER), &err);
	if (err != C37_118_ERR_NONE)
	{
	    OpalPrint("%s [ID #%d] -> Error while setting C37.118 header frame message: %d\n", SRStruct.pmu_name,  SRStruct.dev_id, err);
	}

    do
    { 	
        /* Get model state. */
        model_state = OpalGetAsyncModelState();
        if(model_state == STATE_PAUSE)
        {
		    usleep(1000);
            continue;
        }		
		
		/* Wait for a connection. */
		SRStruct.state = session.state;
        C37_118_slv_conn_accept(&session, &err);
		if (err == C37_118_ERR_NONE)
	    {		
			do
			{		
				C37_118_slv_session_rx(&session, &rx_buf[0], sizeof(rx_buf), &err);
				SRStruct.state = session.state;
				model_state = OpalGetAsyncModelState();
				usleep(1000);
			} while ((model_state != STATE_RESET) && (model_state != STATE_STOP) && (model_state != STATE_ERROR) && (err != C37_118_ERR_SOCK_CLOSED)); 		    
            C37_118_slv_conn_close(&session, &err);
			SRStruct.state = session.state;
		}

		usleep(1000);
        model_state = OpalGetAsyncModelState();
		SRStruct.state = session.state;
    } while ((model_state != STATE_RESET) && (model_state != STATE_STOP) && (model_state != STATE_ERROR));  		   
 
	C37_118_slv_session_close(&session, &err);
	
    return ((void *)0);
}


/* =================================================================================
 * Name:          async_C37_118_get_block_param()
 *
 * Description:   Get C37.118 block parameters:
 *
 * Argument(s):   none
 *
 * Return:        1, if the initialization is successfull.
 *					   
 *                0, otherwise.
 *
 * Caller(s):     main().
 *
 * Note(s):       none.
 * =================================================================================
 */
static  int  async_C37_118_get_block_param(void)
{
	char tmp_buf[C37_118_MAX_PMU_NAME_LEN * 4];
    Opal_GenAsyncParam_Ctrl   IconCtrlStruct;
	int                       err;

	
	strcpy(&SRStruct.channel_name[0],  ""); 
	strcpy(&SRStruct.ip_addr_local[0], "");
	strcpy(&SRStruct.pmu_name[0], "");
	strcpy(&SRStruct.cfg_name[0], "");
	
    /* Get asynchronous controller parameters. */ 
    memset(&IconCtrlStruct, 0, sizeof(IconCtrlStruct));
    if((err = OpalGetAsyncCtrlParameters(&IconCtrlStruct, sizeof(IconCtrlStruct))) != EOK)
    {
    	OpalPrint("%s-> Error: can not get controller parameters (%d).\n", PROGNAME, err);
    	exit(-1);
    }

	SRStruct.dev_id = (short)IconCtrlStruct.controllerID;	
	
	/* If no, fill the configuration structure with mask parameters. */
	SRStruct.dev_fnct       = (int)IconCtrlStruct.FloatParam[ASYNC_C37_118_PARAM_IX_DEV_FNCT];
	SRStruct.dev_protocol   = (int)IconCtrlStruct.FloatParam[ASYNC_C37_118_PARAM_IX_PROTO];
    SRStruct.data_rate      = (int)IconCtrlStruct.FloatParam[ASYNC_C37_118_PARAM_IX_DATA_RATE];
    SRStruct.timebase       = (int)IconCtrlStruct.FloatParam[ASYNC_C37_118_PARAM_IX_TIMEBASE];
	SRStruct.ts_input       = (int)IconCtrlStruct.FloatParam[ASYNC_C37_118_PARAM_IX_TS_INPUT];	
	SRStruct.port_local     = (int)IconCtrlStruct.FloatParam[ASYNC_C37_118_PARAM_IX_PORT_LOCAL]; 
	SRStruct.udp_data_port  = (int)IconCtrlStruct.FloatParam[ASYNC_C37_118_PARAM_IX_UDP_DATA_PORT]; 
	SRStruct.core_nbr       = (int)IconCtrlStruct.FloatParam[ASYNC_C37_118_PARAM_IX_CORE_NBR]; 
	
	if (strcmp("50 Hz",IconCtrlStruct.StringParam[ASYNC_C37_118_PARAM_IX_NOMINAL_FREQ]) == 0)
	{
	    SRStruct.nominal_freq = C37_118_NOMINAL_FREQ_50;    
	} else if ((strcmp("60 Hz",IconCtrlStruct.StringParam[ASYNC_C37_118_PARAM_IX_NOMINAL_FREQ]) == 0)){
	    SRStruct.nominal_freq = C37_118_NOMINAL_FREQ_60;    
	} else {
        SRStruct.nominal_freq = C37_118_PARAM_UNKNOWN;
    }	
	
	strcpy(&tmp_buf[0],      IconCtrlStruct.StringParam[ASYNC_C37_118_PARAM_IX_PMU_NAME]);	
	strncpy(&SRStruct.pmu_name[0], &tmp_buf[0], C37_118_MAX_PMU_NAME_LEN -1);
	strcat(&SRStruct.pmu_name[0], "\0");
	
	strcpy(&SRStruct.cfg_name[0],      IconCtrlStruct.StringParam[ASYNC_C37_118_PARAM_IX_CFG_NAME]); 	
	strcpy(&SRStruct.ip_addr_local[0], IconCtrlStruct.StringParam[ASYNC_C37_118_PARAM_IX_IP_ADDR_LOCAL]);
    strcpy(&SRStruct.channel_name[0],  IconCtrlStruct.StringParam[ASYNC_C37_118_PARAM_IX_NIC_NAME]);
						
	return (EOK);
}


/* =================================================================================
 * Name:          async_C37_118_get_file_param()
 *
 * Description:   Get and validate the input file parameters.
 *
 * Argument(s):   none
 *
 * Return:        EOK, if the operation is successfull.
 *					   
 *                0,   otherwise.
 *
 * Caller(s):     main().
 *
 * Note(s):       none
 * =================================================================================
 */
static  int  async_C37_118_get_inputs_param(char *argv[])
{
    FILE         *p_file;
	C37_118_ERR   err;
	

	p_file = fopen(SRStruct.cfg_name, "r");
	if (p_file == (FILE *)0)
	{
	    OpalTrace("%s [ID #%d] -> %s not found.\n", PROGNAME, SRStruct.channel_name, SRStruct.cfg_name);
	    return(-1);	
	}
	
	C37_118_slv_get_input_cfg(p_file, &SRStruct.inputs_cfg, &err);
	fclose(p_file);
	
	if ((err == C37_118_ERR_LICENSE_NOT_FOUND) || \
	    (err == C37_118_ERR_LICENSE_INIT))
	{  
	     OpalPrint("%s [ID #%d] -> Error: C37.118 slave block can not be used without a valid license for this feature.\n",  SRStruct.pmu_name,  SRStruct.dev_id);
		 async_C37_118_close_shm(argv);
	     exit(-1);
	}

	if (err != C37_118_ERR_NONE)
	{
	    OpalPrint("%s [ID #%d] -> Error: configuration file does not match the requirements\n",  SRStruct.pmu_name,  SRStruct.dev_id);	
		return(-1);
	}	
	
    return (EOK);
}

/* =================================================================================
 * Name:          async_C37_118_print_inputs_param()
 *
 * Description:   Print C37.118 inputs configuration.
 *
 * Argument(s):   none
 *
 * Return:        EOK, if the operation is successfull.
 *					   
 *                0,   otherwise.
 *
 * Caller(s):     main().
 *
 * Note(s):       none
 * =================================================================================
 */
static  int  async_C37_118_print_inputs_param(void)
{
	C37_118_ERR   err;	

	
	C37_118_slv_print_input_cfg(&SRStruct.inputs_cfg, &err);	
	if (err != C37_118_ERR_NONE)
	{
		return(-1);
	}	
	
    return (EOK);
}


/* =================================================================================
 * Name:          async_C37_118_validate_model()
 *
 * Description:   Validate model connections.
 *
 * Argument(s):   none.
 *
 * Return:        none.
 *
 * Caller(s):     main().
 *
 * Note(s):       none.
 * =================================================================================
 */
 static  int  async_C37_118_validate_model(void)
 {
	int  file_data_size;
	int  mdldata_send_size;
	int  nbr_send_icon;
	
    /* Get send block input width. */
	OpalGetAsyncSendIconDataLength (&mdldata_send_size,   SRStruct.dev_id);
	SRStruct.nbr_double_values = mdldata_send_size/sizeof(double);
	
	file_data_size = (SRStruct.inputs_cfg.phasor.nbr * 2) + \
	                  SRStruct.inputs_cfg.analog.nbr      + \
	                  SRStruct.inputs_cfg.digital.nbr     + 5; /* 2 frequency + 3 timestamp inputs. */
	
	SRStruct.offset = 0;
	if (SRStruct.inputs_cfg.phasor.nbr == 0)
		SRStruct.offset++;
		
	if(SRStruct.inputs_cfg.analog.nbr == 0)
		SRStruct.offset++;
		
	if(SRStruct.inputs_cfg.digital.nbr == 0)
		SRStruct.offset++;
	
	if ((SRStruct.nbr_double_values - SRStruct.offset) != file_data_size) {
	    OpalPrint("%s [ID #%d] -> Invalid configuration\n", SRStruct.pmu_name, SRStruct.dev_id);
		OpalPrint("%s [ID #%d] -> According to the %s configuration file, the block must have the following signal connected: \n", SRStruct.pmu_name, SRStruct.dev_id, SRStruct.cfg_name);
		OpalPrint("%s [ID #%d] -> \t %d phasor signals (%d magnitude(s) and %d angle(s))\n", SRStruct.pmu_name, SRStruct.dev_id, (SRStruct.inputs_cfg.phasor.nbr * 2), SRStruct.inputs_cfg.phasor.nbr, SRStruct.inputs_cfg.phasor.nbr);
		OpalPrint("%s [ID #%d] -> \t %d analog signals \n", SRStruct.pmu_name, SRStruct.dev_id, SRStruct.inputs_cfg.analog.nbr);
		OpalPrint("%s [ID #%d] -> \t %d digital signals \n", SRStruct.pmu_name, SRStruct.dev_id, SRStruct.inputs_cfg.digital.nbr);
		OpalPrint("%s [ID #%d] -> \t 1 frequency deviation from nominal signal(fixed number) \n", SRStruct.pmu_name, SRStruct.dev_id);
		OpalPrint("%s [ID #%d] -> \t 1 frequency rate of change signal(fixed number) \n", SRStruct.pmu_name, SRStruct.dev_id);
		OpalPrint("%s [ID #%d] -> \t 3 timestamp signals (sync,  epoch time and microseconds)\n", SRStruct.pmu_name, SRStruct.dev_id);
	    OpalPrint("%s [ID #%d] -> For a total of %d signals. Actually, %d signals are connected to the block.\n", SRStruct.pmu_name, SRStruct.dev_id, file_data_size, SRStruct.nbr_double_values);
		OpalPrint("%s [ID #%d] -> C37.118 process will not be started\n", SRStruct.pmu_name, SRStruct.dev_id);

		return(-1);	
	}
	
	if (SRStruct.inputs_cfg.analog.nbr > C37_118_ANALOG_DATA_NBR_MAX) {
	    OpalPrint("%s [ID #%d] -> Invalid configuration\n", SRStruct.pmu_name, SRStruct.dev_id);
	    OpalPrint("%s [ID #%d] -> Maximum number of phasors to transmit is %d (%d magnitude(s) and %d angle(s))\n", SRStruct.pmu_name, SRStruct.dev_id, C37_118_MAX_PHASOR_NBR, C37_118_MAX_PHASOR_NBR, C37_118_MAX_PHASOR_NBR);		
	    OpalPrint("%s [ID #%d] -> C37.118 process will not be started\n", SRStruct.pmu_name, SRStruct.dev_id);
		return(-1);		
	}
	
	if (SRStruct.inputs_cfg.analog.nbr > C37_118_ANALOG_DATA_NBR_MAX) {
	    OpalPrint("%s [ID #%d] -> Invalid configuration\n", SRStruct.pmu_name, SRStruct.dev_id);
	    OpalPrint("%s [ID #%d] -> Maximum number of analog values to transmit is %d\n", SRStruct.pmu_name, SRStruct.dev_id, C37_118_MAX_ANALOG_NBR);		
	    OpalPrint("%s [ID #%d] -> C37.118 process will not be started\n", SRStruct.pmu_name, SRStruct.dev_id);
		return(-1);		
	}
	
	if (SRStruct.inputs_cfg.analog.nbr > C37_118_DIGITAL_DATA_NBR_MAX) {
	    OpalPrint("%s [ID #%d] -> Invalid configuration\n", SRStruct.pmu_name, SRStruct.dev_id);
	    OpalPrint("%s [ID #%d] -> Maximum number of digital values to transmit is %d\n", SRStruct.pmu_name, SRStruct.dev_id, C37_118_MAX_DIGITAL_NBR);
	    OpalPrint("%s [ID #%d] -> C37.118 process will not be started\n", SRStruct.pmu_name, SRStruct.dev_id);
		return(-1);		
	}	
	

    OpalGetNbAsyncSendIcon(&nbr_send_icon);	
    if(nbr_send_icon != 1)
    {
	    OpalPrint("%s [ID #%d] -> Invalid number of Asynchronous Send blocks detected in the OpC37_118_AsyncSlaveCtrl block. %d block is required.\n", SRStruct.pmu_name, SRStruct.dev_id, ASYNC_C37_118_NBR_SEND_BLOCK);
	    OpalPrint("%s [ID #%d] -> C37.118 process will not be started\n", SRStruct.pmu_name, SRStruct.dev_id);

		return(-1);
    }	

    return(EOK);
 }

/* =================================================================================
 * Name:          async_C37_118_cfg_print()
 *
 * Description:   Print the C37_118 block configuration.                 
 *
 * Argument(s):   none.  
 *
 * Return:        none.
 *
 * Caller(s):     main().
 *
 * Note(s):       none.
 * =================================================================================
 */
 static  void  async_C37_118_cfg_print(void)
{
    OpalTrace("\n----------------------------------------------------------------\n");
    OpalTrace("Listing C37.118 block parameters:\n");
    
    OpalTrace("----------------------------------------------------------------\n");
    if (SRStruct.dev_fnct == ASYNC_C37_118_DEV_FNCT_SLAVE)
    {
       OpalTrace("%s [ID #%d] -> Device function:          Slave\n",  SRStruct.pmu_name, SRStruct.dev_id);
    } else {
       OpalTrace("%s [ID #%d] -> Device function:          Master\n", SRStruct.pmu_name, SRStruct.dev_id);
    }
	
	OpalTrace("%s [ID #%d] -> Core number               %d\n", SRStruct.pmu_name, SRStruct.dev_id, SRStruct.core_nbr);
    
    if (SRStruct.dev_protocol == C37_118_COMM_PROTOCOL_TCP)
    {
       OpalTrace("%s [ID #%d] -> Protocol:                 TCP\n", SRStruct.pmu_name, SRStruct.dev_id);
    } else if  (SRStruct.dev_protocol == C37_118_COMM_PROTOCOL_UDP){
       OpalTrace("%s [ID #%d] -> Protocol:                 UDP\n", SRStruct.pmu_name, SRStruct.dev_id);
	} else {
       OpalTrace("%s [ID #%d] -> Protocol:                 TCP/UDP\n", SRStruct.pmu_name, SRStruct.dev_id);
	   OpalTrace("%s [ID #%d] -> UDP data port:            %d\n",      SRStruct.pmu_name, SRStruct.dev_id, SRStruct.udp_data_port);
    }  				
	
   
	/* Display asynchronous process parameters. */ 
 	OpalTrace("%s [ID #%d] -> Inputs config file:       %s\n", SRStruct.pmu_name, SRStruct.dev_id, SRStruct.cfg_name);  
    OpalTrace("%s [ID #%d] -> Channel name:             %s\n", SRStruct.pmu_name, SRStruct.dev_id, SRStruct.channel_name);
    OpalTrace("%s [ID #%d] -> Local IP addr:            %s\n", SRStruct.pmu_name, SRStruct.dev_id, SRStruct.ip_addr_local);
	

    if (SRStruct.dev_protocol == C37_118_COMM_PROTOCOL_TCP)
    {
           OpalTrace("%s [ID #%d] -> Local TCP port:           %d\n", SRStruct.pmu_name, SRStruct.dev_id, SRStruct.port_local); 
    } else if  (SRStruct.dev_protocol == C37_118_COMM_PROTOCOL_UDP){
           OpalTrace("%s [ID #%d] -> Local UDP port:           %d\n", SRStruct.pmu_name, SRStruct.dev_id, SRStruct.port_local); 
	} else {
           OpalTrace("%s [ID #%d] -> Local UDP port:           %d\n", SRStruct.pmu_name, SRStruct.dev_id, SRStruct.port_local); 
    }  		
  
    if (SRStruct.nominal_freq == C37_118_NOMINAL_FREQ_50)
    {
        OpalTrace("%s [ID #%d] -> Nominal frequency:        50 Hz\n", SRStruct.pmu_name, SRStruct.dev_id);
    } else {
        OpalTrace("%s [ID #%d] -> Nominal frequency:        60 Hz\n", SRStruct.pmu_name, SRStruct.dev_id);
    }  	
	
	OpalTrace("%s [ID #%d] -> Reporting data rate:      %d Hz\n", SRStruct.pmu_name, SRStruct.dev_id, SRStruct.data_rate);
	OpalTrace("%s [ID #%d] -> Timebase:                 %d   \n", SRStruct.pmu_name, SRStruct.dev_id, SRStruct.timebase);
	
    if (SRStruct.ts_input == 0)
    {
        OpalTrace("%s [ID #%d] -> Timestamp input:          Disabled\n", SRStruct.pmu_name, SRStruct.dev_id);
    } else {
        OpalTrace("%s [ID #%d] -> Timestamp input:          Enabled\n", SRStruct.pmu_name, SRStruct.dev_id);
    }  		
	
    OpalTrace("----------------------------------------------------------------\n");	
 } 
 
 
/* =================================================================================
 * Name:          async_C37_118_ext_frm_cb()
 *
 * Description:   Register the extended frame command callback               
 *
 * Argument(s):   p_data     Pointer to the received extended data.
 *
 *                data_len   Length of the received data.
 *
 * Return:        none.
 *
 * Caller(s):     C37.118 library.
 *
 * Note(s):       This function will be called when the PMU will receive a valid
 *                extended frame. It is the user responsibility to read the
 *                frame and take an action depending on the received data. 
 * =================================================================================
 */
static  void  async_C37_118_ext_frm_cb (void  *p_data, int data_len)
{
    C37_118_DATA_BUF  *p_ext_data; 		
	
	
	p_ext_data = (C37_118_DATA_BUF *)p_data;
	
    OpalTrace("%s [ID #%d] -> Received %d bytes of extended data\n", SRStruct.pmu_name, SRStruct.dev_id, data_len);
	OpalTrace("%s [ID #%d] -> Extended data: %s\n", SRStruct.pmu_name, SRStruct.dev_id, p_ext_data);
}
 
 
/* =================================================================================
 * Name:          async_C37_118_close_shm()
 *
 * Description:   Close shared memory.           
 *
 * Argument(s):   none.
 *
 * Return:        none.
 *
 * Caller(s):     main().
 *
 * Note(s):       none.
 * =================================================================================
 */
static  void  async_C37_118_close_shm (char *argv[])
{
    /* Close the shared memories */
    OpalCloseAsyncMem (ASYNC_SHMEM_SIZE,ASYNC_SHMEM_NAME);
    OpalSystemCtrl_UnRegister(PRINT_SHMEM_NAME);	
}


/* =================================================================================
 * Name:           OpalTrace()
 *
 * Description:    Wrapper to give the possibility to the application to disable
 *                 its own diagnostic messages using a macro configuration. 
 *
 * Argument(s):    format   Pointer to string to display.
 *
 *                 ...      Arguments to convert into integers, strings, etc.
 *
 * Return:         none.
 *
 * Caller(s):      Various.
 *
 * Note(s):        none.
 * =================================================================================
 */
static  void  OpalTrace(const char *format, ...)
{
    va_list  arglist;
    char	 tmp_buf[512];

	
	va_start(arglist, format);
	vsprintf(tmp_buf, format, arglist);
	va_end(arglist);
	OpalPrint("%s", tmp_buf);
}


/* =================================================================================
 * Name:           AssignProcToCpu()
 *
 * Description:    Assign asynchronous process to a given CPU.
 *
 * Argument(s):    none
 *
 * Return:         EOK,   if successful,
 *                 errno, otherwise.
 *
 * Caller(s):      main().
 *
 * Note(s):        none.
 * =================================================================================
 */
static  int AssignProcToCpu(int cpu)
{
#if defined(__linux__)
	char      *p_env_var;
		
 	if((p_env_var = getenv("OPAL_C37_118_ASSIGN_TO_CPU")) != NULL)
	{
		/* If environment variable value is valid, change the number of loops. */
		if((strcmp(p_env_var,  "-1") != 0) && \
		   (strcmp(p_env_var,  "")   != 0))
		{
		    cpu = atoi(p_env_var);
		}   
	}

#	if defined(__redhawk__)
	int				rc;
	pid_t			pid = getpid();
	cpuset_t		*pCpuset;

	pCpuset = cpuset_alloc();
	if (NULL == pCpuset)
	{
		fprintf(stderr, "Error allocating a cpuset\n");
		return(ENOMEM);
	}
	cpuset_init(pCpuset);
	cpuset_set_cpu(pCpuset, cpu, 1);
	rc = mpadvise(MPA_PRC_SETBIAS, MPA_TID, pid, pCpuset);
	if (MPA_FAILURE == rc)
	{
		rc = errno;
		fprintf(stderr, "Error from mpadvise, %d %s, for pid %d\n", errno, strerror(errno), pid);
		cpuset_free(pCpuset);
		return(rc);
	}
	cpuset_free(pCpuset);
	return EOK;
#	else
	cpu_set_t bindSet;	
	
	CPU_ZERO(&bindSet);
	CPU_SET(cpu, &bindSet);
	
	/* Changing process cpu affinity. */
	if (sched_setaffinity( 0, sizeof(cpu_set_t), &bindSet ) != 0)
	{
		OpalPrint("Unable to bind the process to cpu #%d. sched_setaffinity() returned with errno %d\n", cpu, errno);
		return EINVAL;
	}
	return EOK;
#	endif
#endif	// __linux__
}
#endif
