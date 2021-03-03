#/bin/bash

echo "Usage: nohub bash read_temp.sh [filename] [timestep]"
echo "Do not forget nohup, or script will stop when adb session ends"
echo ""
FILENAME=$1
echo "Filename: "$FILENAME

TIMESTEP=$2
echo "Timestep: "$TIMESTEP
if [[ -z $FILENAME || -z $TIMESTEP ]];
then
    echo `date`" - Missing mandatory arguments: filename or timestep. "
    echo `date`" - Usage: ./read_temp.sh [filename] [timestep]"
  exit 1
fi

adcpath="/sys/devices/platform/soc/200f000.qcom,spmi/spmi-0/spmi0-00/200f000.qcom,spmi:qcom,pms405@0:vadc@3100/iio:device0/in_temp_pa_therm1_raw"

# Initialize accelero
i2cset -y 2 0x6a 0x11 0x52
i2cset -y 2 0x6a 0x10 0x30

echo "Time (s);Temp (amb I2C TMP75B); Temp (LSM6D accelero); Temp (boost ADC LMT85)" > $FILENAME

while true; do
  time=`date +"%H:%M:%S"`
  temp1=`i2ctransfer -y 2 w1@0x48 0x00 r2`
  temp2_lsb=`i2cget -y 2 0x6a 0x20`
  temp2_msb=`i2cget -y 2 0x6a 0x21`
  temp3_raw=`cat $adcpath`

  # LSB
  tmp=${temp1:5:8}
  tmp=$(($tmp>>4))
  tmp=`dc $tmp 0.0625 mul p`
  tmp1=$((${temp1:0:4}))
  tmp=`dc $tmp $tmp1 add p`
  temp1_res=$tmp
 # Converting hex value to degrees
 #temp1_res=$(($temp1))
 # LSM6D: 256MSB/degC, 0=25deg
 tmp=$(($temp2_msb))
 tmp=$((tmp>>4))
 tmp=$(($tmp+ $(($temp2_lsb))))
 tmp=`dc $tmp 256 div p`
 temp2_res=`dc $tmp 25 add p`
 # Converting ADC value
 tmp=`dc $temp3_raw 71.94 div p`
 temp3_res=`dc 186.39 $tmp sub p`

 echo "$time;$temp1_res;$temp2_res;$temp3_res" >> $FILENAME
 echo "$time;$temp1_res;$temp2_res;$temp3_res"
 sleep $TIMESTEP

done
