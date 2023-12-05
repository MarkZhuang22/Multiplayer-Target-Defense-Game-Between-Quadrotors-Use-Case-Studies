import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from envelope import *
from math import pi, atan2, degrees

# Set your initial conditions and parameters here
# r1, r2 = 6.5, 6.54 # barrier

r1, r2 = 6.5, 6.1 # Intruder winning scenario

# r1, r2 = 6.1, 6.6 # Defender winning scenario

sector_angle = pi / 3  # 60 degrees in radians

# Generate the trajectories
traj, ss, phis, rrs, ts = envelope_barrier(r1, r2)

# Create the plot
fig, ax = plt.subplots()

# Plot the trajectories
ax.plot(traj[:, 0], traj[:, 1], 'b-', alpha=0.8, label='Defender')
ax.plot(traj[:, 2], traj[:, 3], color='xkcd:crimson', alpha=0.8, label='Intruder')

# Draw the initial sector representing the capture range and mark initial positions
xd_init, yd_init = traj[0, 0], traj[0, 1]
theta_init = atan2(yd_init, xd_init)
sector = Wedge((xd_init, yd_init), 2, degrees(theta_init - sector_angle / 2),
               degrees(theta_init + sector_angle / 2), color='green', alpha=0.3)
ax.add_patch(sector)

# Loop through the trajectory data
captured = False
for i, (x_def, y_def, x_intr, y_intr) in enumerate(traj):
    # Draw at every 50 steps and the last position
    if i % 50 == 0 or i == len(traj) - 1:
        # Draw the connecting lines
        ax.plot([x_def, x_intr], [y_def, y_intr], 'k--', alpha=0.5)
        
        ax.plot(x_def, y_def, marker='o', color='b')  # Defender position
        ax.plot(x_intr, y_intr, marker='o', color='xkcd:crimson')  # Intruder position

        # Update the sector orientation
        theta = atan2(y_intr - y_def, x_intr - x_def)  # Angle from defender to intruder
        sector = Wedge((x_def, y_def), 2, degrees(theta - sector_angle / 2),
                       degrees(theta + sector_angle / 2), color='gray', alpha=0.3)
        ax.add_patch(sector)

        # Check if intruder is captured
        if is_within_sector(x_def, y_def, x_intr, y_intr, capture_radius=2, sector_angle=sector_angle):
            captured = True
            ax.plot(x_def, y_def, 'b^', markersize=10, label='Defender final')  # Final position marker for defender
            ax.plot(x_intr, y_intr, color='xkcd:crimson', markersize=10, label='Intruder final')  # Final position marker for intruder
            ax.text(x_def, y_def, 'Captured', fontsize=9, verticalalignment='bottom', horizontalalignment='right')
            break

# Add the legend after all items are plotted to ensure all labels are included
ax.legend()

# Set plot details
ax.set_xlabel('x', fontsize=14)
ax.set_ylabel('y', fontsize=14)
ax.grid()
ax.axis('equal')
plt.savefig('traj_sector.png')
plt.show()

