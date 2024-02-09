import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import vorticity_fxns as fxn

folder_path = "/Users/alexmann/Library/Mobile Documents/com~apple~CloudDocs/Documents/School/Carleton/Masters/Research/KH_circ_log_data/braid_vorticity/"
output_file_path = f"{folder_path}chev_braid_circulations.csv"

# Open the file in write mode
with open(output_file_path, "w") as f_out:
    # Write headers to the file
    f_out.write("timestep, x [m], y [m], z [m], circulation [m^2/s], num_points_used, furthest used point [m]\n")

t_0 = 19084
t_f = 19084
dt = 8          # timesteps between exported files

timestep = t_0
while timestep <= t_f:
    # Define the path to the plane data
    data_path = f"/Users/alexmann/Library/Mobile Documents/com~apple~CloudDocs/Documents/School/Carleton/Masters/Research/KH_circ_log_data/braid_vorticity/temptrace_braid_plane_chev_{timestep}.csv"
    # Read the plane data
    plane_data = np.loadtxt(data_path, skiprows=6, delimiter=',', usecols=(4, 7, 8, 9))

    min_y = np.min(plane_data[:, 2])
    max_y = np.max(plane_data[:, 2])
    min_z = np.min(plane_data[:, 3])
    max_z = np.max(plane_data[:, 3])
#    print(f'min_y = {min_y}, max_y = {max_y}')
#    print(f'min_z = {min_z}, max_z = {max_z}')
    # Interpolate the data onto a regular grid
    # Define the grid points where you want to interpolate the data
    y_grid, z_grid = np.mgrid[-0.01:0.01:200j, 0.01:0.04:200j]
    dy = y_grid[1, 0] - y_grid[0, 0]
    dz = z_grid[0, 1] - z_grid[0, 0]

    # Interpolate the data
    interpolated_data = griddata(plane_data[:, 2:4], plane_data[:, 0], (y_grid, z_grid), method='cubic')

    # plot 2d data points using coloured scatter plot from plt library 

    # Plot the interpolated data
    plt.figure()
    full_plot = fxn.plot_vorticity(z_grid.flatten(), y_grid.flatten(), interpolated_data.flatten())
    plt.savefig(f"{folder_path}plots/full_plot_{timestep}.png", bbox_inches='tight', dpi=300)

    # WORKING HERE               ---***---***---
    # first break the data into 8 equally sized z-sections based on the min and max z values, then identify 
    # the vortice centers based on max vorticity magnitude in each section.  Then, for each vortice center, 
    # calculate the circulation by integrating around the vortice center and within it's 8th section, 
    # disregarding any points with vorcitity of an opposite sign or once the magnitude is less than 5% of the
    # maximum.  Then print to console the maximum distance from vortex center to furtherest 'counted' point,
    # as well as the number of points which were used to calculate the circulation.  Then, output the y,z 
    # coordinates of the center(s) along with the vortex circulation(s) to a csv file.
    # Calculate the number of sections
    num_sections = 8

    # Calculate the section boundaries
    section_boundaries = np.linspace(min_z, max_z, num_sections + 1)
    section_dz = section_boundaries[1] - section_boundaries[0]
#    print(f"Section boundaries: {section_boundaries}")

    # create new array for all points which are used so that they can be plotted afterwards:
    used_points = np.empty((0, 4), float)

    # Iterate over each section
    for section_index in range(num_sections):
    #    print(f"Section {section_index}")
        # Get the data points in the current section
        section_data = plane_data[(plane_data[:, 3] >= section_boundaries[section_index]-section_dz/6) \
                        & (plane_data[:, 3] < section_boundaries[section_index + 1]+section_dz/6)]   # add 1/8 dz to each side of section to ensure all points are included
    #    print(f"Number of points in section: {section_data.shape[0]}")

        # Find the vortex center with the maximum vorticity magnitude in the section
        max_vorticity_index = np.argmax(abs(section_data[:, 0]))
        max_vorticity = section_data[max_vorticity_index, 0]
        vortex_center = section_data[max_vorticity_index, 1:4]
        # print vortex center location:
    #    print(f"Max vorticity: {max_vorticity:.2f}")
    #    print(f"Vortex center: {vortex_center}")

        # Calculate the circulation for the vortex center
        circulation = 0.0
        counted_points = 0
        max_distance = 0.0

        for point in section_data:
            vorticity = point[0]
            distance = np.linalg.norm(point[2:4] - vortex_center[1:3])

            if vorticity*max_vorticity > 0 and abs(vorticity)>abs(max_vorticity)*0.05 and distance <= 2.5*abs(section_boundaries[1]-section_boundaries[0])\
                and abs(point[3]-vortex_center[2]) < 0.5*abs(section_boundaries[1]-section_boundaries[0]):         # same sign, >5% of max vort., distance<2x section width
                circulation += vorticity*dy*dz
                counted_points += 1
                # add used point to array for plotting:
                used_points = np.append(used_points, np.array([point]), axis=0)

                # trying to see why used points seem to not be evenly spread
                #if counted_points < 20:
                #    print(f"Point: {point}")
                #    print(f"used_points[-1]: {used_points[-1,:]}")

                if distance > max_distance:
                    max_distance = distance

    #    print(f"Circulation: {circulation:.5f}")
    #    print(f"Number of points used: {counted_points}")
    #    print(f"Maximum distance: {max_distance:.5f}")

        # Output the y, z coordinates of the vortex center and the circulation to a csv file
        with open(output_file_path, "a") as f_out:
            f_out.write(f"{timestep}, {vortex_center[0]}, {vortex_center[1]}, {vortex_center[2]}, \
                        {circulation}, {counted_points}, {max_distance}\n")

    # plot the used points:
    plt.figure()
    used_plot = fxn.plot_vorticity(used_points[:, 3], used_points[:, 2], used_points[:, 0])
    plt.savefig(f"{folder_path}plots/used_plot_{timestep}.png", bbox_inches='tight', dpi=300)
    #plt.show()

    timestep += dt

