#!/usr/bin/env python3
from tas5825m_header import *
import subprocess as sp
import logging
logger = logging.getLogger(__name__)
import tas2770_dump as td

TAS2770_PWR_CTL_ADDR = 0x02
TAS2770_PAGE_ADDR = 0x00
TAS2770_BOOK_ADDR = 0x7F

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

def tas2770_init(device):
    print("TAS2770 init")
    # Only book 0
    i2c_write_reg(device, TAS2770_BOOK_ADDR, 0x00)
    for page, vals in enumerate(td.dump):
        # Change page
        i2c_write_reg(device, TAS2770_PAGE_ADDR, page)
        for value in vals:
            i2c_write_reg(device, value[0], value[1])

def tas2770_unmute(device):
    print("TAS2770 unmute")
    # Unmute and make current and voltage sense active
    i2c_write_reg(device, TAS2770_PWR_CTL_ADDR, 0x00)

if __name__ == "__main__":
    device = 0x41
    # Only book 0
    i2c_write_reg(device, TAS2770_BOOK_ADDR, 0x00)
    for page, vals in enumerate(td.dump):
        # Change page
        i2c_write_reg(device, TAS2770_PAGE_ADDR, page)
        for value in vals:
            i2c_write_reg(device, value[0], value[1])

    tas2770_unmute(device)

