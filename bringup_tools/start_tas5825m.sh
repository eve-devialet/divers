#!/bin/bash
i2cdev=2
i2caddr="0x4c"

echo "Please make sure I2S clocks are already active!"
# Remove kernel module
rmmod snd_soc_tas5825m

# Enable amps
cd /sys/class/gpio
for i in 103; do
echo GPIO $i
echo $i > export
echo out > gpio$i/direction
echo 1 > gpio$i/value
done

# Set all registers
while read line; do
	echo "i2cset -y $i2cdev $i2caddr $line"
	i2cset -y $i2cdev $i2caddr $line
done < /home/tas5825m.reg	

# Set frequency to Hybrid 384kHz
echo "i2cset -y $i2cdev $i2caddr 0x02 0x02"
i2cset -y $i2cdev $i2caddr 0x02 0x02
# Unmute amp
echo "i2cset -y $i2cdev $i2caddr 0x03 0x03"
i2cset -y $i2cdev $i2caddr 0x03 0x03
