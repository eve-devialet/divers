#!/bin/bash

my_ip="192.168.0.208"
my_port="3334"

echo "Select your input:"
echo "0 - SPDIF input"
echo "1 - HDMI TDM"
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
echo "Y" > /sys/kernel/debug/cygnussvk_cfg/ssp_testport1/slave_mode
# Set SoC in TDM
echo "Y" > /sys/kernel/debug/cygnussvk_cfg/ssp_testport1/tdm_mode
echo "256" > /sys/kernel/debug/cygnussvk_cfg/ssp_testport1/tdm_framesize
# RX audio extraction for HDMI chip
echo 2 > /sys/class/hdmi/sii9396/rx_audio_extraction

card="0" 

# Other modifications
if [ $input -eq 0 ]
then
    echo "SPDIF input"
    # Set input 1
    i2cset -y 1 0x13 0x03 0x49 b
    card="0"
elif [ $input -eq 1 ]
then
    echo "HDMI TDM"
    i2cset -y 1 0x13 0x03 0x48 b
    card="1"
else
    echo "Nothing selected"
fi

cd ~
# Pipe to netcat
echo "Piping sound from card $card to $my_ip $my_port"
arecord -f S32_LE -r48000 -c2 -D hw:0,$card -F0 --period-size=1024 -B0 --buffer-size=4096 | nc $my_ip $my_port

exit 0
