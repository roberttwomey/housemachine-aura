# Setup

Requires pylab, etc.

```bash
sudo apt-get install python-numpy python-scipy python-matplotlib ffmpeg
```

# Generate an image from tracked json

```bash
python combine_tracking_json_movie.py 640 480 640 480 ~/housemachine-aura/data/json/*.json
ffmpeg -i /home/pi/housemachine-aura/data/json/livingroom_motion_2017-08-17_21_trails.avi -c:v libx264 -preset ultrafast -crf 0 trails.mp4
```

# Raspberry Pi node for displaying tracked videos

## Play tracked video fullscreen

`omxplayer overhead_tracking.mp4`

## Play tracked video fullscreen on rotated screen:

`omxplayer --orientation 90 overhead_tracking.mp4`
 
