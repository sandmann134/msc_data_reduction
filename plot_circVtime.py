import numpy as np
import matplotlib.pyplot as plt

folder_path = "/Users/alexmann/Library/Mobile Documents/com~apple~CloudDocs/Documents/School/Carleton/Masters/Research/KH_circ_log_data/braid_vorticity/"
output_file_path = f"{folder_path}chev_braid_circulations.csv"
out_plus = f"{folder_path}chev_braid_circulations_plus.csv"
out_minus = f"{folder_path}chev_braid_circulations_minus.csv"

# now load the csv file and plot the data:
circ_data = np.loadtxt(output_file_path, skiprows=1, delimiter=',', usecols=(0, 1, 2, 3, 4))
circ_data_plus = np.loadtxt(out_plus, skiprows=1, delimiter=',', usecols=(0, 1, 2, 3, 4))
circ_data_minus = np.loadtxt(out_minus, skiprows=1, delimiter=',', usecols=(0, 1, 2, 3, 4))
# normalize circ_data[:,1] by KH wavelength (0.0355) (correcting to center of braid for +/-)
circ_data_minus[:, 1] = (circ_data_minus[:, 1] + (circ_data[0,1]-circ_data_minus[0,1])) / 0.0355
circ_data_plus[:, 1] = (circ_data_plus[:, 1] - (circ_data_plus[0,1]-circ_data[0,1])) / 0.0355
circ_data[:, 1] = circ_data[:, 1] / 0.0355
# normalize circ_data[:,4] by KH circulation (0.35)
circ_data[:, 4] = circ_data[:, 4] / 0.35
circ_data_plus[:, 4] = circ_data_plus[:, 4] / 0.35
circ_data_minus[:, 4] = circ_data_minus[:, 4] / 0.35
plt.figure()
plt.scatter(circ_data[:, 1], circ_data[:, 4], s=5)
plt.scatter(circ_data_plus[:, 1], circ_data_plus[:, 4], s=5, marker='x')
plt.scatter(circ_data_minus[:, 1], circ_data_minus[:, 4], s=5, marker='v')
plt.xlabel('$t/T_{KH}$')
plt.ylabel('$\\Gamma_{braid}$ / $\\Gamma_{KH}$')
plt.title('Streamwise Evolution of Braid Vortices Circulation')
plt.legend(['Braid Center', 'Downstream 1/3rd', 'Upstream 1/3rd'])
plt.savefig(f"{folder_path}plots/circulation_vs_time.png", bbox_inches='tight', dpi=300)
plt.show()