#!/usr/bin/env python3
import subprocess as sp
import logging
logger = logging.getLogger(__name__)

TAS2770_PWR_CTL_ADDR = 0x02
TAS2770_PAGE_ADDR = 0x00
TAS2770_BOOK_ADDR = 0x7F
TAS2770_PCM_DIG_VOLUME_ADDR = 0x05

TAS2770_DEFAULT_I2C = 0x41

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

def tas2770_set_volume(device, volume):
    '''
    Volume value in dB (e.g : 0dB = max, -100dB = min, -101dB = mute)
    We send the doubled hex value as command :
    0x02 means -1 dB, 0x01 means -0.5 dB, etc.
    '''
    volume_val = int(abs(volume) * 2)
    i2c_write_reg(device, TAS2770_PCM_DIG_VOLUME_ADDR, volume_val)

def tas2770_unmute(device):
    print("TAS2770 unmute")
    # Unmute and make current and voltage sense active
    i2c_write_reg(device, TAS2770_PWR_CTL_ADDR, 0x00)

if __name__ == "__main__":
    device = TAS2770_DEFAULT_I2C
    tas2770_set_volume(device, -12)
    tas2770_unmute(device)
