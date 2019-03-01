#!/usr/bin/env python3
from tas5825m_header import *
import subprocess as sp
import logging
import time
logger = logging.getLogger(__name__)

def i2c_read_reg(device=0x4c, register=0x2e, mode='b'):
    cmd = "sudo i2cget -y 1 0x{:02x} 0x{:02x} {}".format(device, register, mode)
    logger.debug(cmd)
    pop = sp.Popen(cmd.split(" "), stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = pop.communicate()
    if pop.returncode == 0:
        return(stdout)
    else:
        raise IOError("No I2C communication")

def i2c_write_reg(device=0x4c, register=0x2e, value="0x00", mode='b'):
    cmd = "sudo i2cset -y 1 0x{:02x} 0x{:02x} 0x{:02x} {}".format(device,
                              register, value, mode)
    logger.debug(cmd)
    pop = sp.Popen(cmd.split(" "), stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = pop.communicate()
    if pop.returncode == 0:
        return(True)
    else:
        raise IOError("No I2C communication")

def i2c_change_bit(device=0x4c, register=0x2e, bitmask=0x01,
                   value=True, mode='b'):
    reg = i2c_read_reg(device, register)
    reg2 = int(reg, base=16)
    if value:
        reg2 = reg2 | bitmask
    else:
        reg2 = reg2 & bitmask
    i2c_write_reg(device, register, reg2)

def tas5825m_init(device):
    print("TAS5825M init")

    # Select page 0
    i2c_write_reg(device, 0, 0)
    # Reset
    #i2c_change_bit(device, TAS5825M_RST_ADDR, TAS5825M_RST_REG_BIT, True)
    #i2c_change_bit(device, TAS5825M_RST_ADDR, TAS5825M_RST_DIG_BIT, True)

    # Set HiZ
    i2c_write_reg(device, TAS5825M_CTRL2_ADDR, TAS5825M_CTRL_STATE_HIZ)

    # DSP in (pre-processing)
    i2c_write_reg(device, TAS5825M_STDOUT_SEL_ADDR, TAS5825M_STDOUT_SEL_DSP_IN)

    # Set to 32 bits
    i2c_write_reg(device, TAS5825M_SAP_CTRL1_ADDR, TAS5825M_WORD_LEN_32)

    time.sleep(5.)
    # Play
    i2c_write_reg(device, TAS5825M_CTRL2_ADDR, TAS5825M_CTRL_STATE_PLAY)

def tas5825m_unmute(device):
    i2c_change_bit(device,TAS5825M_CTRL2_ADDR, TAS5825M_MUTE_BIT, value=False)

def tas5825m_mute(device):
    i2c_change_bit(device,TAS5825M_CTRL2_ADDR, TAS5825M_MUTE_BIT, value=True)

def tas5825m_info(device):
    dat = i2c_read_reg(device=0x4c, register=0x68, mode='b')
    print("Power state (0x03=play): {}".format(dat))
    dat = i2c_read_reg(device=0x4c, register=0x37, mode='b')
    print("CLK detect (FS_MON) (0: FS error): {}".format(dat))
    dat = i2c_read_reg(device=0x4c, register=0x38, mode='b')
    print("BCLK_MON: {}".format(dat))
    dat = i2c_read_reg(device=0x4c, register=0x39, mode='b')
    print("CLKDET_STATUS: {}".format(dat))
    dat = i2c_read_reg(device=0x4c, register=0x69, mode='b')
    print("Automute state (0: not muted): {}".format(dat))
    reg = i2c_read_reg(device=0x4c, register=0x5E, mode='b')
    val = int(reg, base=16) / 8.428
    print("PVDD_ADC: {} V ({})".format(val, reg))
    dat = i2c_read_reg(device=0x4c, register=0x33, mode='b')
    print("SAP_CTRL1 (I2S format, should be 0x03): {}".format(dat))

if __name__ == "__main__":
    device = 0x4c
    tas5825m_init(device)
    tas5825m_info(device)


