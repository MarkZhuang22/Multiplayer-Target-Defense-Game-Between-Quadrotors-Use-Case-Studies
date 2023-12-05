import matplotlib 
matplotlib.rc('xtick', labelsize=14) 
matplotlib.rc('ytick', labelsize=14)
from celluloid import Camera
from envelope import *
from overall_plot import triag_cnstr_3, triag_cnstr_2, triag_cnstr_1, plot_bds, plot_orbit
import matplotlib.tri as tri

if __name__ == '__main__':

    # Define initial conditions for the scenario (barrier case)
	r1, r2 = 6.5, 6.54 # barrier
	# resfig = [0, 15, 65, 89]
	# r1, r2 = 6.5, 6.1 # iwin
	# resfig = [0, 20, 50, 56]
	# resfig = [0, 50, 90, 105, 110, 195, 210, 230, 240, 1200]
	# r1, r2 = 6.1, 6.6 # dwin
	# resfig = [0, 50, 90, 105, 110, 195, 210, 230, 240, 1200]

    # Generate the trajectory, states, control angles, ratios, and time stamps for the given scenario
	traj, ss, phis, rrs, ts = envelope_barrier(r1, r2)

    # Create a matplotlib figure with two subplots
	fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))
	camera = Camera(fig) # Initialize the camera for animation

    # Set labels and grid for the first subplot
	ax1.set_xlabel('x', fontsize=14)
	ax1.set_ylabel('y', fontsize=14)
	ax1.grid()
	ax1.axis('equal')

    # Set labels and grid for the second subplot (vectogram)
	ax2.set_xlabel(r'$\dot{\rho}_D$', fontsize=16)
	ax2.set_ylabel(r'$\dot{\rho}_I$', fontsize=16)
	ax2.grid()
	ax2.axis('equal')

	# plt.subplots_adjust(left=0.05, bottom=0.15, hspace=0.5)
	plt.subplots_adjust(left=0.15, right=0.9, wspace=.3, bottom=0.15)

	# plt.show()

    # Iterate over each time step to create frames for the animation
	for i, (s, x) in enumerate(zip(ss, traj)):
		print(i)
		ax1.plot(traj[:,0], traj[:,1], 'b', alpha=0.8, linestyle='--', marker='o', markevery=5000000)
		ax1.plot(traj[:,2], traj[:,3], color='xkcd:crimson', alpha=0.8, linestyle='--', marker='o', markevery=5000000)
		ax1.plot(x[0], x[1], marker='o', color='b')
		ax1.plot(x[2], x[3], marker='o', color='xkcd:crimson')
		draw_vecgram_animation(ax2, s[0], s[2])
		ax1.legend(['D', 'I'], fontsize=11, loc="upper right")	
		camera.snap()

    # Create and save the animation
	animation = camera.animate(interval=100)  
	animation.save('barrier.mp4')