# ----------------------------------------------------------------
# Oxford Mathematical Brain Modelling Group
#   Simulation activation map demo script - This script requires the
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




# Main function - this is where the program begins execution
if __name__ == "__main__":
    # The context of this demonstration is using freesurfer to visualize
    # results from a network neurodegneeration simulation.  The idea is that
    # one has a system of coupled non-linear ordinary differential equations
    # evolving on a network graph created from a (structural) parcellation
    # of the brain.  An example of such a system is the prion-like evolution 
    # of a toxic protein (misfolded Amyloid-beta, tau, alpha-synuclein, 
    # TDP-43, etc) in some neurodegenerative disease.
    #
    # for instance, c.f.
    #   doi: 10.1103/PhysRevLett.121.158101
    #   doi: 10.1098/rsif.2019.0356
    #   doi: 10.1101/692038
    #   doi: 10.1371/journal.pcbi.1008267
    #   doi: 10.1093/brain/awy059
    #    
    # Moreover, it is assumed that the regions of this simulation can, for 
    # this demonstration, be mapped onto the Desikan Killiany atlas used by 
    # freesurfer.  We will assume that the simulation produces, for each time 
    # we wish to plot, an average (normalized) concentration (i.e. between 0.0 
    # and 1.0) for the DK atlas regions.
    
    # define the activation map and the desired color scheme (note that if 
    # we don't specify a colorscheme then a default blue-to-red colorscheme
    # is used for visualization)
    myActivationMap = activationDesikanKilliany()
    mycmap = cm.get_cmap('jet')
    myActivationMap.setUseMatplotlibColorMap(True, cmap=mycmap)
    
    # Now lets make some synthetic average concentration data from our 
    # simulation.  Lets suppose that some toxic seeds start off in the 
    # entorhinal cortex and spread to nearby regions. We assume that 
    # the minimum simulation value is 0.0 and the 
    # maximum is 1.0 and that we have data for 5 time-points such that
    # 0<= t0 < t1 < t2 < t3 < t4 < t5 < Tfinal
    
    simValues = {'entorhinal':[0.1, 0.23, 0.28, 0.52, 0.98], 
                 'parahippocampal': [0.0, 0.1, 0.18, 0.44, 0.7], 
                 'inferiortemporal': [0.0, 0.07, 0.12, 0.32, 0.6],
                 'middletemporal': [0.0, 0.04, 0.13, 0.28, 0.55], 
                 'superiortemporal': [0.0, 0.09, 0.22, 0.45, 0.62],
                 'inferiorparietal': [0.0, 0.0, 0.1, 0.18, 0.33], 
                 'superiorparietal': [0.0, 0.0, 0.06, 0.15, 0.28],
                 'lateraloccipital': [0.0, 0.0, 0.02, 0.08, 0.13], 
                 'lingual': [0.0, 0.0, 0.01, 0.07, 0.11],
                 'cuneus': [0.0, 0.0, 0.01, 0.06, 0.10]}
 
    
    # We will ideally want to generate 5 images; one for each time across 
    # all regions.  We can do this by looping over the time data and using 
    # the activation map's Simulation interface functionality.  First, we 
    # get an empty simulation map.  This map contains all of the region labels 
    # in our (DK) parcellation and initializes all of the values to zero.
    # Since our global (over all time) maximum for our simulation is 1.0 
    # an our minimum is 0.0 we can get the initial simulation map as follows
    simulationResults = myActivationMap.getEmptySimulationMap(simMinval=0.0,simMaxval=1.0)
    
    # Note that we used the options simMinval and simMaxval, above, to indicate 
    # our global min and max.  The default values are 0.0 and 1.0 (so this was 
    # not necessary) but these might be different for your simulation and should 
    # bet set accordingly.
    
    # Now we loop over our synthetic simulation data and visualize each step 
    # of our simulation results.  For regions where we have no synthetic data,
    # it is assumed that the (concentration) values never change from the 
    # minimum value (simMinval) specified.
    
    nSimTimes = 5
    for t in range(nSimTimes):
        
        # set the values in the regions where the concentration is changing
        for region in simValues:
            simulationResults[region] = simValues[region][t]
        
        # update the activation map for this simulation time (t)
        myActivationMap.setActivationFromSimulationResult(simulationResults)
        
        #visualize the results for time `t' in using freesurfer's tksurfer
        # you can manipulate the visualization, as desired, and save the 
        # resulting figure for your publication.
        vis(myActivationMap)
   
    # Show the activation color bar (optional) 
    # myActivationMap.showActivationColorbar(30)
