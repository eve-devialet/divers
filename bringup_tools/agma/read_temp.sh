#/bin/bash

FILENAME=$1
echo "Filename: "$FILENAME

TIMESTEP=$2
echo "Timestep: "$TIMESTEP

echo "Time (s);Temp (LSM6D); Temp (boost)" > $FILENAME

while true; do
	time=`date +"%H:%M:%S"`
	temp1=`i2cget -y 2 0x48 0x00`
	temp2_lsb=`i2cget -y 2 0x6a 0x20`
	temp2_msb=`i2cget -y 2 0x6a 0x21`

	echo "$time;$temp1;$temp2 $temp2_msb" >> $FILENAME
	echo "$time;$temp1;$temp2_msb $temp2_lsb"
	sleep $TIMESTEP

done
