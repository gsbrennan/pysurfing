# ----------------------------------------------------------------
# Oxford Mathematical Brain Modelling Group
#   This script defines the coloring utilitues used by
#   the other resources in the activation map
#       3. Python v3.8 or higher
#       4. Python numpy package
#       5. Python matplotlib package
#
#
#  Authors:
#               Georgia S. Brennan          - georgia.brennan@maths.ox.ac.uk
#               Travis B. Thompson          - thompsont@maths.ox.ac.uk
#               Marie E. Rognes             - meg@simula.no
#               Alain Goriely               - goriely@maths.ox.ac.uk
#
# Distribution
# This code is distributed under the GNU GPL V3 License
# https://www.gnu.org/licenses/gpl-3.0.html
#
#
# Copyright (c) 2021 G.S. Brennan, A. Goriely. All rights reserved.
#  Mathematical Institute, Oxford University
#  Oxford, United Kingdom
# -----------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt


# this function gets an RGB value for a floating point value such
# that min <= value <= max.  
#
# The option matplotlibcmap = True indicates that 
# the input option `cmap' corresponds to a matplotlib
# colormap.  Such colormaps can be obtained by using 
# matplotlib's get_cmap(..) function
# c.f. https://matplotlib.org/3.1.0/tutorials/colors/colormap-manipulation.html
def getColor(value, minval, maxval, matplotlibcmap=False, cmap = None):

    # normalize value to [0,1]
    nValue = (value - minval) / (maxval - minval)
    rgb = {'R': 0.0, 'G': 0.0, 'B': 0.0}

    if matplotlibcmap:
        # returns an RGBA value 
        cval = cmap(nValue)
        rgb['R'] = cval[0]
        rgb['G'] = cval[1]
        rgb['B'] = cval[2]
    else: # a built in colormap is provided just in case
        if 0 <= nValue <= float(1 / 8):
            rgb['R'] = 0
            rgb['G'] = 0
            rgb['B'] = 4 * nValue + 0.5
        elif float(1 / 8) < nValue <= float(3 / 8):
            rgb['R'] = 0
            rgb['G'] = 4 * nValue - 0.5
            rgb['B'] = 1
        elif float(3 / 8) < nValue <= float(5 / 8):
            rgb['R'] = 4.0 * nValue - 1.5
            rgb['G'] = 1
            rgb['B'] = -4 * nValue + 2.5
        elif float(5 / 8) < nValue <= float(7 / 8):
            rgb['R'] = 1
            rgb['G'] = -4 * nValue + 3.5
            rgb['B'] = 0
        elif float(7 / 8) < nValue <= 1.0:
            rgb['R'] = -4 * nValue + 4.5
            rgb['G'] = 0
            rgb['B'] = 0
        else:
            print("Incorrect value range -- this indicates a bug in the script")



    # scale to RGB values between 0 and 255
    rgb['R'] = int(rgb['R'] * 255)
    rgb['G'] = int(rgb['G'] * 255)
    rgb['B'] = int(rgb['B'] * 255)

    # if desired: scale for hex conversion
    # rgb.['R'] = rgb['R']*15
    # rgb['G'] = rgb['G']*15
    # rgb['B'] = rgb['B']*15

    ret = rgb
    #ret['R'] = int(round(rgb['R']))
    #ret['G'] = int(round(rgb['G']))
    #ret['B'] = int(round(rgb['B']))

    return ret

# prints the activation color bar.
# Input: width
#        the integer width of the activation map color bar
#
# The options for this function are passed directly to getColor.
#
#      The option matplotlibcmap = True indicates that 
#      the input option `cmap' corresponds to a matplotlib
#      colormap.  Such colormaps can be obtained by using 
#      matplotlib's get_cmap(..) function
# c.f. https://matplotlib.org/3.1.0/tutorials/colors/colormap-manipulation.html

def showColorBar(width, matplotlibcmap=False, cmap = None):
    x = np.linspace(0, 1, num=1000)
    C = []
    for xv in x:
        if matplotlibcmap:
            rgbvals = getColor(xv,0.0,1.0,matplotlibcmap, cmap)
        else:
            rgbvals = getColor(xv,0.0,1.0)
        C.append([rgbvals['R'], rgbvals['G'], rgbvals['B']])

    #rgb = np.array(C)/255

    barlen = len(x)
    flag = np.empty((barlen, width, 3))

    extent = barlen-1
    for n in range(barlen):
        for w in range(width):
            flag[n, w, :] = (C[extent-n][0]/255, C[extent-n][1]/255, C[extent-n][2]/255)

    plt.xticks([])
    plt.yticks([])
    plt.imshow(flag)
    plt.show()

