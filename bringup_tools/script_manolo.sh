#!/bin/bash

my_ip="192.168.0.208"
my_port="3334"

echo "Select your input:"
echo "0 - SPDIF Right"
echo "1 - SPDIF Left"
echo "2 - Line"
echo "3 - Phono"
read input

cd /sys/class/gpio

# AKM reset off
echo "404" > export
echo "357" > export
echo "506" > export

echo "out" > gpio404/direction
echo "in" > gpio357/direction
echo "in" > gpio506/direction

echo "1" > gpio404//value

# Set device in master
i2cset -y 1 0x13 0x01 0x5a b 
# Interrupt on unlock
i2cset -y 1 0x13 0x05 0xa5 b
# Set SoC in slave
echo "Y" > /sys/kernel/debug/cygnussvk_cfg/ssp_testport0/slave_mode

# GPIO for relays
cd /sys/class/gpio
echo "374" > export
echo "468" > export

echo "out" > gpio374//direction
echo "out" > gpio468//direction

echo "379" > export
echo "out" > gpio379//direction

echo "377" > export
echo "378" > export
echo "out" > gpio377//direction
echo "out" > gpio378//direction

# Set FS pins
echo "1" > gpio378//value
echo "1" > gpio377//value

# Deactivate phono
echo "0" > gpio379//value

#ADC reset off
echo "443" > export
echo "out" > gpio443/direction
echo "1" > gpio443//value

card="0" 

# Switch analog/digital relays
if [ $input -eq 0 ] || [ $input -eq 1 ]
then
    echo "SPDIF"
    #echo "1" > gpio374//value
    echo "1" > gpio468//value; sleep 0.1; echo "0" > gpio468//value 
    card="0"
elif [ $input -eq 2 ] || [ $input -eq 3 ]
then
    echo "analog"
    echo "1" > gpio374//value; sleep 0.1; echo "0" > gpio374//value
    card="1"
fi

# Other modifications
if [ $input -eq 0 ]
then
    echo "SPDIF Left"
    i2cset -y 1 0x13 0x03 0x48 b
elif [ $input -eq 1 ]
then
    echo "SPDIF Right"
    i2cset -y 1 0x13 0x03 0x49 b
elif [ $input -eq 2 ]
then
    echo "Line"
elif [ $input -eq 3 ]
then
    echo "Phono"
    # Activate phono
    echo "1" > gpio379/value
else
    echo "Nothing selected"
fi

cd ~
# Pipe to netcat
echo "Piping sound from card $card to $my_ip $my_port"
arecord -f S32_LE -r48000 -c2 -D hw:0,$card -F0 --period-size=1024 -B0 --buffer-size=4096 | nc $my_ip $my_port

exit 0
