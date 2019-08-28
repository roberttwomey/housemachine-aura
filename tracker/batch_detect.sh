#!/bin/bash

# ths script
# 1. loops over folders of ceiling video + audio
# 2. does background subtraction and computes motion trails
# 3. saves out full resolution, lossless x264 mp4 files

rooms=(livingroom diningroom kitchen childsroom basement studio)

for room in "${rooms[@]}"
do

	files=/home/rtwomey/housemachine/data/ceiling/$room/*.mp4
	outdir=/home/rtwomey/housemachine/bigdata/cv_lossless/$room

	args="--maxblob 12000 --headless"

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
		outfile=$outdir/$filename.mp4
		tmpfile=/tmp/output.avi
		# echo $filename
		# echo $i
		# echo $outdir/$filename.mov
		if [ ! -e $outfile ]
			then
			# if [ -f /etc/passwd ]
			echo "=== cv processing ==="
			./bgsubtract_track.py --write $args $i $tmpfile
			echo "=== transcoding ==="
			echo "$outfile"
			ffmpeg -loglevel 0 -i $tmpfile -c:v libx264 -preset ultrafast -crf 0 $outfile
			echo "done"
			echo "=== copy json ==="
			cp -v /tmp/output.json $outdir/$filename.json
			# mv $i $datadir/processed
		fi
	done

done