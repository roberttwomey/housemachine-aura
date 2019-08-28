# Text Log Display

__Hardware__

Raspberry Pi 3, preferrably with wired ethernet connection connected to HDTV in portrait mode (vertical orientation)

__OS__

Install recent [Raspbian Buster Lite](https://www.raspberrypi.org/downloads/raspbian/)

__Configure Environment__

_To boot rpi in portrait mode_:

1. ```sudo nano /boot/config.txt```

2. add ```display_hdmi_rotate=2``` to the top of the file.

3. save and exit. 

4. Reboot. 

__Set Up Persistent Service__

1. Create a service file like the following, _blackbox.service_:
```
[Unit]
Description=Runs python based event logger after boot
After=syslog.target network.target

[Service]
Type=forking
ExecStart=/home/pi/housemachine/textlog/launch_blackbox.sh

[Install]
WantedBy=multi-user.target
```

2. copy the service file to _/etc/init/_:

```console
sudo cp blackbox.service /lib/systemd/system
```

3. enable and start

```console
sudo systemctl enable blackbox.service
sudo systemctl start blackbox.service
```

4. stop
```console
sudo systemctl stop blackbox.service
```
