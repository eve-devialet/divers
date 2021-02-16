#!/bin/bash
# I2C init script for TAS2770

i2cdev=2
i2caddrlist="0x41 0x42 0x44 0x46"
#i2caddrlist="0x41"
remove_temp=true

for i2caddr in ${i2caddrlist}; do
	# Software reset
	echo "Software reset..."
	addr=("0x00" "0x7f" "0x00")
	data=("0x00" "0x00" "0x00")
	for i in {0..2}; do
		echo "i2cset -y $i2cdev $i2caddr ${addr[$i]} ${data[$i]}" 
		i2cset -y $i2cdev $i2caddr ${addr[$i]} ${data[$i]} 
	done
	sleep 1

	if $remove_temp; then 
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
	fi

	# Set all registers
	while read line; do
		echo "i2cset -y $i2cdev $i2caddr $line"
		i2cset -y $i2cdev $i2caddr $line
	done < /home/tas2770.reg	

done
