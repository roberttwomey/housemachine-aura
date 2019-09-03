#!/bin/bash


inotifywait -m /home/pi/housemachine/data/videos -e moved_to |
    while read path action file; do
        echo "The file '$file' appeared in directory '$path' via '$action'"
        # do something with the file
	mv $path/$file /media/housedata/videos/
    done

