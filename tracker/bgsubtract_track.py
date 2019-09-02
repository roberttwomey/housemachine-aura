#!/usr/bin/env python

### !/usr/local/bin/python

'''
bg subtraction from overhead video

rtwomey@ucsd.edu 2019
'''
import numpy as np
import cv2
import os
import argparse
import sys
from collections import deque
import json

# https://github.com/ContinuumIO/anaconda-issues/issues/223
# a better video write (alternative to opencv videowriter)
# https://github.com/scikit-video/scikit-video

def sort_by_area(cnts):
	# adapted from  https://github.com/kraib/open_cv_tuts/blob/master/sorting_contours.py

	# initialize the reverse flag and sort index
	i = 0
	reverse = True

	areas = [cv2.contourArea(c) for c in cnts]
	(cnts, areas) = zip(*sorted(zip(cnts, areas),
		key=lambda b:b[1], reverse=reverse))

	# return the list of sorted contours and areas
	return (cnts, areas)


if __name__ == '__main__':

	# parse arguments for program
	parser = argparse.ArgumentParser(description='run background forground segmentation on input video',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument('--write', default=False, dest='dowrite', action='store_true', help='save tracked image as new video')
	parser.add_argument('--headless', default=False, dest='doheadless', action='store_true', help='do not display video on screen')
	parser.add_argument('--undistort', default=False, dest='doundistort', action='store_true', help='undistort circular fisheye')
	parser.add_argument('--noresample', default=False, dest='noresample', action='store_true', help='downsample input video before bgfg segmentation and tracking')
	parser.add_argument('--outputsize', default=640, type=int, dest='outputsize', help='output width (in pixels)')
	parser.add_argument('--minblob', default=600.0, type=float, help='minimum blob size to track')
	# parser.add_argument('--minblob', default=00.0, type=float, help='minimum blob size to track')
	parser.add_argument('--maxblob', default=12000.0, type=float, help='maximum blob size to track')
	parser.add_argument('--radius', default=30.0, type=float, help='maximum radius from frame to frame blob track')
	# parser.add_argument('--outpath', default='/Volumes/Work/Projects/housemachine/data/cv', help='path to store output')
	# parser.add_argument('files', nargs='*', help='glob of input files')
	parser.add_argument('infile', nargs=1, help='input file', default="../../data/livingroom_motion_2017-08-16_18.07.52_8.mp4")
	parser.add_argument('outfile', nargs=1, help='output file')
	
	args = parser.parse_args()

	# runtime options
	doWrite = args.dowrite
	doHeadless = args.doheadless
	doUndistort = args.doundistort
	noResample = args.noresample
	outputsize = args.outputsize
	minBlobSize = args.minblob
	maxBlobSize = args.maxblob
	searchRadius = args.radius
	# outpath = args.outpath
	# files = args.files
	infile = args.infile[0]
	outfile = args.outfile[0]

	print("Reading", infile)

	cap = cv2.VideoCapture(infile)

	# get input file parameters
	width = cap.get(3)
	height = cap.get(4)

	if noResample:
		outputsize = width

	# print cap.get(1), cap.get(2), cap.get(3), cap.get(4)
	# print width, height

	# calculate output file parameters
	# if noResample:
	# 	outwidth = int(width)
	# 	outheight = int(height)
	# else:
		# outwidth = outputsize
		# scalef = float(outputsize) / float(width)
		# outheight = int(scalef * height)

	outwidth = int(outputsize)
	scalef = float(outputsize) / float(width)
	outheight = int(scalef * height)
	print(outwidth, outheight)

	# mask off area outside of circular region
	circlemask = np.zeros((outheight, outwidth), np.uint8)
	cv2.circle(circlemask, (int(outwidth/2), int(outheight/2)), 280, (255, 255, 255), -1)

	# unwarp fisheye
	# cx = outwidth/2.0
	# cy = outheight/2.0
	# fl = 190.0#250.0#150.0
	# fx = fl#300#190
	# fy = fl#300#190
	#
	# K = np.array([[  fx,     0.  ,  cx],
	#               [    0.  ,   fy,  cy],
	#               [    0.  ,     0.  ,     1.  ]])
	#
	# # zero distortion coefficients work well for this image
	# D = np.array([0., 0., 0., 0.])
	#
	# # use Knew to scale the output
	# Knew = K.copy()
	# # Knew[(0,1), (0,1)] = 1.5 * Knew[(0,1), (0,1)]
	# Knew[(0,1), (0,1)] = 0.4 * Knew[(0,1), (0,1)]

	# setup video output
	if doWrite:
		exists = True
		count = 0

		# while exists:
		# 	outfilename = "{0}_cv{1:03d}.avi".format(os.path.splitext(os.path.basename(infile))[0], count)
		# 	outfile = os.path.join(outpath, outfilename)
		# 	exists = os.path.exists(outfile)
		# 	count = count + 1

		#define the codec and create VideoWriter object
		# fourcc = cv2.VideoWriter_fourcc(*'XVID')
		# fourcc = cv2.VideoWriter_fourcc(*'X264')
		# fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
		# fourcc = 0 # uncompressed avi
		# fourcc = cv2.VideoWriter_fourcc('H','2','6','4')
		fourcc = cv2.VideoWriter_fourcc('a','v','c','1')
		out = cv2.VideoWriter(outfile,fourcc, 15.0, (outwidth, outheight))

		# if doDownsample:
		# 	out = cv2.VideoWriter(outfile,fourcc, 15.0, (outwidth, outheight))
		# else:
		# 	out = cv2.VideoWriter(outfile,fourcc, 15.0, (int(width), int(height)))

		# print outwidth, outheight, out.get(1), out.get(2), out.get(3), out.get(4)
		print("Writing output to", outfile)

	# open desktop windows if necessary
	if not doHeadless:
		cv2.namedWindow('tracking', cv2.WINDOW_NORMAL)
		# cv2.namedWindow('fgmask', cv2.WINDOW_NORMAL)
		# cv2.namedWindow('fgbg', cv2.WINDOW_NORMAL)

	# setup background detector
	# http://docs.opencv.org/3.2.0/d2/d55/group__bgsegm.html
	# fgbg = cv2.bgsegm.createBackgroundSubtractorMOG(backgroundRatio=0.7)
	# fgbg = cv2.bgsegm.createBackgroundSubtractorMOG(backgroundRatio=0.3)
	# fgbg = cv2.bgsegm.createBackgroundSubtractorGMG(initializationFrames = 50)#30)
	# fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()

	# history = 50
	# fgbg = cv2.createBackgroundSubtractorMOG2(history = history, detectShadows=True)
	# fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
	# fgbg = cv2.createBackgroundSubtractorKNN(history = history, detectShadows = True)
	fgbg = cv2.createBackgroundSubtractorKNN(detectShadows = True) # default history 500 frames

	trails = []

	# loop over video file
	f = 0
	while(1):
		f = f + 1

		ret, frame = cap.read()

		if frame is None:
			break

		outputframe = cv2.resize(frame, (outwidth, outheight))

		maskedframe = cv2.bitwise_and(outputframe, outputframe, mask = circlemask)

		# frame = cv2.fisheye.undistortImage(frame, K, D=D, Knew=Knew)

		# ADVANCED BGSEGM METHODS
		# print "apply segmentation"
		fgmask = fgbg.apply(maskedframe)
		# fgmask = fgbg.apply(frame, learningRate=1.0/history)
		# fgmask = fgbg.apply(frame, learningRate = 0)

		# print "threshold"
		ret, thresh = cv2.threshold(fgmask, 244, 255, cv2.THRESH_BINARY)

		# thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
		# thresh = cv2.erode(thresh, None, iterations=10)
		if thresh is None:
			break

		# print "dilate"
		thresh = cv2.dilate(thresh, None, iterations=3)

		# print "find contours"
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

		if len(cnts) > 0:
			(newcnts, areas) = sort_by_area(cnts)
			for i in range(len(newcnts)):

				contour = newcnts[i]
				area = areas[i]

				if area > minBlobSize and area < maxBlobSize:
					# print("{0}: {1} of {2} contours".format(f, i, len(newcnts)))

					# cv2.drawContours(frame, [cnt], 0, (127, 255, 0), 3)
					# cv2.drawContours(frame, [cnt], 0, (64, 255, 0), 3)
					cv2.drawContours(frame, [contour], 0, (0, 255, 0), 3)
					# cv2.drawContours(outputframe, [contour], 0, (0, 255, 0), 3)

					# else:
					# 	largecnt = []
					# 	for point in contour:
					# 		largepoint = point / scalef
					# 		# print point, largepoint
					# 		largecnt.append(largepoint)

					# 	largecnt = np.array(largecnt)
					# 	contour = np.array(largecnt).reshape((-1,1,2)).astype(np.int32)
					# 	# cv2.drawContours(frame, [cnt], 0, (127, 255, 0), 6)
					# 	# cv2.drawContours(frame, [cnt], 0, (64, 255, 0), int(width/213))
					# 	cv2.drawContours(frame, [contour], 0, (0, 255, 0), int(width/213))

					# perimeter = cv2.arcLength(cnt,True)

					M = cv2.moments(contour.astype(np.float32))

					# center of mass
					cx = M['m10']/M['m00']
					cy = M['m01']/M['m00']

					center = (cx, cy)

					foundTrail = False

					for i, trail in enumerate(trails):
						if len(trail) == 0:
							trail.appendleft(center)
							foundTrail = True
							# print("added to zero length {0}".format(i))
							break

						dist = np.linalg.norm(np.array(trail[0])-np.array(center))

						if dist < searchRadius:
							trail.appendleft(center)
							# print("added to close trail {0}".format(i))
							foundTrail = True

					if not foundTrail:
						trails.append(deque(maxlen=10000))
						trails[-1].appendleft(center)
						# print("created new trail {0}".format(i))


		# masked = cv2.bitwise_and(outputframe, outputframe, mask=fgmask)

		# cv2.addWeighted(trails, 1.0, frame, 0.0, 0.0, frame)

		# trailsmask = cv2.cvtColor(trails, cv2.COLOR_BGR2GRAY)
		# ret, thresh = cv2.threshold(trailsmask, 0, 255, cv2.THRESH_BINARY)
		# frame = cv2.bitwise_and(frame, frame, mask=thresh)
		# print("\t\t",len(trails))

		for trail in trails:
			for i in range(1, len(trail)):
				# if either of the tracked points are None, ignore
				# them
				if trail[i - 1] is None or trail[i] is None:
					continue

				# otherwise, compute the thickness of the line and
				# draw the connecting lines
				thickness = 1#int(np.sqrt(100 / float(i + 1)) * 2.5)
				
				# draw trails on output frame
				cv2.line(frame, (np.float32(trail[i-1][0]), np.float32(trail[i-1][1])), (np.float32(trail[i][0]), np.float32(trail[i][1])), (0, 0, 255), thickness, cv2.LINE_AA)

				# if doDownsample:
					# full size
					# cv2.line(frame, (np.float32(pts[i-1][0]/scalef), np.float32(pts[i-1][1]/scalef)), (np.float32(pts[i][0]/scalef), np.float32(pts[i][1]/scalef)), (0, 0, 255), thickness, cv2.LINE_AA)
					# cv2.line(frame, (np.float32(pts[i-1][0]), np.float32(pts[i-1][1])), (np.float32(pts[i][0]), np.float32(pts[i][1])), (0, 0, 255), thickness, cv2.LINE_AA)
				# else:
					# reduced size
					# cv2.line(outputframe, (np.float32(pts[i-1][0]), np.float32(pts[i-1][1])), (np.float32(pts[i][0]), np.float32(pts[i][1])), (0, 0, 255), thickness, cv2.LINE_AA)

		# # make colored overlay of thresholded shape
		# colthresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
		# cv2.addWeighted(colthresh, 0.5, frame, 0.5, 0.0, frame)

		# # show colored overlay
		# if showMask:
		# 	colthresh = cv2.cvtColor(circlemask, cv2.COLOR_GRAY2BGR)
		# 	cv2.addWeighted(colthresh, 0.5, frame, 0.5, 0.0, frame)

		# masked = cv2.resize(masked, (outwidth,outheight))
		# thresh = cv2.resize(thresh, (outwidth,outheight))
		# fgmask = cv2.resize(fgmask, (outwidth,outheight))

		# if not fullResolution:
		# 	# frame = cv2.resize(frame, (outwidth,outheight))
		# 	frame = cv2.resize(outputframe, (outwidth,outheight))

		if not doHeadless:
			cv2.imshow('tracking',frame)
			# cv2.imshow('fgbg',fgmask)
			# cv2.imshow('mask',thresh)

		if doWrite:
			try:
				out.write(outputframe)
			except:
				print("Error: video frame did not write")
			# out.write(frame)

		k = cv2.waitKey(30) & 0xff
		if k == 27:
		   break

	print("done. ")
	# print "freeing resources"

	# write out tracked paths as json
	if doWrite:
		paths = []
		for trail in trails:
			thistrail = []
			for i in range(1, len(trail)):
				# if any of the tracked points are None, ignore them
				thistrail.append((trail[i]))
			paths.append(thistrail)

		pathfile = os.path.splitext(outfile)[0]+".json"
		print("write trails",pathfile)
		with open(pathfile, 'w') as outfile:
			json.dump(paths, outfile, indent=2)

	cap.release()
	# del cap
	# del fgbg

	if doWrite:
		out.release()
		# outfile.close()
		# del out
		# del fourcc

	cv2.destroyAllWindows()
#