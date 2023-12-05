import matplotlib 
matplotlib.rc('xtick', labelsize=14) 
matplotlib.rc('ytick', labelsize=14) 
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import os
import csv
import numpy as np
from math import cos, sin, acos, sqrt, tan
# from vecgram import semipermeable_r, velocity_vec, get_phi, get_phi_max
from vecgram import *

from Config import Config
r = Config.CAP_RANGE # Capture range of the defender
R = Config.TAG_RANGE # Radius of the target area
vd = Config.VD       # Defender's velocity
vi = Config.VI       # Intruder's velocity
gmm = acos(vd/vi)

# Define the minimum and maximum capture radii for the intruder and defender
rIcap_min, rIcap_max = r/(sin(gmm)), r/(1-cos(gmm))
rDcap_min, rDcap_max = rIcap_min*(vd/vi), rIcap_max*(vd/vi)
r1_min = r/tan(gmm)  # Minimum radius for defender
r2_min = r/sin(gmm)  # Minimum radius for intruder

def save_traj_plot(traj, dirc):
	"""
    Saves a trajectory plot to a specified directory.

    Parameters:
    traj (np.array): Array of trajectory points.
    dirc (str): Directory path where the plot will be saved.
    """
	fig, ax = plt.subplots()
	ax.plot(traj[:,0], traj[:,1])
	ax.plot(traj[:,2], traj[:,3])
	for i, x in enumerate(traj):
		if i%50 == 0:
			ax.plot([x[0], x[2]], [x[1], x[3]], 'b--')
	# ax.plot(circ[:,0], circ[:,1], '--')
	ax.grid()
	ax.axis('equal')
	plt.savefig(dirc)
	plt.close()

# this function read the data created by envelope_barrier(..)
def read_dwin_data():
	"""
    Reads defender winning data from a CSV file and returns arrays of states, positions, phi angles, and ratios.
    """
	with open('res/r1_6.100-r2_6.600/data.csv') as f:
		# print('reading')
		reader = csv.reader(f, delimiter=',')
		ss, xs, phis, ratios = [], [], [], []
		for row in reader:
			# print(row)
			s = list(map(float, row))
			ss.append(s[:4])
			phis.append(s[-1])
			xd = s[0]*cos(s[1])
			yd = s[0]*sin(s[1])
			xi = s[2]*cos(s[3])
			yi = s[2]*sin(s[3])
			x = [xd, yd, xi, yi]
			xs.append(x)
			ratios.append(s[2]/s[0])
				# print(len(S))
	return np.asarray(ss), xs, phis, ratios

def read_barrier_data():
	"""
    Reads barrier data from a CSV file and returns arrays of states, positions, phi angles, and ratios.
    """
	with open('res/r1_6.500-r2_6.540/data.csv') as f:
		# print('reading')
		reader = csv.reader(f, delimiter=',')
		ss, xs, phis, ratios = [], [], [], []
		for row in reader:
			# print(row)
			s = list(map(float, row))
			ss.append(s[:4])
			phis.append(s[-1])
			xd = s[0]*cos(s[1])
			yd = s[0]*sin(s[1])
			xi = s[2]*cos(s[3])
			yi = s[2]*sin(s[3])
			x = [xd, yd, xi, yi]
			xs.append(x)
			ratios.append(s[2]/s[0])
				# print(len(S))
	return np.asarray(ss), xs, phis, ratios

# this function read all the data saved by envelope_barrier(), so as to  
# plot the cyan trajectories in Figure 16
def read_data():
	"""
    Reads all data saved by envelope_barrier() to plot trajectories in Figure 16.
    """
	S, X, PHI, R = [], [], [], []
	for root, dirs, files in os.walk('res'):
		for dname in dirs:
			# print(dname)
			if os.path.exists('res/'+dname+'/data.csv'):
				# print('exists')
				with open('res/'+dname+'/data.csv') as f:
					# print('reading')
					reader = csv.reader(f, delimiter=',')
					ss, xs, phis, ratios = [], [], [], []
					for row in reader:
						# print(row)
						s = list(map(float, row))
						ss.append(s[:4])
						phis.append(s[-1])
						xd = s[0]*cos(s[1])
						yd = s[0]*sin(s[1])
						xi = s[2]*cos(s[3])
						yi = s[2]*sin(s[3])
						x = [xd, yd, xi, yi]
						xs.append(x)
						ratios.append(s[2]/s[0])
				save_traj_plot(np.asarray(xs), 'res/'+dname+'/traj.png')
				S.append(np.asarray(ss))
				X.append(np.asarray(xs))
				PHI.append(np.asarray(phis))
				R.append(np.asarray(ratios))
				# print(len(S))
	return S, X, PHI, R

# the three functions below are the Phase II constraints
# they will be put as the second argument of plot_bds
def triag_cnstr_1(r1):
	return r1 - r	

def triag_cnstr_2(r1):
	return r1 + r	

def triag_cnstr_3(r1):
	return r - r1

# draw the Phase II constraint, which are the dashed black lines in Figure 16
def plot_bds(ax, func, n=5, label=None):
	"""
    Plots the Phase II constraint boundaries on the given axes.

    Parameters:
    ax (matplotlib.axes.Axes): The axes on which to plot the boundaries.
    func (callable): The constraint function to be plotted.
    n (int): Number of points to calculate for the boundary.
    label (str): Label for the boundary in the plot.
    """
	r1s = np.linspace(0, 10., n)
	r2s = np.zeros(n)
	for i, r1 in enumerate(r1s):
		r2s[i] = (func(r1))
	ax.plot(r1s, r2s, 'k--', label=label)

# seems not used
def plot_orbit(ax):
	ax.plot([rDcap_min, rDcap_max], [rIcap_min, rIcap_max], 'k--')

# seems not used
def solve_phi0_states(r1):

	def get_phi(r2, r1=r1):
		return get_phi_max(r1, r2)[0]

# dashed blue lines in Figure 16
def read_switchline():
	"""
    Reads switch line data from a CSV file.
    """
	with open('switch.csv', 'r') as f:
		reader = csv.reader(f, delimiter=',')
		r1, r2 = [], []
		for row in reader:
			s = list(map(float, row))
			r1.append(s[0])
			r2.append(s[1])
	return r1, r2

# dashed blue lines in Figure 16
def get_switchline():
	"""
    Computes the switch line based on the Phase II constraints and saves it to a CSV file.
    """
	r1s, r2s, phis = [], [], []
	r0s = np.linspace(0.2*r, 8*r, 66)
	for r0 in r0s:
		r1l, r1u = (r0 - r)/2, (r0 + r)/2
		for r1 in np.linspace(r1l+0.06, r1u-0.06, 66):
			r2 = r0 - r1
			if abs((r1**2 + r2**2 - r**2)/(2*r1*r2))<1:
				r1s.append(r1)
				r2s.append(r2)
				phis.append(get_phi_max(r1, r2)[0])
    	
	r1s = np.asarray(r1s)
	r2s = np.asarray(r2s)
	phis = np.asarray(phis)

	xi, yi = np.linspace(1., 10., 50), np.linspace(1., 10., 50)
	triang = tri.Triangulation(r1s, r2s)
	interpolator = tri.LinearTriInterpolator(triang, phis)
	Xi, Yi = np.meshgrid(xi, yi)
	zi = interpolator(Xi, Yi)

	fig, ax = plt.subplots()
	cs = ax.contour(xi, yi, zi, levels=14, linewidths=2, colors='r')

	line = []
	for p in cs.collections[1].get_paths()[0].vertices:
		if p[0] > r1_min and p[1] > r2_min:
			line.append(p)
			with open('switch.csv', 'a') as f:
				f.write(','.join(list(map(str, p)))+'\n')
	plt.close()

	return np.asarray(line)

if __name__ == '__main__':
    # This block includes reading data, plotting phase II constraints, plotting trajectories on boundaries,
    # plotting switch lines, and setting up the overall plot with legends and labels.

	r1, r2 = read_switchline()

	line2x = [2.36, 2.5, 2.71, 2.85, 3.196, 4.605, 5.952, 7.518]
	line2y = [0.47, 0.64, 0.88, 1.04, 1.42, 2.93, 4.317, 5.9015]

	fig, ax = plt.subplots()
	ax.plot(r1, r2, 'b--', alpha=0.6, label='switch line', zorder=1000, linewidth=2.)
	ax.plot(line2x, line2y, 'b--', alpha=0.6, zorder=1000, linewidth=2.)

	# print('reading trajectory')
	ss, xs, phis, rs = read_data()
	ssd, _, _, _ = read_dwin_data()
	ssb, _, _, _ = read_barrier_data()

	plot_bds(ax, triag_cnstr_3)
	plot_bds(ax, triag_cnstr_2)
	plot_bds(ax, triag_cnstr_1, label=r'Phase II constraint')
	# plot_orbit(ax)
	# cntr = ax.contour(xi, yi, zi, [0])

	# # fig.colorbar(cntr, ax=ax)

	for i, s in enumerate(ss):
		if i%2 == 0:
			# ax.plot(s[:,0], s[:,2], 'bo-')
			# ax.plot(s[:,0], s[:,2], 'bo-', ms=3, markevery=10)
			ax.plot(s[:,0], s[:,2], 'c-', label=None, alpha=0.6)

	ax.plot(ssd[:,0], ssd[:,2], 'm-o', ms=3, markevery=10, zorder=1001, label=r'$(\rho_D, \rho_I)=(6.1, 6.6)$')
	ax.plot(ssb[:,0], ssb[:,2], 'b', zorder=1001, label='barrier')
	ax.plot(r1_min, r2_min, 'ro', label='attractor', zorder=1002)

	ax.grid()
	ax.axis('equal')
	ax.set_xlim([0, 10])
	ax.set_ylim([0, 10])
	plt.xlabel(r'$\dot{\rho_D}$', fontsize=14)
	plt.ylabel(r'$\dot{\rho_I}$', fontsize=14)
	ax.legend(fontsize=12)
	plt.show()
