#!/usr/bin/env python3
from tas5766m_header import *
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


def tas5766m_init(device):
    print("TAS5766M init")

    # Select page 0
    i2c_write_reg(device, 0, 0)

    # First reset the chip
    i2c_write_reg(device, TAS5766M_RQST_ADDR, TAS5766M_RQST_BIT)
    i2c_write_reg(device, TAS5766M_RSTM_ADDR, TAS5766M_RSTM_BIT | TAS5766M_RSTR_BIT)
    i2c_write_reg(device, TAS5766M_RQST_ADDR, 0)

    # Mute outputs
    i2c_write_reg(device, TAS5766M_RQML_ADDR, TAS5766M_RQML_BIT | TAS5766M_RQMR_BIT)

    # Disable clock divider autoset
    reg = i2c_read_reg(device, TAS5766M_DCAS_ADDR)
    reg2 = int(reg, base=16) | TAS5766M_DCAS_BIT
    i2c_write_reg(device, TAS5766M_DCAS_ADDR, reg2)

    # Ignore SCK detection
    reg = i2c_read_reg(device, TAS5766M_IDSK_ADDR)
    reg2 = int(reg, base=16) | TAS5766M_IDSK_BIT
    i2c_write_reg(device, TAS5766M_IDSK_ADDR, reg2)

    # Ignore clock halt
    reg = i2c_read_reg(device, TAS5766M_IDCH_ADDR)
    reg2 = int(reg, base=16) | TAS5766M_IDCH_BIT
    i2c_write_reg(device, TAS5766M_IDCH_ADDR, reg2)

    # Set BCK as PLL reference
    i2c_write_reg(device, TAS5766M_SREF_ADDR, 0x10)

    # Configure PLL for 48 kHz operations
    # Input SCK (CLKIN) is 3.072 MHz
    # PLLCK = (CLKIN * J.D * R) / P = (3.072 * 16.0 * 2) / 1
    #       = 98.304 MHz
    #  J = 16
    #  D = 0
    #  R = 2
    #  P = 1
    i2c_write_reg(device, TAS5766M_PPDV_ADDR    , 0)
    i2c_write_reg(device, TAS5766M_PJDV_ADDR    , 16)
    i2c_write_reg(device, TAS5766M_PDDV_MSB_ADDR, 0)
    i2c_write_reg(device, TAS5766M_PDDV_LSB_ADDR, 0)
    i2c_write_reg(device, TAS5766M_PRDV_ADDR    , 1)   # write value-1 to the register

    # Configure output clock dividers
    i2c_write_reg(device, TAS5766M_DDSP_ADDR    , 1)   # write value-1 to the register
    i2c_write_reg(device, TAS5766M_DDAC_ADDR    , 15)  # write value-1 to the register
    i2c_write_reg(device, TAS5766M_DNCP_ADDR    , 3)   # write value-1 to the register
    i2c_write_reg(device, TAS5766M_DOSR_ADDR    , 7)   # write value-1 to the register

    # Number of DSP clock cycle in one sample frame
    # DSPCK = 49.152 MHz
    # DSPCK / 48 kHz = 1024
    i2c_write_reg(device, TAS5766M_IDAC_MSB_ADDR, 0x04)
    i2c_write_reg(device, TAS5766M_IDAC_LSB_ADDR, 0x00)


    print("Wait for PLL to lock\n")
    # Wait for PLL lock
    pll_lock = int(i2c_read_reg(device, TAS5766M_PLCK_ADDR), base=16)
    while (pll_lock != 0):
        pll_lock = int(i2c_read_reg(device, TAS5766M_PLCK_ADDR), base=16) & TAS5766M_PLCK_BIT
        print(pll_lock)

def tas5766m_unmute(device):
    i2c_write_reg(device, TAS5766M_RQML_ADDR, 0x0)

def tas5766m_mute(device):
    i2c_write_reg(device, TAS5766M_RQML_ADDR, 0x1)

def tas5766m_reset(device):
    # Select page 0
    i2c_write_reg(device, 0, 0)

    # First reset the chip
    i2c_write_reg(device, TAS5766M_RQST_ADDR, TAS5766M_RQST_BIT)
    i2c_write_reg(device, TAS5766M_RSTM_ADDR, TAS5766M_RSTM_BIT | TAS5766M_RSTR_BIT)
    i2c_write_reg(device, TAS5766M_RQST_ADDR, 0)

if __name__ == "__main__":
    device = 0x4c
    tas5766m_init(device)
    #tas5766m_reset(device)
    tas5766m_unmute(device)
