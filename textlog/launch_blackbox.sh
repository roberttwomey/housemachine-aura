#!/bin/bash
sleep 10
cd /home/pi/housemachine/textlog/
/usr/bin/screen -dmS blackbox /usr/bin/python /home/pi/housemachine/textlog/blackbox_logger.py
