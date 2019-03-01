#!/usr/bin/env python3
from tas5825m_header import *
import subprocess as sp
import logging
logger = logging.getLogger(__name__)

TAS2770_PWR_CTL_ADDR = 0x02

def i2c_read_reg(device=0x41, register=0x2e, mode='b'):
    cmd = "sudo i2cget -y 1 0x{:02x} 0x{:02x} {}".format(device, register, mode)
    logger.debug(cmd)
    pop = sp.Popen(cmd.split(" "), stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = pop.communicate()
    if pop.returncode == 0:
        return(stdout)
    else:
        raise IOError("No I2C communication")

def i2c_write_reg(device=0x41, register=0x2e, value="0x00", mode='b'):
    cmd = "sudo i2cset -y 1 0x{:02x} 0x{:02x} 0x{:02x} {}".format(device,
                              register, value, mode)
    logger.debug(cmd)
    pop = sp.Popen(cmd.split(" "), stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = pop.communicate()
    if pop.returncode == 0:
        return(True)
    else:
        raise IOError("No I2C communication")

def tas5825m_init(device):
    print("TAS5825M init")

    # Select page 0
    i2c_write_reg(device, 0, 0)

    # Unmute and make current and voltage sense active
    i2c_write_reg(device, TAS2770_PWR_CTL_ADDR, 0x00)

if __name__ == "__main__":
    device = 0x41



