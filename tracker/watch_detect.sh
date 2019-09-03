#!/bin/bash


inotifywait -m /home/pi/housemachine/data/videos -e close_write |
    while read path action file; do
        echo "The file '$file' appeared in directory '$path' via '$action'"
        # do something with the file
	echo "Moving file to /media/housedata/videos"
	mv $path/$file /media/housedata/videos/
	echo "Calculating background subtraction"
	python bgsubtract_track.py --headless --radius 30 --outputsize 1280 --maxblob 30000 --write /media/housedata/videos/$file /media/housedata/tracked/$file 
#	killall omxplayer.bin
	#filename=$(basename "$file")
	#filename="${filename%.*}"
	#scp pi@trails.locaoutfile=$outdir/$filename.mp4
    done

