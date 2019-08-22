if [ $# -eq 0 ]
  then
    room=livingroom
    echo "No arguments supplied, using $room" 
else
	room=$1
fi

rooms=(diningroom kitchen childsroom basement studio)

for room in "${rooms[@]}"
do

	files=/home/rtwomey/housemachine/data/ceiling/$room/*.mp4
	outdir=/home/rtwomey/housemachine/data/ceiling/audio/$room

	echo "reading files from $files"
	echo "writing sound to $outdir"

	shopt -s nullglob

	#!/bin/bash
	if [ ! -d $outdir ] 
	then
	    mkdir -p $outdir
	fi

	# loop over files
	for i in $files
	do
		filename=$(basename "$i")
		filename="${filename%.*}"
		outfile=$outdir/$filename.wav
		# echo $filename
		# echo $i
		# echo $outdir/$filename.mov
		if [ ! -e $outfile ]
			then
			# if [ -f /etc/passwd ]
			echo "processing $i"
			ffmpeg -loglevel 0 -i $i -f wav -ar 48000 -vn $outfile
			# mv $i $datadir/processed
		fi
	done
done