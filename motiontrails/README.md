# Setup

Requires pylab, etc.

# Generate an image from tracked json

```bash
python render_tracking_json.py 1920 1080 ~/housemachine-aura/data/json/*.json
```

# Raspberry Pi node for displaying tracked videos

## Play tracked video fullscreen

`omxplayer overhead_tracking.mp4`

## Play tracked video fullscreen on rotated screen:

`omxplayer --orientation 90 overhead_tracking.mp4`
 
