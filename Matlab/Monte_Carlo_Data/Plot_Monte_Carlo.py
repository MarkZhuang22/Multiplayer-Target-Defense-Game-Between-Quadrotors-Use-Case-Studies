import matplotlib.pyplot as plt
from scipy.io import loadmat
import os

# Define the directory where your .mat files are stored
directory = '/Users/markzhuang/Desktop/Thesis/Thesis_research/Matlab'

# Fixed positions for Defender 2 and Intruder
D2_position = [0, 0]  # [x, y]
I_position = [5, 5]  # [x, y]

# Plot settings
colors = {'D1': 'red', 'D2': 'blue', 'I': 'green'}

# Function to plot positions
def plot_positions(region):
    plt.figure()
    for file in os.listdir(directory):
        if file.startswith(f"successful_conditions_region{region}") and file.endswith(".mat"):
            data = loadmat(os.path.join(directory, file))
            for condition in data['successful_conditions']:
                plt.plot(condition[3], condition[2], 'o', color=colors['D1'], label='Defender 1' if 'D1' not in locals() else "")
                locals()['D1'] = True

    # Plot fixed positions for Defender 2 and Intruder
    plt.plot(D2_position[0], D2_position[1], 'o', color=colors['D2'], label='Defender 2')
    plt.plot(I_position[0], I_position[1], 'o', color=colors['I'], label='Intruder')

    plt.title(f'Positions in Region {region}')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.legend()
    plt.grid(True)

    # Set fixed axis ranges
    plt.xlim(0, 10)
    plt.ylim(0, 10)

    # Set the aspect of the plot to be equal
    plt.gca().set_aspect('equal', adjustable='box')

    # Show the plot with the set axis limits
    plt.show()

# Plot for each region
for region in [1, 2, 3]:
    plot_positions(region)
