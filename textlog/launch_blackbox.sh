#!/bin/bash
sleep 10
cd /home/pi/housemachine/python
/usr/bin/screen -dmS blackbox /usr/bin/python /home/pi/housemachine/python/blackbox_logger.py
