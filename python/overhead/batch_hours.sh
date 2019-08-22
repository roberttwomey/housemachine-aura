#!/bin/bash

files=/home/rtwomey/housemachine/data/cv_lossless/*.txt
outdir=/hom/rtwomey/housemachine/data/cv_lossless/hours

# loop over files
for i in $files
do
	filename=$(basename "$i")
	filename="${filename%.*}"

	echo "processing $filename"	
	# ./concat.sh $filename
	ffmpeg -loglevel 0 -f concat -i $filename.txt -c copy hours/$filename.mp4
done
