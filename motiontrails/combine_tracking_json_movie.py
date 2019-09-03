#!/usr/bin/env python
"""
Render a text file of drawing data as png.

rtwomey@uw.edu

"""

import numpy as np
import pylab
import struct
import sys
# import pygame
# from pygame.locals import * 
import time
import argparse
import os
import json
import cv2

def ReadJSONDrawingData(filename):

    with open(filename) as infile:
        d = json.load(infile)

    shapes=[]
    i=0
    for trail in d['trails']:
        thisshape = {}
        for point in trail:
            # print cv[:2]
            thisshape[point[2]]=point[:2]

        # print "***"
        i = i +1
        # print "this poly",poly
        shapes.append(thisshape)
        # shapes.append(np.array(thisshape))

    return shapes

def mapToScreen(point, minx, maxx, miny, maxy, outwidth, outheight):

    width = maxx - minx
    height = maxy - miny

    xscale = (outwidth/width)
    yscale = (outheight/height)

    # for project amelia onscreen display
    margin = 0
    if xscale < yscale:
        # fit to width
        scale = xscale
        xoff = 0
        yoff = (outheight - (height * scale))/2.0
        # scale = outwidth / (width * 1.0)
        # margin = width * 0.0
        # scale = 800.0 / (width * 1.4)
        # margin = width * 0.2
        # dominant = width
    else: 
        # fit to height
        scale = yscale
        xoff = (outwidth - (width*scale))/2.0
        yoff = 0

    # else:
    #     scale = outwidth / (height * 1.0)
    #     margin = width * 0.0
    #     # scale = 800.0 / (height * 1.4)
    #     # margin = height * 0.2
    #     dominant = height

    # xoff = 0# - margin - ((dominant - width) / 2.0)
    # yoff = 0# - margin - ((dominant - height) / 2.0)
    # print(xoff, yoff)
    # yoff = 0 - margin - (((outwidth * scale)-height) / 2.0)
    
    # offset = np.array((-xoff, -yoff)) * scale

    offset = np.array((xoff, yoff))

    # print(scale, offset)
    mappedpoint = (point * scale + offset)
    # mappedpoint[1] = outwidth - mappedpoint[1]
    return mappedpoint

 
def main():
    global width, height
    
    # # check arguments
    # if len(sys.argv) > 3:
    #     infiles = sys.argv[1:]
    # else:
    #     print """Usage: render_drawings.py width height infile1.txt inifle2.txt ..."""
    #     sys.exit()

    #infiles = [ "/Users/rtwomey/Pictures/Convex Mirror storefront/work/traced.txt"]
    # handle command line arguments
    parser = argparse.ArgumentParser(description='Render drawing points as png (argparse library is required)')
    parser.add_argument('width', type=float, default=640)
    parser.add_argument('height', type=float, default = 480)
    parser.add_argument('outwidth', type=int, default=800)
    parser.add_argument('outheight', type=int, default=800)
    # parser.add_argument('outfile', default='trails.mp4')
    parser.add_argument('files', nargs='*', help='glob of input files')
    
    args = parser.parse_args()
    width = args.width
    height = args.height
    outwidth = args.outwidth
    outheight = args.outheight
    infiles = args.files
                
    # colors
    WHITE = (255, 255, 255)
    BLUE = (255, 0, 0)
    BLACK = (0, 0, 0)

    # blank image 
    # img = np.zeros((outwidth, outheight, 3), np.uint8)
    img = np.zeros((outheight, outwidth, 3), np.uint8)

    cv2.rectangle(img, (0,0), (outwidth, outheight), WHITE, cv2.FILLED)

    # fourcc = 0
    fourcc = cv2.VideoWriter_fourcc('a','v','c','1')
    outfile = infiles[0].split(".")[0]+"_trails.mp4"
    try: 
        out = cv2.VideoWriter(outfile, fourcc, 15.0, (int(outwidth), int(outheight)))
    except e:
        print(e)

    for infname in infiles:
        
        points = []

        # read in input file (drawing reording)
        shapes = ReadJSONDrawingData(infname)
        
        # print(shapes)

        for shape in shapes:

            # points = shape

            firstPoint = True

            for point in shape:
                print(shape[point])
                exit()

                curr = mapToScreen(point[:2], 0, width, 0, height, outwidth, outheight)
                
                # pen down
                # color = BLUE
                color = BLACK

                if firstPoint:
                    firstPoint = False
                else:
                    # cv2.line(img, (int(last[0]), int(last[1])), (int(curr[0]), int(curr[1])), (color), 1)
                    cv2.line(img, (np.float32(last[0]), np.float32(last[1])), (np.float32(curr[0]), np.float32(curr[1])), (color), 1, cv2.LINE_AA)

                    try:
                        # print(".", end=" ")
                        out.write(img)
                    except:
                        print("Error: video frame did not write")

                last = curr

    # save out image image
    outfname = infiles[0].split(".")[0]+"_black.png"            
    # outfname = infiles[0].split(".")[0]+".png"            
    print("Saving image {0}".format(outfname))
    cv2.imwrite(outfname, img)
    print("Writing video to {0}".format(outfile))
    out.release()

if __name__ == "__main__":
    main()
    
