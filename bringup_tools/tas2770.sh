#!/bin/bash
# I2C init script for TAS2770

i2cdev=2
i2caddrlist="0x41 0x42 0x44 0x46"
# Remove kernel module to avoid putting amp in soft shutdown
rmmod snd_soc_tas2770
for i2caddr in ${i2caddrlist}; do
	# Init
	addr=("0x00" "0x7f" "0x00" "0x00" "0x03" "0x05" "0x0e" "0x1b" "0x32" "0x3c" "0x7e")
	data=("0x00" "0x00" "0x00" "0x06" "0x14" "0x03" "0xf3" "0x00" "0x80" "0x21" "0x38")
	for i in {0..10}; do
		echo "i2cset -y $i2cdev $i2caddr ${addr[$i]} ${data[$i]}" 
		i2cset -y $i2cdev $i2caddr ${addr[$i]} ${data[$i]} 
	done

	# Remove temp protection
	addr=("0x7f" "0x02" "0x00" "0x0d")
	data=("0x00" "0x02" "0xfd" "0x0d")
	for i in {0..3}; do
		echo "i2cset -y $i2cdev $i2caddr ${addr[$i]} ${data[$i]}" 
		i2cset -y $i2cdev $i2caddr ${addr[$i]} ${data[$i]} 
	done
	echo "i2cget -y $i2cdev $i2caddr 0x48" 
	bit=`i2cget -y $i2cdev $i2caddr 0x48`
	#Test if $bin -eq 0x01
	echo "Bit 0x048 should be 1: "$bit
	addr=("0x48" "0x0d" "0x00" "0x02")
	data=("0x41" "0x00" "0x00" "0x00")
	for i in {0..3}; do
		echo "i2cset -y $i2cdev $i2caddr ${addr[$i]} ${data[$i]}" 
		i2cset -y $i2cdev $i2caddr ${addr[$i]} ${data[$i]} 
	done
	# Set 48kHz format, high to low, autodetect sample rate disabled
	addr=("0x02" "0x0a" "0x02")
	data=("0x02" "0x17" "0x00")
	for i in {0..2}; do
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
done
