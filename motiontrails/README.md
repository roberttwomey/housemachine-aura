# Setup

Requires pylab, etc.

```bash
sudo apt-get install python-numpy python-scipy python-matplotlib
```

# Generate an image from tracked json

```bash
python combine_tracking_json.py 640 480 1920 ~/housemachine-aura/data/json/*.json
```

# Raspberry Pi node for displaying tracked videos

## Play tracked video fullscreen

`omxplayer overhead_tracking.mp4`

## Play tracked video fullscreen on rotated screen:

`omxplayer --orientation 90 overhead_tracking.mp4`
 
