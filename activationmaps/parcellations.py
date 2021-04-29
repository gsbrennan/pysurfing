# ----------------------------------------------------------------
# Oxford Mathematical Brain Modelling Group
#   This file defines the basic parcellation maps.  New
#   parcellations can be constructed by deriving a new
#   class from the parcellation base class
#       1. Python v3.8 or higher
#       2. Python numpy package
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

from activationmaps.coloring import getColor

class parcellationBase:

    # ------------
    def __init__(self,nRegions):
        # A dictionary of the regions supported by
        # your parcellation.

        self.nR = int(nRegions)
        self.RGB = {}
        self.regionMap = {}

        # The default RGB value (defaults to gray in freesurfer)
        self.defaultRGB = [160, 160, 160]
        dstr = 'nolabel'
        
        # Do we use a matplotlib colormap
        self.usecm = False
        self.cmap = None

        for i in range(self.nR):
            self.regionMap[i] = dstr
            self.RGB[i] = self.defaultRGB

    # ------------
    def __checkRegionIndex(self,idxRgn):
        idxRgn = int(idxRgn)

        if idxRgn < 0 or idxRgn > self.nR:
            print(f"Invalid Region index.  Valid range is an integer from 0 to {self.nR-1}")
            return False

        return True

    # ------------
    # Determines whether a matplotlib colormap should be used 
    # when deducing RGB values for this parcellation
    # c.f. https://matplotlib.org/3.1.0/tutorials/colors/colormap-manipulation.html
    #
    #   
    # Example
    #   turn off colormap usage: setUseMatplotlibColorMap(False)
    #
    #   turn on colormap usage: in this case the option cmap should be 
    #   a matplotlib colormap
    #   
    #   mymap = matplotlib.cm.get_cmap('viridis')
    #   setUseMatplotlibColorMap(True,cmap=mymap)
    #
    def setUseMatplotlibColorMap(self, use, cmap=None):
        self.usecm = use
        
        if use:
            self.cmap = cmap
        else:
            self.cmap = None
            
    # -------------
    # Returns the internal colormap variables.  This function 
    # is used by the activation map <--> parcellation interface
    def getCurrentMatplotlibColormapConfig(self):
        return self.usecm, self.cmap

    # ------------
    # label a region index with an anatomical string
    def setRegionLabel(self, idxRgn, strLabel):
        idxRgn = int(idxRgn)

        if self.__checkRegionIndex(idxRgn):
            self.regionMap[idxRgn] = strLabel

    # ------------
    def setRegionRGBValue(self, idxRgn, r, g, b):
        idxRgn = int(idxRgn)

        if self.__checkRegionIndex(idxRgn):
            self.RGB[idxRgn] = [r, g, b]

    # ------------
    def getNumberOfRegions(self):
        return self.nR

    # returns a list of all valid numerical region indices
    def getRegionIndices(self):
        #x = []
        #for i in range(self.nR):
        #    x.append(i)
        #return x
        return list(self.regionMap.keys())

    #------------
    def getRegionLabel(self, idxRgn):
        lab = 'invalid index'
        idxRgn = int(idxRgn)

        if self.__checkRegionIndex(idxRgn):
            lab = self.regionMap[idxRgn]
        else:
            print(f"Invalid region index {idxRgn} passed to getRegionLabel")

        return lab

    #------------
    def getRegionRGB(self, idxRgn):
        rgbv = self.defaultRGB
        idxRgn = int(idxRgn)

        if self.__checkRegionIndex(idxRgn):
            rgbv = self.RGB[idxRgn]
        else:
            print(f"Invalid region index {idxRgn} passed to getRegionRGB")

        return rgbv

    #------------
    # this function returns a dictionary whose
    # keys are region labels and whose indices
    # are the region indexes
    def getRegionToIndexMap(self):
        res = {}

        for k in self.regionMap:
            val = self.regionMap[k]
            res[val] = k

        return res


    #-----------------
    # Returns a dictionary whose keys are region
    # labels of the parcellation and whose values
    # are the current RGB entries in the form of
    # an integer list [R, G, B] where
    # 0<= R, G, B, <= 255
    def getRegionRGBDictionary(self):
        res = {}

        ndx = self.getRegionIndices()
        for i in ndx:
            rgnstr = self.getRegionLabel(i)
            res[rgnstr] = self.RGB[i]

        return res

    # -----------------
    # Takes as input a dictionary whose keys
    # are the region labels (of the parcellation)
    # and whose values are expected to be an
    # integer array of the form [R, G, B]
    # where 0<= R,G,B <= 255
    def setFromRegionRGBDictionary(self,rdict):
        lookup = self.getRegionToIndexMap()
        strndx = list(rdict.keys())

        for j in strndx:
            iRegion = lookup[strndx]
            rgb = rdict[j]
            self.setRegionRGBValue(iRegion, int(rgb[0]), int(rgb[1]), int(rgb[2]))

    #------------
    # Returns a dictionary whose keys are region
    # labels of the parcellation and whose values
    # is a floating point.  You can set the initialization
    # value of all keys by using the option
    #    floatval = x where x is a floating point.
    #    floatval = 0.0 by default
    def getRegionValueDictionary(self, floatval=0.0):
        res = {}
        finit = float(floatval)

        ndx = self.getRegionIndices()
        for i in ndx:
            rgnstr = self.getRegionLabel(i)
            res[rgnstr] = finit
        
        return res


    # -----------------
    # Takes as input a dictionary whose keys
    # are the region labels (of the parcellation)
    # and whose values are expected to be a
    # single floating point.  You should specify
    # the minimum and maximum value to use for the
    # RGB calculation if they differ from the defaults
    # of min=0.0 and max = 1.0
    # 
    # if the option setMinToDefault == True then 
    # the default RGB color is used for all minimum values
    def setRGBfromValueDictionary(self, rdict, min=0.0, max=1.0, setMinToDefaultRGB=False):
        lookup = self.getRegionToIndexMap()
        strndx = list(rdict.keys())

        for j in strndx:
            iRegion = lookup[j]
            val = rdict[j]
            
            rgb = {'R':self.defaultRGB[0], 'G':self.defaultRGB[1], 'B':self.defaultRGB[2]}
            
            if setMinToDefaultRGB == False or val != min:
                rgb = getColor(val, min, max, self.usecm, self.cmap)
            
            self.setRegionRGBValue(iRegion, rgb['R'], rgb['G'], rgb['B'])

    #------------
    # Reset all regions to the default RGB color
    #    (amounts to a uniform reset of the parcellation)
    def resetToDefaultRGB(self):
        indxs = self.getRegionIndices()
        for i in indxs:
            self.setRegionRGBValue(i, self.defaultRGB[0], self.defaultRGB[1], self.defaultRGB[2])


# Specific parcellations provide two things
#
# 1. region labels for that parcelation:
#       this should be done in the constructor as in the DK atlas below
# 2. Extended functionality.  As an example, the DK atlas supports 
#       a Parcellation-specific lobe grouping that is used by the 
#       companion DK activation class
class parcellationDesikanKillianyHemisphere(parcellationBase):

    def __init__(self):

        # The Desikan Killiany atlas has 36 regions
        # (per hemisphere)
        super().__init__(36)

        # These are the canonical region labels for the
        # Desikan Killiany atlas as used by freesurfer
        super().setRegionLabel(0, 'unknown')
        super().setRegionLabel(1, 'bankssts')
        super().setRegionLabel(2, 'caudalanteriorcingulate')
        super().setRegionLabel(3, 'caudalmiddlefrontal')
        super().setRegionLabel(4, 'corpuscallosum')
        super().setRegionLabel(5, 'cuneus')
        super().setRegionLabel(6, 'entorhinal')
        super().setRegionLabel(7, 'fusiform')
        super().setRegionLabel(8, 'inferiorparietal')
        super().setRegionLabel(9, 'inferiortemporal')
        super().setRegionLabel(10, 'isthmuscingulate')
        super().setRegionLabel(11, 'lateraloccipital')
        super().setRegionLabel(12, 'lateralorbitofrontal')
        super().setRegionLabel(13, 'lingual')
        super().setRegionLabel(14, 'medialorbitofrontal')
        super().setRegionLabel(15, 'middletemporal')
        super().setRegionLabel(16, 'parahippocampal')
        super().setRegionLabel(17, 'paracentral')
        super().setRegionLabel(18, 'parsopercularis')
        super().setRegionLabel(19, 'parsorbitalis')
        super().setRegionLabel(20, 'parstriangularis')
        super().setRegionLabel(21, 'pericalcarine')
        super().setRegionLabel(22, 'postcentral')
        super().setRegionLabel(23, 'posteriorcingulate')
        super().setRegionLabel(24, 'precentral')
        super().setRegionLabel(25, 'precuneus')
        super().setRegionLabel(26, 'rostralanteriorcingulate')
        super().setRegionLabel(27, 'rostralmiddlefrontal')
        super().setRegionLabel(28, 'superiorfrontal')
        super().setRegionLabel(29, 'superiorparietal')
        super().setRegionLabel(30, 'superiortemporal')
        super().setRegionLabel(31, 'supramarginal')
        super().setRegionLabel(32, 'frontalpole')
        super().setRegionLabel(33, 'temporalpole')
        super().setRegionLabel(34, 'transversetemporal')
        super().setRegionLabel(35, 'insula')

        # Here we populate an internal dictionary which we must
        # build manually.  This internal dictionary defines groupings
        # for this atlas.
        self.regionGroupings = {'Lobe':self.__setLobeIndices()}

    def __setLobeIndices(self):
        # The list of lobes for the DK atlas can be found here
        # https://surfer.nmr.mgh.harvard.edu/fswiki/CorticalParcellation
        # also c.f. https://en.wikipedia.org/wiki/File:Lateral_surface_-_Middle_frontal_gyrus.png
        lobes = {'Frontal':[2, 3, 12, 14, 17, 18, 19, 20, 24, 26, 27, 28, 32],
                 'Parietal':[8, 10, 22, 23, 25, 29, 31],
                 'Temporal':[1, 6, 7, 9, 15, 16, 30, 33, 34],
                 'Occipital':[5, 11, 13, 21]}

        return lobes

    # This function returns a list of supported groupings defined for this
    # atlas.  The grouping keys can be used to set group-wide RGB values
    def getSupportedGroupings(self):
        return list(self.regionGroupings.keys())

    # This function returns a list of identifiers for a particular grouping
    # this list of identifiers can be used, directly, to set group RGB values
    def getSubgroupings(self, groupStr):

        retv = ['invalid group identifier string']

        if groupStr in self.regionGroupings:
            retv = list(self.regionGroupings[groupStr].keys())

        return retv

    # Set all RGB entries in the subgroup `subgroupStr' belonging to
    # grouping `groupStr' to the indicated values.
    # Example: setGroupRGB('Lobes', 'Frontal', 255, 0, 0)
    # Returns true if successful and false otherwise
    def setGroupRGB(self, groupStr, subgroupStr, R, G, B):
        retv = False

        if groupStr in self.regionGroupings:
            if subgroupStr in self.regionGroupings[groupStr]:
                subgids = self.regionGroupings[groupStr][subgroupStr]
                for id in subgids:
                    super().setRegionRGBValue(id, R, G, B)
            else:
                print(f"{subgroupStr} is not a subgroup identifier of the grouping {groupStr}")
        else:
            print(f"{groupStr} is an invalid group identifier")





