#!/bin/bash

inotifywait -m /media/housedata/tracked -e close_write |
    while read path action file; do
        echo "The file '$file' appeared in directory '$path' via '$action'"
        # do something with the file

	if [[ "$file" =~ .*json$ ]]; then # Does the file end with .xml?
		echo "Kill omxplayer"
		killall omxplayer.bin
        fi


	if [[ "$file" =~ .*mp4$ ]]; then
		echo "Play new file"
		omxplayer --loop $path/$file
	fi
    done

