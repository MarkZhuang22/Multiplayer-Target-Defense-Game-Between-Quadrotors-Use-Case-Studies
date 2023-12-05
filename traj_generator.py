from envelope import *

# Generating a range of values for r0
r0s = np.linspace(r, 7*r, 13)  # r is the capture range imported from envelope.py

# Loop through the generated range of r0
for r0 in r0s:
    # Calculate lower and upper bounds for r1 based on r0
    r1l, r1u = (r0 - r)/2, (r0 + r)/2

    # Generate trajectories for different r1 values within the calculated bounds
    for r1 in np.linspace(r1l+0.1, r1u-0.1, 13):
        r2 = r0 - r1  # Calculate r2 based on r1 and r0

        # Ensure that the computed r1 and r2 are valid for the game's geometry
        if abs((r1**2 + r2**2 - r**2)/(2*r1*r2)) < 1:
            print('new plot')
            # Generate the trajectory and related data for given r1 and r2
            traj, ss, phis, rrs, _ = envelope_barrier(r1, r2)      

# Additional calls to envelope_barrier with specific r1, r2 values
traj, ss, phis, rrs, _ = envelope_barrier(6.1, 6.6)       # Defender winning case
traj, ss, phis, rrs, _ = envelope_barrier(6.5, 6.54)      # Barrier case
traj, ss, phis, rrs, _ = envelope_barrier(6.5, 6.1)       # Intruder winning case
