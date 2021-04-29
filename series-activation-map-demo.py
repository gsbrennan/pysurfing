# ----------------------------------------------------------------
# Oxford Mathematical Brain Modelling Group
#   Series activation map demo script - This script requires the
#   following software / packages to be present
#       1. Freesurfer v.7  (https://surfer.nmr.mgh.harvard.edu/fswiki/rel7downloads)
#       2. Matlab
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


from matplotlib import cm
from activationmaps.exporting import fsVisualizeActivation
from activationmaps.activations import activationDesikanKilliany

#-----------------------------------------------------------------
# This function demonstrates how to visualize an activation map
# with tksurfer
def vis(activationMap, showColorBar=False):
    # Now we will visualize the activation map using freesurfer's
    # tksurfer command line tool.  Once tksurfer has opened, you can
    # manipulate the view and save the figure.
    # -- -- -- -- -- --
    #  NOTE: If you are using this script remotely (for instance
    #    connected to a machine using X2go or similar) then
    #    you may need to preprend a string to load libGL so that
    #    tksurfer displays output correctly over X2go (or similar).
    #
    #    This is demonstrated below but you may need to change the
    #    path to point to libGL on the system to which you
    #    are connected

    # Set this string to the (absolute) path to where freesurfer
    # is installed on your machine (this is the same directory
    # as $FREESURFER_HOME)
    freesurferPath = "/scratch/oxmbm-shared/freesurfer/"

    # Set this string to the (absolute) path to where the freesurfer
    # subject directory.  (This is the same directory as
    # $SUBJECTS_DIR)
    freesurferSubjectPath = freesurferPath + "subjects/"

    # Set this string to the name of the subject you want to use
    # to view the visualization of the activation map.  It is assumed
    # that a full --recon_all has already been done for this subject
    # (using freesurfer).  If not, please do this beforehand.
    freesurferSubject = "bert"

    # This is the preload command which is often needed for
    # remote clients.  If you are running locally (on your laptop, etc)
    # then simply set this to an empty string. i.e. ''

    #using tksurfer on your local machine
    #tkpreload = '' 
    
    # may be necessary when using tksurfer remotely (X2go or similar)
    # (your path to libGL.so may differ -- change the line below accordingly)
    tkpreload = "LD_PRELOAD=/opt/matlab/sys/opengl/lib/glnxa64/libGL.so.1"

    # Now, we create the visualization object to visualize our activation map
    #    and tell it about our freesurfer configuration and any preloading
    #    command necessary
    visIt = fsVisualizeActivation()
    visIt.setFreesurferPath(freesurferPath)
    visIt.setFreesurferSubjectPath(freesurferSubjectPath)
    visIt.setFreesurferSubjectName(freesurferSubject)
    
    # this line is only necessary if you need to preprend a preload command
    # to tksurfer.  Otherwise, it is not needed (i.e. if executing tksurfer
    # on your local workstation / laptop,  etc)
    visIt.setTksurferPreloadCommand(tkpreload)

    # Now we are ready to visualize.
    # Interactive visualization on the left hemisphere
    #   note: we can use the option hemi='Right' to visualize the
    #   right hemisphere if we desire
    visIt.visualizeHemisphereActivation(activationMap)

    # ---------
    # uncomment these lines to show the colorbar for
    # the acitvation map.  This is useful if you want to
    # put the colorbar in a publication figure.  You can
    # change the width of the colorbar by passing in a positive
    # integer.  Larger integers generate thicker color bars.
    #
    if showColorBar:
        activationMap.showActivationColorbar(30)
#-----------------------------------------------------------------




#-----------------------------------------------------------------
def demoSingleRegionActivation():

    # Create an activation map.  We will use the Desikan-Killiany
    # Lobe activation map here.  We demonstrate activation of a single
    # parcellation region using the anatomical name
    
    
    # activation functionality; our motivation will be to highlight 
    # the Braak stages used in a recent publication on tau seed 
    # staging along the Braak pathway
    #    
    myActivationMap = activationDesikanKilliany()
  
    # [Optional] Set an alternative matplotlib color map for the activation
    viridis = cm.get_cmap('viridis')
    myActivationMap.setUseMatplotlibColorMap(True, cmap=viridis)
    
    
    # Activation maps often implement higher-order functionality (such as 
    # setting regional colors) but we can also retrieve the activation map's 
    # underlying parcellation object for direct manipulation.  We can then
    # activate our map with the parcellation values.  
    parc = myActivationMap.getParcellation()
    
    # Set all of the regions in the parcellation to the same color
    parc.resetToDefaultRGB()
    
    # Now we retrieve a dictionary whose keys are the Desikan Killiany 
    # region names and whose values correspond to a floating point 
    # for each region.  These could come from the result of a simulation
    # or we can simply use them as tags, etc.  We specify that the 
    # initial value for all regions should be 0.0
    parcValues = parc.getRegionValueDictionary(floatval=0.0)


    # We could print the keys of parcValues to see the region labels 
    # if we wanted to (or did not know what they were)
    #print(*parcValues, sep='\n')

    # Set the entorhinal cortex region to 1.0
    parcValues['entorhinal'] = 1.0

    
    # Now we pass the dictionary back into the parcellation to 
    # set the coloring according to our changes.  We specify 
    # that the value-based coloring should be done with respect to a 
    # minimum of 0 and a maximum of 1.0
    
    # We can specify the option setMinToDefaultRGB=True to set all 
    parc.setRGBfromValueDictionary(parcValues, min=0.0, max=1.0, setMinToDefaultRGB=True)

    # Now we visualize the activation map and also show the colorbar
    vis(myActivationMap)
#-----------------------------------------------------------------    


#-----------------------------------------------------------------
def demoStagingActivation():
    # comments in this function are reduced for functionality that
    # has already been presented in other examples     
    myActivationMap = activationDesikanKilliany()
  
    purple = cm.get_cmap('Purples')
    myActivationMap.setUseMatplotlibColorMap(True, cmap=purple)
    
    # there are 6 distinct stages in Devos' Braak staging map
    # c.f. Fig 3 in 
    # https://doi.org/10.3389/fnins.2018.00267
    #
    # These can be amalgamated into 5 regions
    # using a Lausanne 2018 parcellation c.f. Table 4 in 
    # https://www.biorxiv.org/content/10.1101/2021.01.21.427609v2
    #
    # The DK atlas does not contain subcortical regions, so we can 
    #   visualize 4 stages (stage I, III, IV, and V from the paper above) 
    #   using the DK atlas with freesurfer
    devosBraakStaging = myActivationMap.getEmptyStagingMap(4)
    
    # Now we specify the DK atlas region names for each stage
    
    # stage I
    devosBraakStaging[1] = ['entorhinal'] 
    
    # stage III
    devosBraakStaging[2] = ['parahippocampal'] 

    # stage IV
    devosBraakStaging[3] = ['rostralanteriorcingulate', 'caudalanteriorcingulate']
    
    # stage V
    devosBraakStaging[4] = ['cuneus', 'pericalcarine', 'lateraloccipital', 'lingual']
    
    # now we call on Freesurfer to visualize each stage in the activation
    # sequence above. We use the appendPrio=True option to show all previous
    # stages as also activated (i.e. progression)
    for i in range(4):
        myActivationMap.setActivationFromStage(devosBraakStaging, i+1, appendPrior=True)
        vis(myActivationMap)

    # Show the color bar (optional)
    myActivationMap.showActivationColorbar(30)
    
#-----------------------------------------------------------------

# Main function - this is where the program begins execution
if __name__ == "__main__":
    
    #----------
    # Activate a single region (entorhinal cortex) using
    # the activation map's parcellation directly
    #----------
    # demoSingleRegionActivation()
    
    
    #-----------
    # Demonstrate a (histopathological) Staging sequence inspired by 
    # Tau Braak seed staging in Alzheimer's disease
    #  c.f. doi: 10.3389/fnins.2018.00267
    #
    # Uses the activation map's 'Staging map' interface
    #-----------
    demoStagingActivation()
