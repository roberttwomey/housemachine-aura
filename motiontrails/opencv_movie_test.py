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
    # parser = argparse.ArgumentParser(description='Render drawing points as png (argparse library is required)')
    # parser.add_argument('width', type=float, default=640)
    # parser.add_argument('height', type=float, default = 480)
    # parser.add_argument('outwidth', type=int, default=800)
    # parser.add_argument('outheight', type=int, default=800)
    # # parser.add_argument('outfile', default='trails.mp4')
    # parser.add_argument('files', nargs='*', help='glob of input files')
    
    # args = parser.parse_args()
    # width = args.width
    # height = args.height
    # outwidth = args.outwidth
    # outheight = args.outheight
    # infiles = args.files
    # outfile = infiles[0].split(".")[0]+"_trails.avi"

    outfile = "test2.avi"
    width = 640
    height = 480
    outwidth = 640
    outheight = 480

    # colors
    WHITE = (255, 255, 255)
    BLUE = (255, 0, 0)
    BLACK = (0, 0, 0)

    color = BLACK

    # blank image 
    img = np.zeros((outheight, outwidth, 3), np.uint8)

    cv2.rectangle(img, (0,0), (outwidth, outheight), WHITE, cv2.FILLED)

    fourcc = 0
    try: 
        out = cv2.VideoWriter(outfile, fourcc, 15.0, (int(outwidth), int(outheight)))
    except e:
        print(e)

    curr = np.array([0, 0])
    last = curr
    for i in range(1000):

        curr = (np.random.random_sample()*width, np.random.random_sample()*height)

        cv2.line(img, (np.float32(last[0]), np.float32(last[1])), (np.float32(curr[0]), np.float32(curr[1])), (color), 1, cv2.LINE_AA)

        try:
            print(".")
            out.write(img)
        except:
            print("Error: video frame did not write")

        last = curr

    out.release()

if __name__ == "__main__":
    main()
    
