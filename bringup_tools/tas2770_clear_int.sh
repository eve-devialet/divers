#!/bin/bash
# I2C init script for TAS2770

i2cdev=2
i2caddrlist="0x41 0x42 0x44 0x46"
# Remove kernel module to avoid putting amp in soft shutdown
rmmod snd_soc_tas2770
for i2caddr in ${i2caddrlist}; do
	# Unmute all amps
	addr=("0x02")
	data=("0x00")
	for i in 0; do
		echo "i2cset -y $i2cdev $i2caddr ${addr[$i]} ${data[$i]}" 
		i2cset -y $i2cdev $i2caddr ${addr[$i]} ${data[$i]} 
	done
	# Read interrupt registers to clear
	addr=("0x24" "0x25" "0x26")
	for i in {0..2}; do
		echo "i2cget -y $i2cdev $i2caddr ${addr[$i]}" 
		res=`i2cget -y $i2cdev $i2caddr ${addr[$i]}`
		echo "Interrupt reg $i: $res"
	done
	echo "i2cget -y $i2cdev $i2caddr 0x02" 
	res=`i2cget -y $i2cdev $i2caddr 0x02`
	echo "Mute reg (0=OK): $res"
done
