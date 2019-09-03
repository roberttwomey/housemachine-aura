#!/bin/bash

inotifywait -m /media/housedata/tracked -e close_write |
    while read path action file; do
        echo "The file '$file' appeared in directory '$path' via '$action'"
        # do something with the file

	#echo "Kill omxplayer"
	#pid=$(pidof omxplayer)
	#kill $pid

	echo "Play new file"
	omxplayer $path/$file
    done

