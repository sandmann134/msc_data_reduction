import matplotlib.pyplot as plt

def plot_vorticity(x, y, z):    # plot the used points:
    plt.scatter(x, y, c=z, cmap='jet', s=5, vmin=-2000, vmax=2000)  # Specify the range for the colorbar
    plt.colorbar()
    
    # Set the axis labels and title
    #plt.xlabel('Z')
    #plt.ylabel('Y')
    #plt.title('Interpolated Data')
    plt.xlim([0.01, 0.03])
    plt.ylim([-0.006, 0.01])

    # Show the plot
    return plt.gcf()