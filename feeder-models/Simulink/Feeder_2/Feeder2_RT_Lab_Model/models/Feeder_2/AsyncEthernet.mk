# ----------------------------------------------------------------------------#
# Specify program name
PROGRAM = AsyncEthernet


# ----------------------------------------------------------------------------#
# Specify default values if we are not compiling from RT-LAB
#
# ----------------------------------------------------------------------------#
TARGET_OPALRT_ROOT ?= /usr/opalrt
RTLAB_ROOT = $(TARGET_OPALRT_ROOT)

# ----------------------------------------------------------------------------#
# QNX v6.x
#
ifeq "$(SYSNAME)" "nto"

	CC = gcc
	LD = $(CC)
	TARGET_LIB =  -lsocket

endif
# ----------------------------------------------------------------------------#

# ----------------------------------------------------------------------------#
# RedHawk Linux
#
ifeq "$(shell uname)" "Linux"

	RTLAB_INTEL_COMPILER ?= 1
	# Intel Compiler support
	ifeq ($(RTLAB_INTEL_COMPILER),1)
		CC = opicc
		LD = opicpc
	# Gnu Compiler support
	else
		CC = gcc
		LD = g++
		INTEL_LIBS = -limf -lirc
	endif

	# RedHat or RedHawk
	LINUX_FLAVOR = $(shell uname -r | grep RedHawk)
	ifneq "$(LINUX_FLAVOR) " " " ### Linux (RedHat)
		RH_FLAGS = -D_GNU_SOURCE -D__redhawk__
		RH_LIBS = -lccur_rt
	else
		RH_FLAGS = -D_GNU_SOURCE
	endif

	TARGET_LIB = -lpthread -lm -ldl -lutil -lrt $(RH_LIBS) $(INTEL_LIBS)

endif
# ----------------------------------------------------------------------------#

# Support for debugging symbols
ifeq ($(DEBUG),1)
	CC_DEBUG_OPTS=-g -D_DEBUG
	LD_DEBUG_OPTS=-g
else
	CC_DEBUG_OPTS=-O
	LD_DEBUG_OPTS=
endif


INCLUDES = -I. -I$(RTLAB_ROOT)/common/include_target
LIBPATH  = -L. -L$(RTLAB_ROOT)/common/lib $(OPAL_LIBPATH)
CC_OPTS =
LD_OPTS = 
OBJS = ${PROGRAM}.o DBusConfig.o

ADDLIB = -lOpalCore -lOpalUtils -llicenseRH32
LIBS   = -lOpalAsyncApiCore $(ADDLIB) $(TARGET_LIB) $(OPAL_LIBS)

CFLAGS  = -c $(CC_OPTS) $(CC_DEBUG_OPTS) $(RH_FLAGS) $(INCLUDES)
LDFLAGS = $(LD_OPTS) $(LD_DEBUG_OPTS) $(LIBPATH)

all: $(PROGRAM)

install:
	\mkdir -p $(TARGET_OPALRT_ROOT)/local
	\chmod 755 $(TARGET_OPALRT_ROOT)/local
	\cp -f $(PROGRAM) $(TARGET_OPALRT_ROOT)/local

clean:
	\rm -f $(OBJS) $(PROGRAM)

$(PROGRAM): $(OBJS)
	$(LD) $(LDFLAGS) -o $@ $(OBJS) $(LIBS) $(LIBS)
	chmod 777 $@
	@echo "### Created executable: $(PROGRAM)"
