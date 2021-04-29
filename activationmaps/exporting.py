# ----------------------------------------------------------------
# Oxford Mathematical Brain Modelling Group
#   This script contains utilities for exporting
#   activation maps to freesurfer using matlab
#       1. Python v3.8 or higher
#       2. Freesurfer v. 7 or higher
#       3. Matlab
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

import os
from activationmaps.activations import *

# This class handles the visualization of annotated csv files using
# freesurfer v7+ (tksurfer) and Matlab
class fsVisualizeActivation:

    def __init__(self):
        print("----------------------------------------------------------")
        print("")
        print("           ____       _____            ____               ")
        print("          / __ \__  _/ ___/__  _______/ _____  _____      ")
        print("         / /_/ / / / \__ \/ / / / ___/ /_/ _ \/ ___/      ")
        print("        / ____/ /_/ ___/ / /_/ / /  / __/  __/ /          ")
        print("       /_/    \__, /____/\__,_/_/  /_/  \___/_/           ")
        print("             /____/                                       ")
        print("")
        print("----------------------------------------------------------")
        print("       Oxford Mathematical Brain Modelling Group          ")
        print("   Portions copyright 2021 G.S. Brennan and A. Goriely    ")
        print("")
        print("              replace_ctab.m is copyrighted by            ")
        print("    Dr. Anderson Winkler and distributed with permission  ") 
        print("                  https://brainder.org                    ")
        print("")
        print("                  PySurfer is distributed                 ")
        print("     according to the GNU GPL v3 Open-Source License      ")
        print("----------------------------------------------------------")

        # freesurfer path
        self.fspath = ''
        self.fsp = False

        # subject path
        self.fssubjp = ''
        self.fssp = False

        # subject name
        self.fssubjn = ''
        self.fssn = False;

        # tksurfer command
        self.tkpreload = ''
        self.tkcmd = 'tksurfer'

    def __fixpath(self,path):
        fixed = path
        if fixed[-1] != '/':
            fixed = fixed + '/'
        return fixed

    def __checkMatlab(self):
        matlabready = False

        if self.fsp:
            matlabready = os.path.exists(self.fspath + "matlab/replace_ctab.m")
            if matlabready == False:
                print("This script requires that the script replace_ctab.m is located")
                print(f"in the directory {self.fspath}" + "matlab")
                print("A copy of replace_ctab.m (copyright Anderson M. Winkler, brainder.org)")
                print("   that has been modified, from the original, to work with")
                print("   Matlab R2020b is distributed with this Python package.")

        return matlabready

    def isReady(self):

        if self.fsp == False:
            print("The freesurfer (root) path has not been set")

        if self.fssp == False:
            print("The freesurfer subject path has not been set")

        if self.fssn == False:
            print("The freesurfer subject name (to visualize) has not been set")
            print(" ** it is assumed that Freesurfer's recon_all command has already")
            print("    been run on any subject that you are trying to visualize")

        return self.fsp and self.fssp and self.fssn


    def setFreesurferPath(self,pathto):
            self.fspath = self.__fixpath(pathto)
            self.fsp = True

    def setFreesurferSubjectPath(self,pathto):
        self.fssubjp = self.__fixpath(pathto)
        self.fssp = True

    def setFreesurferSubjectName(self,sname):
        self.fssubjn = sname
        self.fssn = True

    def setTksurferPreloadCommand(self,cstr):
        print(f"The tksurfer preload command {cstr} will be prepended to all (shell) calls to tksurfer")
        print(f"i.e. the following call will be made for visualization")
        print(f"{cstr} tksurfer [further options]")

        self.tkpreload = cstr


    # pass in an (hemispheric) activation map (c.f. activations.py) for
    # visualization with tksurfer.  It is assumed that you
    # will visualize the left hemisphere (default) but you
    # can override this with the option hemi='Right'.
    # Options:
    #    saveToDisk: set to True to write an image to disk
    #    saveAs: set saveToDisk=True and provide a filename without
    #            extension for the image name (e.g. saveAs='myfile')
    #
    # Note: Saving to disk is currently under development and does not yet work
    #       correctly.  A tcl script needs to be generated and called to do this
    def visualizeHemisphereActivation(self,actv,hemi='Left',saveToDisk=False,saveAs=''):
        bMatlab = self.__checkMatlab()
        bInit = self.isReady()

        hemistr = 'lh'

        if hemi == 'Right':
            hemistr = 'rh'

        fsparc = hemistr + ".aparc.annot"
        fsparcvis = fsparc + '.vis'
        tkparcvis = "aparc.annot.vis"

        # We are ready to go
        if bMatlab and bInit:
            # write the activation map CSV
            ctabpath = self.fssubjp + self.fssubjn + "/label/"
            actv.writeActivationCSV(ctabpath, 'vis')
            # We don't necessarily know if the user has overridden the writeActivationCSV
            # function so we ask the base class for the filename it wrote
            cstabcsv = actv.getLastFileWritten()

            # the matlab command string
            matlabcmd = f"matlab -batch \"replace_ctab('{ctabpath + fsparc}','{cstabcsv}','{ctabpath + fsparcvis}')\""

            # execute the matlab command
            os.system(matlabcmd)

            # the tksurfer command string
            tksrfcmd = str(self.tkpreload + ' ' + self.tkcmd).strip()
            tksrfcmd = tksrfcmd + f" {self.fssubjn}" + f" {hemistr}" + f" pial -annotation {tkparcvis}"

            if saveToDisk:
                tksrfcmd = tksrfcmd + f" save_tiff {saveAs}.tiff"

            os.system(tksrfcmd)

            # Cleanup: remove the csv tab file we created
            rmcmd = f"rm {self.fspath + self.fssubjn}" + f"/label/{fsparcvis}"

            os.system(rmcmd)