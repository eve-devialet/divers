#!/bin/bash

getArch()
{
#  STR=getconf LONG_BIT
  STR=64
  if [ $STR -eq 64 ]; then
    ARCH=x86_64
  else
# default is 32bit
    ARCH=i386
  fi
  echo "------------------------------------------------"
  echo "in function getArch"
  echo STR = $STR
  echo ARCH = $ARCH
  echo "------------------------------------------------"
}

I2C-Static()
{
rm -rf libMPSSE.so
rm -rf libMPSSE.a
rm -rf sample-dynamic.o
rm -rf sample-static.o
cp -f ../include/libMPSSE_i2c.h .
cp -f ../include/linux/*.h .
cp -f ../lib/linux/i386/* .
echo ------------------------------------------------
echo Building sample by linking to static library and running it
gcc -g -Wl,--no-as-needed -ldl -I. -o sample-static.o sample-static.c libMPSSE.a
./sample-static.o
cd ..
}

I2C-Dynamic()
{
cd I2C
rm -rf libMPSSE.so
rm -rf libMPSSE.a
rm -rf sample-dynamic.o
rm -rf sample-static.o
cp -f ../include/libMPSSE_i2c.h .
cp -f ../include/linux/*.h .
cp -f ../lib/linux/i386/* .
echo ------------------------------------------------
echo Building sample by linking to dynamic library and running it
gcc -Wl,--no-as-needed -ldl sample-dynamic.c -o sample-dynamic.o
./sample-dynamic.o
cd ..
}

#Execution starts from here
getArch ;
#Select input
I2C-Static;
#Done

