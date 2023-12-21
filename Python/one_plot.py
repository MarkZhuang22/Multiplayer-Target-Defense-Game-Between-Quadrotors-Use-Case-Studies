import matplotlib 
matplotlib.rc('xtick', labelsize=14) 
matplotlib.rc('ytick', labelsize=14)
from matplotlib.patches import Wedge
from envelope import *
from overall_plot import *
import matplotlib.tri as tri
from math import pi

if __name__ == '__main__':
    # Define initial conditions for rho_D and rho_I based on the scenario

	# r1, r2 = 6.5, 6.54 # barrier
	# resfig = [0, 15, 65, 89]
	# r1, r2 = 6.5, 6.1 # Intruder winning scenario
	# resfig = [0, 20, 50, 56]
	# resfig = [0, 50, 90, 105, 110, 195, 210, 230, 240, 1200]
	r1, r2 = 6.1, 6.6 # Defender winning scenario
	# resfig = [0, 50, 90, 105, 110, 195, 210, 230, 240, 1200]


	########################## optimal trajectory like Figure 14 ###########################
	traj, ss, phis, rrs, ts = envelope_barrier(r1, r2)

    # Plot trajectories for defender and intruder
	fig, ax = plt.subplots()
	ax.plot(traj[:,0], traj[:,1], 'b', alpha=0.8, marker='o', markevery=50)
	ax.plot(traj[:,2], traj[:,3], color='xkcd:crimson', marker='o', alpha=0.8, markevery=50)
	for i, x in enumerate(traj):
		if i%50 == 0:
			ax.plot([x[0], x[2]], [x[1], x[3]], 'k--')
			ax.plot(x[0], x[1], marker='o', color='b')
			ax.plot(x[2], x[3], marker='o', color='xkcd:crimson')
	# ax.plot(circ[:,0], circ[:,1], 'r-')
	plt.xlabel('x', fontsize=14)
	plt.ylabel('y', fontsize=14)
	ax.grid()
	ax.axis('equal')
	ax.legend(['D', 'I'], fontsize=14)
	plt.savefig('traj.png')
	plt.show()

	########################## phi_D^ast, like Figure 13###########################
	# fig, ax = plt.subplots()
	# ax.plot(ts, np.asarray(phis)*180/pi, 'b.-', markevery=5)
	# plt.xlabel('time', fontsize=14)
	# plt.ylabel(r'$\phi_D^\ast(^\circ)$', fontsize=14)
	# ax.grid()
	# plt.show()

	########################## flow field ###########################
	# fig, ax = plt.subplots()
	# plot_bds(ax, triag_cnstr_3)
	# plot_bds(ax, triag_cnstr_2)
	# plot_bds(ax, triag_cnstr_1)
	# # plot_bds(ax, stable_orbit)
	# plot_orbit(ax)
	# ax.plot(ss[:,0], ss[:,2], 'bo-', ms=3, markevery=10)
	# 	# ax.plot(x[:,2], x[:,3])
	# cntr = ax.contour(xi, yi, zi, [0])
	# ax.grid()
	# ax.axis('equal')
	# ax.set_xlim([0, 15.])
	# ax.set_ylim([0, 15.])
	# plt.savefig('state.png')
	# plt.show()

	########################## vecgram, like Figure 12 ###########################
	# at each time step, there is a vectogram. we only pick some representative ones to show. 
	# k = 0
	# for i, s in enumerate(ss):
	# 	print(i)
	# 	# print(i)
	# 	# if i in [0, 15, 65, 89]:
	# 	# 	print(k)
	# 	# 	print(i)
	# 	# if i%10 == 0:
	# 	# if i in resfig:
	# 	draw_vecgram(s[0], s[2], i, 0)
		
	# 		# time.sleep(.1)
	# # plt.show()
