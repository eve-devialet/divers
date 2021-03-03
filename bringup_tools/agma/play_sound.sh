#!/bin/bash

FILENAME=$1
USER_VOLUME=$2

echo "Usage: nohub bash play_sound.sh [absolute filename] [[volume]]"
echo "Do not forget nohup, or script will stop when adb session ends"
echo "If relative filename is given, loop will only work once."
echo ""
if [[ -z $FILENAME ]];
then
    echo `date`" - Missing mandatory argument: filename (absolute path). "
    echo `date`" - Usage: ./play_sound.sh [filename] [[volume]]"
  exit 1
fi
if [[ -z $USER_VOLUME ]];
then
    echo `date`" - No volume selected, using 0.2. "
    export VOLUME=0.2
    echo `date`" - Usage: ./play_sound.sh [filename] [[volume]]"
else
    export VOLUME=$USER_VOLUME
fi

while true; do
  echo "Filename (absolute path): "$FILENAME
  bash /usr/libexec/twix/wrappers/play_file $FILENAME&
  sleep 2

  # Reset TAS2770
  i2cdev=2
  i2caddrlist="41 42 44 46"
  cd /sys/kernel/debug/regmap
  for i2caddr in ${i2caddrlist}; do
    # Unmute all amps
    echo "SW reboot amp 0x$i2caddr"
    echo 0x02 > 2-00$i2caddr/address
    echo 1 > 2-00$i2caddr/count
    echo 1 > 2-00$i2caddr/data
    sleep 0.1
    echo 0 > 2-00$i2caddr/data
  done
  # Wait for process to end
  wait
done
