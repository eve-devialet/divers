#!/bin/bash

pwm_boost=false
if $pwm_boost; then 
	echo "Set up PWM boost"
	# PWM GPIO
	cd /sys/class/gpio
	echo 1272 > export
	echo out > gpio1272/direction
	# PWM activation
	cd /sys/class/pwm/pwmchip30
	/sys/devices/platform/soc/200f000.qcom,spmi/spmi-0/spmi0-01/200f000.qcom,spmi:qcom,pms405@1:qcom,pwms@bc00/pwm/pwmchip30 # echo 0 > export
	echo 0 > export
	cd pwm0
	echo 100 > period
	echo 90 > duty_cycle
	echo 1 > enable

	# Boost activation
	cd /sys/class/gpio
	echo 37 > export
	echo out > gpio37/direction
	echo 1 > gpio37/value
else
	echo "Set up GPIO boost"
	cd /sys/class/gpio
	for i in 36 78; do
		echo GPIO $i
		echo $i > export
		echo out > gpio$i/direction
		echo 0 > gpio$i/value
	done
fi


# Enable amps
cd /sys/class/gpio
for i in 103 104 106 113 115; do
echo GPIO $i
echo $i > export
echo out > gpio$i/direction
echo 1 > gpio$i/value
done

bash ./tas2770.sh
