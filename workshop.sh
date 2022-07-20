#!/bin/bash
cat<<tac
###may#####     Building public, dynamic webapps using
#contain###            MicroPython on the ESP32
##hackers#    is a Workshop at May Contain Hackers 2022, by
########        Bjarni Rúnar Einarsson <bre@pagekite.net>
##
#   The aim of this workshop is to give an introduction to the tools and
#   processes involved in developing web-apps for the ESP32_CAM module,
#   using MicroPython and the uPageKite packge.
#
#   Much of what is presented here will also work for other ESP32-based
#   boards, as well as the Raspberry Pi Pico W.
#
#   The way this workshop works, is we are going to repeat making edits
#   to this shell script, discuss the changes, and run it. Once we've
#   reached the end, you'll have done the following:
#
#      * Installed the ESP32 SDK, MicroPython and uPageKite
#      * Made contact with the ESP32
#      * Learned how to read/write the the ESP32's flash
#      * Learned how to access the MicroPython serial console
#      * Launch a simple, live web-app
#
tac


##############################################################################
### 0. Download the workshop handouts (or ask Bjarni for the backup USB key)
#
# git clone https://github.com/BjarniRunar/mch2022-esp32-fun
# cd mch2022-esp32-fun
#
## Edit workshop.sh using your favorite editor. Which is vi, amirite?
## Configure your WiFi and PageKite settings.
#
# vi workshop.sh   ## <- You Are Here
#
# export UPK_WIFI_SSID="MCH2022-open"
# export UPK_WIFI_KEY=""
# export UPK_KITE_NAME=""
# export UPK_KITE_SECRET=""
#
## In another window: Run the workshop script!
#
# bash workshop.sh    # If you uncomment this, enjoy your infinite loop
#
## That's how we're doing things, because typing and typos are boring.



### -- Script magic - just pretend you didn't see these, nudge wink --
export HACKDIR=$(pwd)
export IDF_TOOLS_PATH=$HACKDIR/esp-tools
export UPK_APP=$HACKDIR/webapp
export PYTHONPATH=$HACKDIR/upagekite:$PYTHONPATH
set -e -x
### -- Script magic ends --


##############################################################################
### 1. Install Prerequisites
#
# See: https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/linux-macos-setup.html
#
## Debian/Ubuntu
#
# sudo apt-get update && sudo apt-get install \
#      git wget flex bison gperf python3 cmake ninja-build ccache \
#      libffi-dev libssl-dev dfu-util libusb-1.0-0 python3-venv picocom
#
## CentOS? Fedora?
#
# sudo yum -y update && sudo yum install \
#      git wget flex bison gperf python3 cmake ninja-build ccache dfu-util \
#      libusbx picocom
#
## MacOS - Homebrew or MacPorts, pick one
#
# python --version
# brew install cmake ninja dfu-util picocom       #+ python3 if python is old
# sudo port install cmake ninja dfu-util picocom  #+ python38 if python is old
#
exit 0  # Comment out the code above, and delete this line to proceed.


##############################################################################
### 2. Check if we can see the chip!
#
## Plug it in to your USB port
#
# dmesg |tail -20 |grep -i usb
#
## You should see a USB serial device; is it ttyUSBn ?
## If not, we need to check cabling or try another board.
#
## Edit this line, if necessary:
export ESP32TTY=/dev/ttyUSB0     # Don't comment this out, it's used later!










exit 0  # Comment out the code above, and delete this to proceed.


##############################################################################
### 3. Download some tools and binaries (or copy from the USB stick)
#
## The ESP32 SDK: version 4.4, so we can rebuild MicroPython later on
#
# cd $HACKDIR
# git clone -b v4.4 --recursive https://github.com/espressif/esp-idf.git
# cd esp-idf
# ./install.sh
#
## MicroPython binaries!
#
# mkdir -p $HACKDIR/firmwares
# cd $HACKDIR/firmwares
# wget https://micropython.org/resources/firmware/esp32spiram-20220618-v1.19.1.bin
#
## The upagekite source
#
# cd $HACKDIR
# git clone https://github.com/pagekite/upagekite


exit 0  # Comment out the code above, and delete this to proceed.


##############################################################################
### 4. Flashing the chip with MicroPython
#
# cd $HACKDIR/firmwares
# source $HACKDIR/esp-idf/export.sh >/dev/null 2>&1
#
## How about first we save the firmware we already have?
##
## Note: 4MB flash == 0x3ff000 + 0x1000 ...we skip the bootloader?
##       If you want to preserve the that part too, use 0 0x400000,
##       but be warned that the write_flash command must match!
#
# esptool.py --port $ESP32TTY --baud 460800 read_flash 0x1000 0x3ff000 \
#   $HACKDIR/firmwares/esp32-cam-stock-firmware.bin
#
## Flashing! Modify this if you have another binary you like.
#
# esptool.py --port $ESP32TTY --baud 460800 write_flash -z 0x1000 \
#   $HACKDIR/firmwares/esp32spiram-20220618-v1.19.1.bin
#
#
# (After this, we should fall through to a shell configured for further
#  experimentation.)




##############################################################################
### 5. Let's take a loop at the sample webapp!
#
# vi $HACKDIR/webapp/stage_2.py
#
## We can run it locally first, to get a feel for things...
#
# cd $HACKDIR/webapp
# exec python3 stage_2.py

### 6. Uploading the upagekite source and demo to the chip
#
## This script is a silly hack to upload code to the ESP32 over
## the serial link and translate the UPK_* environment variables
## into settings usable by code running on the device. By default
## it will upload only new/changed code, and launch the webapp
## when done. For other options, consult pydoc:
#
# pydoc3 upagekite.esp32_install
#
# python3 -m upagekite.esp32_install \
#   |picocom --lower-dtr --lower-rts -b115200 $ESP32TTY
# exit 0
#
## Now we alternate between steps 5 and 6 to create our app!


##### FIXME: Insert security discussion here, demo more of the upagekite
#####        web framework.


##############################################################################
### 7. Let's get the camera working!
#
## See: https://lemariva.com/blog/2020/06/micropython-support-cameras-m5camera-esp32-cam-etc
## Also: https://github.com/BjarniRunar/building-micropython
#
## Download Bjarni's firmware (or build your own)
#
# cd $HACKDIR/firmwares
# wget https://github.com/BjarniRunar/micropython-firmwares/raw/main/micropython-esp32-cam-upagekite-20220720.bin
#
## Flash it...
#
# source $HACKDIR/esp-idf/export.sh >/dev/null 2>&1
# esptool.py --port $ESP32TTY --baud 460800 write_flash -z 0x1000 \
#   $HACKDIR/firmwares/micropython-esp32-cam-upagekite-20220720.bin
#
# rm -f /tmp/upk-change-marker.*  # Force esp32_install to re-up everything
#
## Connect to the chip, does it look different?  CTRL+X exits.
#
# sleep 2
# exec picocom --lower-dtr --lower-rts -b115200 $ESP32TTY
#
## Now go back to steps 5/6: but add --nopk to esp32_install!



### N. Play around!
#
cd $HACKDIR
set +x
if [ "$IDF_PATH" = "" ]; then
  source $HACKDIR/esp-idf/export.sh >/dev/null 2>&1
fi
cat <<tac
==== Dropping you to an interactive bash shell, CTRL-D to exit ===='

Some things to try:

  * esptool.py --help
  * esptool.py [command] --help
  * esptool.py --port $ESP32TTY chip_id
  * esptool.py --port $ESP32TTY flash_id
  * picocom --lower-dtr --lower-rts -b115200 $ESP32TTY

Hint: Use CTRL-X to escape out of picocom.

tac
exec bash \
  --rcfile <(echo "PS1='MCH/ESP32/\$? \\[\\033[1;32m\\]\\w\\[\\033[0m\\] \$ '")\
  -i
