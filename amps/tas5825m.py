#!/usr/bin/env python3
from tas5825m_header import *
import subprocess as sp
import logging
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

    # DSP in
    i2c_write_reg(device, TAS5825M_STDOUT_SEL_ADDR, TAS5825M_STDOUT_SEL_BIT)

    # Set to 24 bits
    i2c_write_reg(device, TAS5825M_SAP_CTRL1_ADDR, TAS5825M_WORD_LEN_24)

    # Play
    i2c_write_reg(device, TAS5825M_CTRL2_ADDR, TAS5825M_CTRL_STATE_PLAY)

def tas5766m_unmute(device):
    i2c_write_reg(device,TAS5825M_CTRL2_ADDR, TAS5825M_MUTE_BIT, value=False)

def tas5766m_mute(device):
    i2c_write_reg(device,TAS5825M_CTRL2_ADDR, TAS5825M_MUTE_BIT, value=True)


if __name__ == "__main__":
    device = 0x4c
    tas5825m_init(device)


