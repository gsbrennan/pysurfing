# ----------------------------------------------------------------
# Oxford Mathematical Brain Modelling Group
#   Lobe activation map script - This script requires the
#   following software / packages to be present
#       1. Python v3.8 or higher
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

from activationmaps.coloring import getColor, showColorBar
import activationmaps.parcellations as parc


# This class defines the base operations for an activation map.
# Construction requires the use of a parcellation class defined in
# parcellations.py
class activationBase:

    def __init__(self,parcellation):
        self.parc = parcellation
        self.lastwritten = ''

    def __fixpath(self,path):
        fixed = path
        if fixed[-1] != '/':
            fixed = fixed + '/'
        return fixed
    
    # shows the colorbar currently associated
    # with the parcellation.  This colorbar can
    # be saved for use in figures etc
    def showActivationColorbar(self, width):
        mplib, pcmap = self.parc.getCurrentMatplotlibColormapConfig()
        showColorBar(width, matplotlibcmap=mplib, cmap=pcmap)

    def writeActivationCSV(self, path, filename):
        fullpath = self.__fixpath(path) + filename + ".csv"
        indx = self.parc.getRegionIndices()

        with open(fullpath, 'w') as ofile:
            for i in indx:
                lab = self.parc.getRegionLabel(i)
                rgb = self.parc.getRegionRGB(i)
                str = f"{i} {lab} {rgb[0]} {rgb[1]} {rgb[2]} 0\n"
                ofile.write(str)

        self.lastwritten = fullpath


    def getLastFileWritten(self):
        return self.lastwritten

    def getParcellation(self):
        return self.parc
    
    # Set regional activations (values) from an input parcellation
    # it is assumed that the parcellation you pass is the same 
    # as the map's internal parcellation type -- you can retrieve
    # the internal parcellation by calling getParcellation()
    #
    # Setting the option useParcColorScheme = False means that 
    #   we should set the internal colormap information to 
    #   coincide with the colormap of the parcellation 
    #   passed into the function
    def activateFromParcellationRGB(self, parcIn, useParcColorScheme=True):
        indxs = parcIn.getRegionIndices()
        
        if useParcColorScheme:
            use, cmap = parcIn.getCurrentMatplotlibColormapConfig()
            self.setUseMatplotlibColorMap(use, cmap)
            
        
        for i in indxs:
            rgb = parcIn.getRegionRGB(i)
            self.parc.setRegionRGBValue(i, rgb[0], rgb[1], rgb[2])
        
        
    # provides an interface for the activation classes to set the 
    # colormap associated with any internal parcellations    
    def setUseMatplotlibColorMap(self, use, cmap=None):
        self.parc.setUseMatplotlibColorMap(use, cmap)
       
    #------------------------------------------------
    # Activation Staging functionality interface
    #   see: series-activation-map-demo.py
    #------------------------------------------------
    # Return a dictionary for the user to fill out.  
    # The key of the map is an integer stage number.  The values
    # should be a list of strings in this stage
    #
    # Example
    #   mystaging = myActivation.getEmptyStagingMap(3)
    #   myStaging[1] = ['entorhinal','cuneus', 'bankssts']
    #   myStaging[2] = ['parahippocampal']
    #   myStaging[3] = ['insula', 'middletemporal']
    def getEmptyStagingMap(self,nLen):
        return dict((i+1,['unspecified']) for i in range(nLen))
    
    # Activates a staging map (c.f. getStagingMap()) stage.  
    #  Input stmap:
    #       The staging map.  Call getEmptyStagingMap to get an
    #       empty map to fill
    #
    #   Input (integer) stage:
    #       The stage you wish to activate for visualization 
    #       (i.e. the map key)
    #
    #   [Optional] set option appendPrior=True so that all previous stages 
    #       are also activated     
    #
    #   Example: The following code will activate all regions associated to
    #       both stage 1 and 2 of the staging map "myStaging"
    #   
    #       myActivation.setActivationFromStage(myStaging,2,appendPrior=True)
    def setActivationFromStage(self, stmap, stage, appendPrior=False):
        self.parc.resetToDefaultRGB()

        ndxs = []
        
        if appendPrior:
            ndxs = [i+1 for i in range(stage)]
        else:
            ndxs = [stage]
            
        parcValues = self.parc.getRegionValueDictionary(floatval=0.0)
        
        for ndx in ndxs:
            rgns = stmap[ndx]
            for r in rgns:
                parcValues[r] = 1.0
            
        self.parc.setRGBfromValueDictionary(parcValues, min=0.0, max=1.0, setMinToDefaultRGB=True)


    #------------------------------------------------
    # Activation Simulation functionality interface
    #   see: 
    #------------------------------------------------
    
    # returns an empty simulation dictionary with all regional values
    #   initialized to simMinVal
    #
    #   options:
    #   simMinVal (default 0.0): the global minimum of your simulation values.
    #       This should be the minimum for all regions and for all time, etc
    #   simMaxval (default 1.0): the global maximum of your simulation values.
    #       This should be the maximum for all regions and for all time, etc
    #
    #  Note: it is important that your minval and maxval be set to the global
    #   minimum and maximum overall values you plan to represent.  Min and 
    #   max values are used to compute the RGB colors assigned to values.  
    def getEmptySimulationMap(self,simMinval=0.0,simMaxval=1.0):
        res = self.parc.getRegionValueDictionary(floatval=simMinval)
        
        # add the min and max to the dictionary
        res['simulationMinimumValue'] = simMinval
        res['simulationMaximumValue'] = simMaxval
        
        return res
    
    # sets the activation map pursuant to the current state of 
    # a simulation Map.  Use getEmptySimulationMap to create 
    # a simulation map that you can pass to this function
    #
    # Inputs:
    # a simulation map, created from getEmptySimulationMap, containing the 
    #   floating point values (for each parcellation region) to be used in the
    #   activation.   
    def setActivationFromSimulationResult(self, simMap):
        minkey = 'simulationMinimumValue'
        maxkey = 'simulationMaximumValue'
        
        minV = simMap[minkey] 
        maxV = simMap[maxkey]
        
        parcValues = self.parc.getRegionValueDictionary(floatval=minV)
        
        for r in simMap:
            if r!=minkey and r!=maxkey:
                # the rest of the keys are parcellation regions
                parcValues[r] = simMap[r]
        
        # set the parcellation colors for this activation
        self.parc.setRGBfromValueDictionary(parcValues, min=minV, max=maxV, setMinToDefaultRGB=False)
        
        
        
# Lobe activation map for the DesikanKilliany atlas on
# a single hemisphere
class activationDesikanKilliany(activationBase):

    # Initialize the object.  The default is that this
    # object represents a left hemisphere (hemi='Left')
    # for the right hemisphere, initialize with (hemi='Right')
    def __init__(self,hemi='Left'):
        self.dkparc = parc.parcellationDesikanKillianyHemisphere()
        self.actv = [1, 2, 3, 4]


        if hemi == 'Left':
            self.hemi = 'lh'
        elif hemi == 'Right':
            self.hemi = 'rh'
        else:
            print(f"Hemisphere should be Left or Right. Defaulting to Left")
            self.hemi = 'lh'

        super().__init__(self.dkparc)


    # an override of the parcellation CSV writing routine from
    # the base class.  this preprepends parcellation information
    # There is no need to specify a file extension.  Simply provide
    # a name for the file.
    # Example: writeParcellationCSV('/path/to/save/','myactivation')
    def writeActivationCSV(self, path, filename):
        filename = self.hemi + '.aparc.annot.ctab.' + filename
        super().writeActivationCSV(path, filename)


    # Pass in the activation order of the lobes.  These should be
    # unique integers equal to 1, 2, 3 or 4.
    # Example: setActivationOrder(2, 3, 1, 4)
    # means temporal --> frontal --> parietal --> occipital
    def setActivationOrder(self, frontal, parietal, temporal, occipital):
        mplib, pcmap = self.parc.getCurrentMatplotlibColormapConfig()
        
        if frontal not in self.actv:
            print(f"invalid activation order value {frontal} for the Frontal lobe")
        elif parietal not in self.actv:
            print(f"invalid activation order {parietal} for the Parietal lobe")
        elif temporal not in self.actv:
            print(f"invalid activation order {temporal} for the Temporal lobe")
        elif occipital not in self.actv:
            print(f"invalid activation order {occipital} for the Occipital lobe")
        else:
            rgbv = getColor(frontal, 1, 4, matplotlibcmap=mplib, cmap = pcmap)
            self.dkparc.setGroupRGB('Lobe', 'Frontal', rgbv['R'], rgbv['G'], rgbv['B'])

            rgbv = getColor(parietal, 1, 4, matplotlibcmap=mplib, cmap = pcmap)
            self.dkparc.setGroupRGB('Lobe', 'Parietal', rgbv['R'], rgbv['G'], rgbv['B'])

            rgbv = getColor(temporal, 1, 4, matplotlibcmap=mplib, cmap = pcmap)
            self.dkparc.setGroupRGB('Lobe', 'Temporal', rgbv['R'], rgbv['G'], rgbv['B'])

            rgbv = getColor(occipital, 1, 4, matplotlibcmap=mplib, cmap = pcmap)
            self.dkparc.setGroupRGB('Lobe', 'Occipital', rgbv['R'], rgbv['G'], rgbv['B'])
    
    
 

        