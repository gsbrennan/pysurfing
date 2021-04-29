### PySurfing - Coloring FreeSurfer brains with Python

<p align="center">
  <img width="479" height="420" src="https://github.com/gsbrennan/pysurfer/blob/main/pysurfer.jpg?raw=true">
</p>

In a [2011 blog posting](https://brainder.org/2011/07/05/freesurfer-brains-in-arbitrary-colours/) the topic of coloring FreeSurfer segmented brains, with arbitrary RGB values, was broached.  Applications such as shading regions to show significant p-values derived from surface area comparisons, or differences in cortical thickness, between groups were discussed.  This manual approach is immensely useful for generating figures with anatomical clarity.  However, if a larger number of figures are desired the manual approach can become time-consuming.  

What if one wanted to visualize the evolution of misfolded proteins, as they reproduced and spread throughout the brain, using FreeSurfer segmented brains? Researchers have used [network mathematical models](https://royalsocietypublishing.org/doi/full/10.1098/rsif.2019.0356) to study these types of "network neurodegeneration" problems; including the [longitudinal progression of TAU PET data](https://www.frontiersin.org/articles/10.3389/fnins.2020.566876/full).  A simple network mathematical model of misfolded protein propagation is the [Fisher-Kolmogorov](https://doi.org/10.1098/rsif.2019.0356) model evolving on structural connectome graph of the brain.  This model takes the form 

<p align="center">
<img src="https://render.githubusercontent.com/render/math?math=%5Cfrac%7B%5Cpartial%20p_i%7D%7B%5Cpartial%20t%7D%20%3D%20-%5Crho%5Csum_%7Bj%3D1%7D%5E%7B%7CV%7C%7D%5Cmathbf%7B%5Cmathcal%7BL%7D%7D_%7Bij%7D%5C%2Cp_j%20%20%2B%20%5Calpha%20p_i%20%5Cleft(1-p_i%5Cright)%0A%20">
</p>

where <img src="https://render.githubusercontent.com/render/math?math=%5Cvert%20V%20%5Cvert"> denotes the number of anatomical regions, <img src="https://render.githubusercontent.com/render/math?math=%5Cmathcal%7BL%7D%0A%20"> denotes the *graph Laplacian tensor*, <img src="https://render.githubusercontent.com/render/math?math=%5Crho"> is a characteristic diffusion constant, <img src="https://render.githubusercontent.com/render/math?math=%5Calpha"> is a growth coefficient and <img src="https://render.githubusercontent.com/render/math?math=p_i%20"> represents the concentration of a misfolded protein in a specific anatomical region (corresponding to the index <img src="https://render.githubusercontent.com/render/math?math=i">).  There are two primary challenges that arise, here, when using replace_ctab.m manually:

1. The mapping from a given set of scalar concentration values to a desired RGB color scheme may not be readily apparent 
2. One may seek to visualize numerous images; this can arise, for instance, when on has generated solution data across a large number of mathematical simulation time steps.

In the context of network neurodegeneration modeling, these two difficulties mean that the manual approach to a FreeSurfer-based visualization can be somewhat difficult to efficiently manage.  An Oxford mathematician, [Ms. Georgia S. Brennan](https://twitter.com/gsbrennan), has recently released the first version of her **PySurfing** toolkit; she also credits support from her two doctoral advisers, [Prof. Alain Goriely](http://goriely.com/) and [Prof. Marie E. Rognes](http://marierognes.org/), as well as [Dr. Travis B. Thompson](https://twitter.com/mathemology).  The need for **PySurfing** originated as part of her desire to more readily visualize her novel network mathematical modeling results on anatomical domains.   

<p align="center">
  <img width="1000" height="300" src="https://github.com/gsbrennan/pysurfer/blob/main/img/simulationactivation.jpg?raw=true">
</p>

**PySurfing** is a functionality-added, wrapper extending the [original 2011 approach](https://brainder.org/2011/07/05/freesurfer-brains-in-arbitrary-colours/), which uses the replace_ctab.m Matlab script to automate the visualization of FreeSurfer brains using the Python language.  The current release of **PySurfing** is intended for use with FreeSurfer 7, Matlab 2020b (or Matlab 2021a) and Python 3.8.  **PySurfing** provides several built-in interfaces to make FreeSurfer visualization more accessible.  These include 

1. The use of any color map provided by the widely-used matplotlib library
2. Arbitrary region coloring using the anatomical names of the Desikan-Killiany atlas
3. Lobe activation maps 
4. Staging progression maps (such as Braak Tau staging)
5. Support for visualizing sequences of values generated via mathematical simulations

At the time of writing, **PySurfing** comes with three demonstration scripts, and a step-by-step documentation guide, to get you up-and-running with accessible FreeSurfer visualizations from Python.  The main **PySurfing** project repository is available at [Ms. Brennan's github repository](https://github.com/gsbrennan).  


###### Archived copies of research software releases, including **PySurfing**, can be found on the [Oxford Mathematical Brain Modelling Group's](https://github.com/OxMBM) organizational repository page. 

