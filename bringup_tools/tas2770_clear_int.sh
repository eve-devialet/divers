#!/bin/bash
# I2C init script for TAS2770

i2cdev=2
i2caddrlist="0x41 0x42 0x44 0x46"
#i2caddrlist="0x41"
# Remove kernel module to avoid putting amp in soft shutdown
rmmod snd_soc_tas2770
for i2caddr in ${i2caddrlist}; do
	# Unmute all amps
	echo ""
        echo "Amp $i2caddr"
	addr=("0x02")
	data=("0x00")
	for i in 0; do
		echo "i2cset -y $i2cdev $i2caddr ${addr[$i]} ${data[$i]}" 
		i2cset -y $i2cdev $i2caddr ${addr[$i]} ${data[$i]} 
	done
	# Read interrupt registers to clear
	addr=("0x24" "0x25" "0x26")
	for i in {0..2}; do
		res=`i2cget -y $i2cdev $i2caddr ${addr[$i]}`
                if [[ "$res" == "0x00" ]]; then
                        echo "OK"
                else
			echo "Interrupt reg $i (${addr[$i]}): $res"
                fi
	done
	res=`i2cget -y $i2cdev $i2caddr 0x02`
	echo "Mute reg (0=OK): $res"
done
echo ""
