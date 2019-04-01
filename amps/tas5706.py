#!/usr/bin/env python3
import subprocess as sp
import logging
logger = logging.getLogger(__name__)
import csv
 
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

def tas5706_init(device):
    print("TAS5706 init")
    lines = read_ini_file()
    for line in lines:
        register = int(line[1], base=16)
        if line[0] == 1:
            # Write one byte
            value = int(line[2], base=16)
            #print("{} {} {}".format(device, register, value))
            i2c_write_reg(device=device, register=register, value=value, mode='b')
        if line[1] == 2:
            # Multibyte write
            print("Unimplemented multibyte write")


def read_ini_file():
    lines = list()
    with open("tas5706_2BTL_ini.csv", "r") as myfile:
        mycsv = csv.reader(myfile, delimiter=";")
        for line in mycsv:
            if int(line[0]) == 0:
                # 0 means comment line
                pass
            else:
                lines.append([int(line[0]), line[1], line[2]])
    return(lines)  

if __name__ == "__main__":
    tas5706_init(0x4c)