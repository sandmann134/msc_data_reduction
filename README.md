# msc_data_reduction

This txt file includes a description of the function, use, and linking of the python
scripts in this folder.

braid_circ.py:

This script takes CFD data from streamwise planes contained in separate CFD files 
stored in folder_path, identifies and calculates the circulation of the vortices
contained in those planes, and writes the results to an output .csv file in the 
form of 'timestep, x (plane), y (vortex center), z (vortex center), circulation,
number of points included in circ calc, and distance to furthest used point.

While it is doing these calculations, the script also produces coloured vorticity
plots for both 1) all data for each plane and 2) the data counted as 'part' of 
each vortex (via a fxn written separately in vorticity_fxns.py), and saves these
plots.

See the script and included comments for a more detailed description of the program
logic.


vorticity_fxns.py:

As referenced above, this simply contains some separated functions which are used in
vorticity and circulation analysis.


plot_circVtime.py
