#!/bin/bash

FILENAME=$1

if [[ -z $FILENAME ]];
then
    echo `date`" - Missing mandatory argument: filename (absolute path). "
    echo `date`" - Usage: ./play_sound.sh [filename]"
  exit 1
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
