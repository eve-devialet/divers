/*!
 * \file sample-static.c
 *
 * \author FTDI
 * \date 20110512
 *
 * Copyright � 2000-2014 Future Technology Devices International Limited
 *
 *
 * THIS SOFTWARE IS PROVIDED BY FUTURE TECHNOLOGY DEVICES INTERNATIONAL LIMITED ``AS IS'' AND ANY EXPRESS
 * OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL FUTURE TECHNOLOGY DEVICES INTERNATIONAL LIMITED
 * BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
 * THE POSSIBILITY OF SUCH DAMAGE.
 *
 * Project: libMPSSE
 * Module: I2C Sample Application - Interfacing 24LC024H I2C EEPROM
 *
 * Rivision History:
 * 0.1 - 20110513 - initial version
 * 0.2 - 20110801 - Changed LatencyTimer to 255
 * 				  Attempt to open channel only if available
 *				  Added & modified macros
 *                		  Change I2C_GetChannelInfo & OpenChannel to start indexing from 0
 * 0.3 - 20111212 - Added comments
 */

/******************************************************************************/
/* 							 Include files										   */
/******************************************************************************/
/* Standard C libraries */
#include<stdio.h>
#include<stdlib.h>
/* OS specific libraries */
#ifdef _WIN32
#include<windows.h>
#endif

/* Include D2XX header*/
#include "ftd2xx.h"

/* Include libMPSSE header */
#include "libMPSSE_i2c.h"

/******************************************************************************/
/*								Macro and type defines							   */
/******************************************************************************/
/* Helper macros */

#define APP_CHECK_STATUS(exp) {if(exp!=FT_OK){printf("%s:%d:%s(): status(0x%x) \
!= FT_OK\n",__FILE__, __LINE__, __FUNCTION__,exp);exit(1);}else{;}};
#define CHECK_NULL(exp){if(exp==NULL){printf("%s:%d:%s():  NULL expression \
encountered \n",__FILE__, __LINE__, __FUNCTION__);exit(1);}else{;}};

/* Application specific macro definations */
#define I2C_DEVICE_ADDRESS_EEPROM		0x57
#define I2C_DEVICE_BUFFER_SIZE		256
#define I2C_WRITE_COMPLETION_RETRY		10
#define START_ADDRESS_EEPROM 	0x00 /*read/write start address inside the EEPROM*/
#define END_ADDRESS_EEPROM		0x10


#define RETRY_COUNT_EEPROM		10	/* number of retries if read/write fails */
#define CHANNEL_TO_OPEN			0	/*0 for first available channel, 1 for next... */
//#define DATA_OFFSET				1
#define DATA_OFFSET				5

/******************************************************************************/
/*								MCP45 defines   							   */
/******************************************************************************/
/* MCP45 commands */
#define MCP45_WRITE_DATA        0x00
#define MCP45_INCREMENT         0x01
#define MCP45_DECREMENT         0x02
#define MCP45_READ_DATA         0x03

/* MCP45 registers addresses */
#define MCP45_ADDR_WIPER0       0x00
#define MCP45_ADDR_TCON         0x04

/* MCP45 TCON BITS*/
/*R0B 1: P0B pin connected to resistor network, 0: disconnected*/
#define MCP45_TCON_R0B_MASK     0x01
/*R0W 1: P0W pin connected to resistor network, 0: disconnected*/
#define MCP45_TCON_R0W_MASK     0x02
/*R0A 1: P0A pin connected to resistor network, 0: disconnected*/
#define MCP45_TCON_R0A_MASK     0x04
/*R0HW 0: Resistor 0 forced to hardware pin shutdown, 1: not forced*/
#define MCP45_TCON_ROHW_MASK    0x08


/******************************************************************************/
/*								Global variables							  	    */
/******************************************************************************/
uint32 channels;
FT_HANDLE ftHandle;
ChannelConfig channelConf;
FT_STATUS status;
uint8 buffer[I2C_DEVICE_BUFFER_SIZE];

/******************************************************************************/
/*						Public function definitions						  		   */
/******************************************************************************/
/*!
 * \brief Writes to EEPROM
 *
 * This function writes a byte to a specified address within the 24LC024H EEPROM
 *
 * \param[in] slaveAddress Address of the I2C slave (EEPROM)
 * \param[in] registerAddress Address of the memory location inside the slave to where the byte
 *			is to be written
 * \param[in] data The byte that is to be written
 * \return Returns status code of type FT_STATUS(see D2XX Programmer's Guide)
 * \sa Datasheet of 24LC024H http://ww1.microchip.com/downloads/en/devicedoc/22102a.pdf
 * \note
 * \warning
 */
FT_STATUS write_byte(uint8 slaveAddress, uint8 registerAddress, uint8 data)
{
	uint32 bytesToTransfer = 0;
	uint32 bytesTransfered;
	bool writeComplete=0;
	uint32 retry=0;

	bytesToTransfer=0;
	bytesTransfered=0;
	buffer[bytesToTransfer++]=registerAddress; /* Byte addressed inside EEPROM */
	buffer[bytesToTransfer++]=data;
	status = I2C_DeviceWrite(ftHandle, slaveAddress, bytesToTransfer, buffer, \
&bytesTransfered, I2C_TRANSFER_OPTIONS_START_BIT|I2C_TRANSFER_OPTIONS_STOP_BIT);

	/* poll to check completition */
	while((writeComplete==0) && (retry<I2C_WRITE_COMPLETION_RETRY))
	{
		bytesToTransfer=0;
		bytesTransfered=0;
		buffer[bytesToTransfer++]=registerAddress; /* Addressed inside EEPROM  */
		status = I2C_DeviceWrite(ftHandle, slaveAddress, bytesToTransfer,\
			buffer, &bytesTransfered, \
			I2C_TRANSFER_OPTIONS_START_BIT|I2C_TRANSFER_OPTIONS_BREAK_ON_NACK);
		if((FT_OK == status) && (bytesToTransfer == bytesTransfered))
		{
			writeComplete=1;
			printf("  ... Write done\n");
		}
		retry++;
		//printf("Retry=%d\n",retry);
	}
	return status;
}

/*!
 * \brief Reads from EEPROM
 *
 * This function reads a byte from a specified address within the 24LC024H EEPROM
 *
 * \param[in] slaveAddress Address of the I2C slave (EEPROM)
 * \param[in] registerAddress Address of the memory location inside the slave from where the
 *			byte is to be read
 * \param[in] *data Address to where the byte is to be read
 * \return Returns status code of type FT_STATUS(see D2XX Programmer's Guide)
 * \sa Datasheet of 24LC024H http://ww1.microchip.com/downloads/en/devicedoc/22102a.pdf
 * \note
 * \warning
 */
FT_STATUS read_byte(uint8 slaveAddress, uint8 registerAddress, uint8 *data)
{
	FT_STATUS status;
	uint32 bytesToTransfer = 0;
	uint32 bytesTransfered;

	bytesToTransfer=0;
	bytesTransfered=0;
	buffer[bytesToTransfer++]=registerAddress; /*Byte addressed inside EEPROM */
	status = I2C_DeviceWrite(ftHandle, slaveAddress, bytesToTransfer, buffer, \
		&bytesTransfered, I2C_TRANSFER_OPTIONS_START_BIT);
	APP_CHECK_STATUS(status);
	bytesToTransfer=1;
	bytesTransfered=0;
	status |= I2C_DeviceRead(ftHandle, slaveAddress, bytesToTransfer, buffer, \
		&bytesTransfered, I2C_TRANSFER_OPTIONS_START_BIT);
	APP_CHECK_STATUS(status);
	*data = buffer[0];
	return status;
}

FT_STATUS MCP45_read_wiper(uint8 slaveAddress, uint8 *value)
{
    FT_STATUS status;
    uint8 memAddress;

    memAddress = (MCP45_READ_DATA << 2) + (MCP45_ADDR_WIPER0 << 4);
    status = read_byte(slaveAddress, memAddress, value);

    return status;
}

FT_STATUS MCP45_read_tcon(uint8 slaveAddress, uint8 *value)
{
    FT_STATUS status;
    uint8 memAddress;

    memAddress = (MCP45_READ_DATA << 2) + (MCP45_ADDR_TCON << 4);
    status = read_byte(slaveAddress, memAddress, value);

    return status;
}

FT_STATUS MCP45_write_wiper(uint8 slaveAddress, uint8 value)
{
    FT_STATUS status;
    uint8 memAddress;

    memAddress = (MCP45_WRITE_DATA << 2) + (MCP45_ADDR_WIPER0 << 4);
    status = write_byte(slaveAddress, memAddress, value);

    return status;
}

FT_STATUS MCP45_increment_wiper(uint8 slaveAddress)
{
    FT_STATUS status;
    uint8 memAddress;
    uint8 value;

    memAddress = (MCP45_INCREMENT << 2) + (MCP45_ADDR_WIPER0 << 4);
    value = (MCP45_INCREMENT << 2) + (MCP45_ADDR_WIPER0 << 4);
    status = write_byte(slaveAddress, memAddress, value);

    return status;
}

FT_STATUS MCP45_decrement_wiper(uint8 slaveAddress)
{
    FT_STATUS status;
    uint8 memAddress;
    uint8 value;

    memAddress = (MCP45_DECREMENT << 2) + (MCP45_ADDR_WIPER0 << 4);
    value = (MCP45_INCREMENT << 2) + (MCP45_ADDR_WIPER0 << 4);
    status = write_byte(slaveAddress, memAddress, value);

    return status;
}
/*
 * \brief Main function / Entry point to the sample application
 *
 * This function is the entry point to the sample application. It opens the channel, writes to the
 * EEPROM and reads back.
 *
 * \param[in] none
 * \return Returns 0 for success
 * \sa
 * \note
 * \warning
 */
int main()
{
	FT_STATUS status;
	FT_DEVICE_LIST_INFO_NODE devList;
	uint8 address;
	uint8 data;
	int i,j;

#ifdef _MSC_VER
	Init_libMPSSE();
#endif
	//channelConf.ClockRate = I2C_CLOCK_FAST_MODE;/*i.e. 400000 KHz*/
	//channelConf.ClockRate = I2C_CLOCK_STANDARD_MODE; /*i.e. 100000 KHz*/
	//channelConf.ClockRate = 20000; /*for test only*/
	channelConf.ClockRate = 2000; /*for test only*/
	channelConf.LatencyTimer= 255;
	//channelConf.Options = I2C_DISABLE_3PHASE_CLOCKING;
	channelConf.Options = I2C_ENABLE_DRIVE_ONLY_ZERO;
	//channelConf.Options = I2C_DISABLE_3PHASE_CLOCKING | I2C_ENABLE_DRIVE_ONLY_ZERO;

	status = I2C_GetNumChannels(&channels);
	APP_CHECK_STATUS(status);
	printf("Number of available I2C channels = %d\n",channels);

	if(channels>0)
	{
		for(i=0;i<channels;i++)
		{
			status = I2C_GetChannelInfo(i,&devList);
			APP_CHECK_STATUS(status);
			printf("Information on channel number %d:\n",i);
			/*print the dev info*/
			printf("		Flags=0x%x\n",devList.Flags);
			printf("		Type=0x%x\n",devList.Type);
			printf("		ID=0x%x\n",devList.ID);
			printf("		LocId=0x%x\n",devList.LocId);
			printf("		SerialNumber=%s\n",devList.SerialNumber);
			printf("		Description=%s\n",devList.Description);
			printf("		ftHandle=0x%x\n",(int)devList.ftHandle);/*is 0 unless open*/
		}

		/* Open the first available channel */
		status = I2C_OpenChannel(CHANNEL_TO_OPEN,&ftHandle);
		APP_CHECK_STATUS(status);
		printf("\nhandle=0x%x status=%d\n",(int)ftHandle,status);
		status = I2C_InitChannel(ftHandle,&channelConf);
		APP_CHECK_STATUS(status);

#if 1
        address = 0;
        status = MCP45_read_wiper(address, &data);
		APP_CHECK_STATUS(status);
        printf("Data read on wiper=0x%x\n", data);

        data = 0x05;
        status = MCP45_write_wiper(address, &data);
		APP_CHECK_STATUS(status);
        printf("Data written on wiper=0x%x\n", data);

        status = MCP45_read_wiper(address, &data);
		APP_CHECK_STATUS(status);
        printf("Data read on wiper=0x%x\n", data);

        status = MCP45_increment_wiper(address);
		APP_CHECK_STATUS(status);
        printf("Data incremented\n");

        status = MCP45_read_wiper(address, &data);
		APP_CHECK_STATUS(status);
        printf("Data read on wiper=0x%x\n", data);

        status = MCP45_read_tcon(address, &data);
		APP_CHECK_STATUS(status);
        printf("Data read on tcon=0x%x\n", data);

#endif
#if 0
		buffer[0]=0x00;
		buffer[1]=0x00;

		status = I2C_DeviceRead(ftHandle, I2C_DEVICE_ADDRESS_EEPROM, 1, buffer, \
		&channels, I2C_TRANSFER_OPTIONS_START_BIT|I2C_TRANSFER_OPTIONS_STOP_BIT|I2C_TRANSFER_OPTIONS_NACK_LAST_BYTE);
		printf("read data = 0x%x\n",buffer[0]);
		APP_CHECK_STATUS(status);

		status = I2C_CloseChannel(ftHandle);
#endif
#if 0

		for(address=START_ADDRESS_EEPROM;address<END_ADDRESS_EEPROM;address++)
		{
			printf("writing address = %d data = %d", address, \
				address+DATA_OFFSET);
			status = write_byte(I2C_DEVICE_ADDRESS_EEPROM, address, \
				address+DATA_OFFSET);
			for(j=0; ((j<RETRY_COUNT_EEPROM) && (FT_OK !=status)); j++)
			{
				printf("---- writing again to address = %d, data =%d\n", \
					address, address+DATA_OFFSET);
				status = write_byte(I2C_DEVICE_ADDRESS_EEPROM, address, \
					address+DATA_OFFSET);
			}
			APP_CHECK_STATUS(status);
		}
		printf("\n");
		for(address=START_ADDRESS_EEPROM; address<END_ADDRESS_EEPROM; address++)
		{
			status = read_byte(I2C_DEVICE_ADDRESS_EEPROM,address, &data);
			for(j=0; ((j<RETRY_COUNT_EEPROM) && (FT_OK !=status)); j++)
			{
				printf("read error... retrying \n");
				status = read_byte(I2C_DEVICE_ADDRESS_EEPROM,address, &data);
			}
			printf("reading address %d data read=%d\n",address,data);
		}
		status = I2C_CloseChannel(ftHandle);
#endif
	}

#ifdef _MSC_VER
	Cleanup_libMPSSE();
#endif

	return 0;
}
