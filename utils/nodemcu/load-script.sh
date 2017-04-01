#!/bin/bash

begin() 
{
    echo "------------ SCRIPT START ------------"
}

finish() {
    if [ $1 -eq 0 ]
    then
        echo "RESULT: Success"
    else
        echo "RESULT: Failed"
    fi
    echo "------------ SCRIPT END ------------"
    exit $1
}

begin

# CONFIGURATION
repl_name="picocom"
file_mng_name="ampy"
source_dir="testing"
destination_dir="modules"

if ! repl_loc="$(type -p "$repl_name")" || [ -z "$repl_loc" ]
then
    echo "Application picocom not found. Please install it by \"sudo apt-get install picocom\""
    finish 1
fi

#if ! result="$(python -c "import $file_mng_name" 2>&1)" || [ -n "$result" ]
if ! python -c "import $file_mng_name" 2> /dev/null
then
    echo "Python module ampy not found. Please install it by \"pip install adafruit-ampy\""
    finish 1
fi

if [ ! -e /etc/udev/rules.d/99-usb-serial.rules ]
then
  echo "udev rule file '99-usb-serial.rules' missing in /etc/udev/rules.d."
  finish 1
fi

if [ ! -e /dev/nodemcu ]
then
  echo "NodeMcu device not found make sure it is connected in USB"
  finish 1
fi

# If there is no parameter load all Robophery files
if [ $# -eq 0 ]
then
  exist=$(ampy --port /dev/nodemcu ls | grep $destination_dir)

  if [[ $exist == "$destination_dir" ]]
  then
      ampy --port /dev/nodemcu rmdir /$destination_dir
  fi

  echo "All Robophery files loading to interface=$(readlink /dev/nodemcu)"

  ampy --port /dev/nodemcu put $source_dir/ $destination_dir/

  if [ $? -ne 0 ]
  then
      finish 1
  fi
else # Load file specified as parameter to nodemcu root
  files=("$@")
  file_cnt=$#
  file_ptr=0

  while [ ! $file_cnt -eq 0 ]
  do
    echo "File \"${files[$file_ptr]}\" loading to root at interface=$(readlink /dev/nodemcu)"

    ampy --port /dev/nodemcu put ${files[$file_ptr]}

    if [ $? -ne 0 ]
    then
      finish 1
    else
      file_cnt=$((file_cnt-1))
      file_ptr=$((file_ptr+1))
    fi
  done
fi

finish 0
