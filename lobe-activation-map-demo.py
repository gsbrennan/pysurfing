# ----------------------------------------------------------------
# Oxford Mathematical Brain Modelling Group
#   Lobe activation map script - This script requires the
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

    #tkpreload = ''
    tkpreload = "LD_PRELOAD=/opt/matlab/sys/opengl/lib/glnxa64/libGL.so.1"

    # Now, we create the visualization object to visualize our activation map
    #    and tell it about our freesurfer configuration and any preloading
    #    command necessary
    visIt = fsVisualizeActivation()
    visIt.setFreesurferPath(freesurferPath)
    visIt.setFreesurferSubjectPath(freesurferSubjectPath)
    visIt.setFreesurferSubjectName(freesurferSubject)
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







# Main function - this is where the program begins execution
if __name__ == "__main__":

    # Create an activation map.  We will use the Desikan-Killiany
    # activation map here and specify the activation order
    # of the Frontal, Parietal, Temporal, and Occipital lobes
    # (in that order) as integers.
    myActivationMap = activationDesikanKilliany()

    # [Optional] Set an alternative matplotlib color map for the activation
    viridis = cm.get_cmap('viridis')
    myActivationMap.setUseMatplotlibColorMap(True, cmap=viridis)

    # Set the activation order (according to the current internal 
    #  color mapping scheme)
    myActivationMap.setActivationOrder(2, 1, 3, 4)

    # visualize the map (see the function above) and show the color bar
    vis(myActivationMap, showColorBar=False)
    
    # Show the color bar (optional)
    # myActivationMap.showActivationColorbar(30)
