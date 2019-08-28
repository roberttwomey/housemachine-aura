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
    for trail in d:
        thisshape = []
        for point in trail:
            # print cv[:2]
            thisshape.append(point)#:2])

        # print "***"
        i = i +1
        # print "this poly",poly
        # shapes.append(thisshape)
        shapes.append(np.array(thisshape))

    return shapes
    # return d

def mapToScreen(point, minx, maxx, miny, maxy):

    width = maxx - minx
    height = maxy - miny

    if width > height:
        scale = 800.0 / (width * 1.0)
        margin = width * 0.0
        # scale = 800.0 / (width * 1.4)
        # margin = width * 0.2
        dominant = width
        
    else:
        scale = 800.0 / (height * 1.0)
        margin = width * 0.0
        # scale = 800.0 / (height * 1.4)
        # margin = height * 0.2
        dominant = height

    xoff = 0 - margin - ((dominant - width) / 2.0)
    yoff = 0 - margin - ((dominant - height) / 2.0)
    
    offset = np.array((-xoff, -yoff)) * scale

    mappedpoint = (point * scale + offset)
    mappedpoint[1] = 800.0 - mappedpoint[1]
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
    parser.add_argument('width', type=float, default=512)
    parser.add_argument('height', type=float, default = 512)
    parser.add_argument('infile',
            help='output of json to text command (.txt)', nargs='+')
    
    args = parser.parse_args()
    width = args.width
    height = args.height
    infile = args.infile
                
    # colors
    WHITE = (255, 255, 255)
    BLUE = (255, 0, 0)

    # blank image 
    img = np.zeros((800, 800, 3), np.uint8)

    for infname in infile:
        
        # read in input file (drawing reording)
        shapes = ReadJSONDrawingData(infname)
        
        cv2.rectangle(img, (0,0), (800, 800), WHITE, cv2.FILLED)
        print shapes

        for shape in shapes:

            # points = shape

            firstPoint = True

            for point in shape:
                print point
                curr = mapToScreen(point, 0, width, 0, height)
                
                # pen down
                color = BLUE

                if firstPoint:
                    firstPoint = False
                else:
                    cv2.line(img, (int(last[0]), int(last[1])), (int(curr[0]), int(curr[1])), (color), 1)

                last = curr

        # save out image image
        outfname = infname.split(".")[0]+".png"            
        print "Saving image {0}".format(outfname)
        cv2.imwrite(outfname, img)


if __name__ == "__main__":
    main()
    
