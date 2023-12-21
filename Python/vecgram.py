'''
This script uses different notations from the paper, please see below (some of) the correspondance:

    script      |       paper   
----------------+-------------------  
    rIcap_min   |       rho_I^ast
    phi         |       phi_D
    psi         |       phi_I
    r1          |       rho_D
    r2          |       rho_I
    ...         |       ...
----------------+-------------------
'''

import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['text.usetex'] = True
import numpy as np
from math import pi, sqrt, acos, cos, sin, tan, atan2
from scipy.optimize import minimize, dual_annealing
from Config import Config

r = Config.CAP_RANGE # capture radius of the defender
R = Config.TAG_RANGE # radius of the target area
vd = Config.VD       # defender's velocity
vi = Config.VI       # invader's velocity
gmm = acos(vd / vi)  
 
'''
rho_D, rho_I are bounded in phase II:
rDcap_min <= rho_D <= rDcap_max
rIcap_min <= rho_I <= rIcap_max 

for more details, please refer to Equations (23) (24) (27)
'''
rIcap_min, rIcap_max = r / (sin(gmm)), r / (1 - cos(gmm))
rDcap_min, rDcap_max = rIcap_min * (vd / vi), rIcap_max * (vd / vi)


''' 
given:  rho_D, rho_I, phi_D, notations in the paper,
        r1,    r2,    phi  , notations of this script
return: phi_D^ast, notations in the paper
'''

# Calculates the velocities of the defender and intruder based on their positions and controls.
def velocity_vec(r1, r2, phi, backward=False):
    """
    Computes the velocity components for the defender and intruder based on their optimal control strategy.

    Parameters:
    r1 (float): Radial distance of the defender from the target center.
    r2 (float): Radial distance of the intruder from the target center.
    phi (float): The defender's control input angle.
    backward (bool): Flag to compute velocity in the backward direction (for reverse time simulation).

    Returns:
    tuple: Components of velocity (vr1, vr2, vtht1, vtht2) for the defender and intruder.
    """

    # given defender's control, solve the invader's control, see (22)
    # for more info, this is the ``best response'' in game theory
    psi = acos(vd / vi * cos(phi))
    psi = -abs(psi)

    # Eq (21)
    alpha = acos((r ** 2 + r1 ** 2 - r2 ** 2) / (2 * r1 * r))
    beta = pi - acos((r ** 2 + r2 ** 2 - r1 ** 2) / (2 * r2 * r))

    # as we apply the concept of dynamic programming, the game is solved backward in time,
    # which means the velocity solved is reversed by default
    # to obtain the velocity in the forward direction, specify backward=False explicitly
    if backward:
        vr1 = vd * cos(alpha + phi)
        vr2 = vi * cos(beta + psi)
        vtht1 = vd * sin(alpha + phi) / r1
        vtht2 = vi * sin(beta + psi) / r2
    else:
        vr1 = -vd * cos(alpha + phi)
        vr2 = -vi * cos(beta + psi)
        vtht1 = -vd * sin(alpha + phi) / r1
        vtht2 = -vi * sin(beta + psi) / r2

    return vr1, vr2, vtht1, vtht2

''' 
given:  rho_D, rho_I, notations in the paper,
        r1,    r2   , notations of this script
return: phi_D^ast, the defender's optimal control

See algorithm 3
'''

# Implements Algorithm 3 from the paper to determine the defender's optimal control 
# phi_D* by computing the slopes of the vectogram tangents and choosing the correct 
# tangent based on the algorithm's conditions.
def get_phi(r1, r2):
    """
    Determines the defender's optimal control angle phi_D* based on the current positions of the defender and intruder.

    Parameters:
    r1 (float): Radial distance of the defender from the target center.
    r2 (float): Radial distance of the intruder from the target center.

    Returns:
    float: The optimal control angle phi_D* for the defender.
    """

    # this looks like velocity_vec but only returns the first two outputs
    def get_v(phi, r1, r2):
        psi = acos(vd / vi * cos(phi))
        psi = -abs(psi)
        alpha = acos((r ** 2 + r1 ** 2 - r2 ** 2) / (2 * r1 * r))
        beta = pi - acos((r ** 2 + r2 ** 2 - r1 ** 2) / (2 * r2 * r))

        v1 = -vd * cos(alpha + phi)
        v2 = -vi * cos(beta + psi)

        return v1, v2

    # the slope of the two tangents (red line in Figure 12) of the vectogram.
    def slope_p(phi, r1=r1, r2=r2):
        v1, v2 = get_v(phi, r1, r2)
        return atan2(v2, v1)

    def slope_n(phi, r1=r1, r2=r2):
        v1, v2 = get_v(phi, r1, r2)
        return -atan2(v2, v1)

    # below is the implementation of algorithm 3
    phi_max_slope = minimize(slope_n, 0).x
    phi_min_slope = minimize(slope_p, -.0001).x
    ang_p = slope_p(phi_max_slope)
    ang_n = slope_p(phi_min_slope)
    if ang_p - ang_n > pi:
        # print(ang_p, ang_n)
        # print('set 0')
        return 0
    else:
        # if max(phi_max_slope, phi_min_slope) < 0:
        #     print('compute: both < 0')
        #     return max(phi_max_slope, phi_min_slope)
        # else:
        #     print('compute: one < 0, chose smaller')
        #     return min(phi_max_slope, phi_min_slope)
        if ang_p > 0:
            return phi_max_slope
        else:
            return phi_min_slope

    # feels like this line won't be executed. May be some remains of older versions
    return sol.x


# the maximum phi_D that could be returned by get_phi
def get_phi_max(r1, r2):
    """
    Finds the maximum value of the defender's control angle that leads to the minimum slope in the vectogram.

    Parameters:
    r1 (float): Radial distance of the defender from the target center.
    r2 (float): Radial distance of the intruder from the target center.

    Returns:
    float: The maximum control angle phi_D that minimizes the vectogram slope.
    """
    def get_v(phi, r1, r2):
        psi = acos(vd / vi * cos(phi))
        psi = -abs(psi)
        alpha = acos((r ** 2 + r1 ** 2 - r2 ** 2) / (2 * r1 * r))
        beta = pi - acos((r ** 2 + r2 ** 2 - r1 ** 2) / (2 * r2 * r))

        v1 = -vd * cos(alpha + phi)
        v2 = -vi * cos(beta + psi)

        return v1, v2

    def slope_p(phi, r1=r1, r2=r2):
        v1, v2 = get_v(phi, r1, r2)
        return atan2(v2, v1)

    def slope_n(phi, r1=r1, r2=r2):
        v1, v2 = get_v(phi, r1, r2)
        return -atan2(v2, v1)
    
    return minimize(slope_n, 0).x

# this function is called by one_plot.py to generate one subfigure of Figure 12, 18, 20
'''
input: rho_D,  rho_I, paper notations, or
          r1,     r2, notation used by this scripts
'''
def draw_vecgram(r1, r2, id, capid):
    """
    Generates and saves a vectogram plot based on the defender's and intruder's positions.

    Parameters:
    r1 (float): Radial distance of the defender from the target center.
    r2 (float): Radial distance of the intruder from the target center.
    id (int): Unique identifier for the generated plot file.
    capid (int): Identifier for the sub-caption of the plot.

    Returns:
    None: The plot is saved to a file and not returned.
    """
    capfig = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    v1s, v2s = [], []
    phis = np.concatenate([np.linspace(-pi, 0, 30),np.linspace(0.0, pi, 30), np.array([-pi])])
    for phi in phis:
        s = velocity_vec(r1, r2, phi, backward=False)
        v1s.append(s[0])
        v2s.append(s[1])
    vphi0 = velocity_vec(r1, r2, 0, backward=False)
    # print(r1, r2, vphi0[0], vphi0[1])

    phi_opt = get_phi(r1, r2)
    so = velocity_vec(r1, r2, phi_opt, backward=False)

    fig, ax = plt.subplots()
    # ax.clear()
    ax.plot(v1s[0:30], v2s[0:30], 'k-', label=r'$\phi\leq0$')
    ax.plot(v1s[30:-1], v2s[30:-1], 'k--', label=r'$\phi>0$')
    ax.plot(v1s[:1], v2s[:1], 'b.', label=r'$\phi = -\pi$')
    # ax.plot(v1s[29:30], v2s[29:30], 'y.')
    ax.plot(vphi0[0], vphi0[1], 'g.', label=r'$\phi = 0$')
    ax.plot([1.01 * so[0], 0], [1.01 * so[1], 0], 'r')
    ax.legend(fontsize=14)
    plt.xlabel(r'$\dot{\rho}_D$', fontsize=16)
    plt.ylabel(r'$\dot{\rho}_I$', fontsize=16)
    ax.grid()
    # plt.title(r'$\phi=%.3f$, $(\rho_D, \rho_I)=(%.3f, %.3f)$' % (phi_opt, r1, r2), fontsize=14)
    plt.title(r'('+capfig[capid]+')', fontsize=16)
    # fig.canvas.draw()
    # ax.grid()
    ax.axis('equal')
    # plt.show()
    plt.savefig('vecgram_'+str(id)+'.png')
    plt.close('all')

# this function is called by animator.py to generate each frame of the vectogram
def draw_vecgram_animation(ax, r1, r2):
    """
    Draws the vectogram for animation on the given axes based on the current state.

    Parameters:
    ax (matplotlib.axes.Axes): Axes object on which to draw.
    r1 (float): Radial distance of the defender from the target center.
    r2 (float): Radial distance of the intruder from the target center.

    Returns:
    None: Vectogram is drawn on the provided axes.
    """
    v1s, v2s = [], []
    phis = np.concatenate([np.linspace(-pi, 0, 30),np.linspace(0.0, pi, 30), np.array([-pi])])
    for phi in phis:
        s = velocity_vec(r1, r2, phi, backward=False)
        v1s.append(s[0])
        v2s.append(s[1])
    vphi0 = velocity_vec(r1, r2, 0, backward=False)

    phi_opt = get_phi(r1, r2)
    so = velocity_vec(r1, r2, phi_opt, backward=False)

    ax.plot(v1s[0:30], v2s[0:30], 'k-')
    ax.plot(v1s[30:-1], v2s[30:-1], 'k--')
    ax.plot(v1s[:1], v2s[:1], 'b.')
    # ax.plot(v1s[29:30], v2s[29:30], 'y.')
    ax.plot(vphi0[0], vphi0[1], 'g.')
    ax.plot([1.01 * so[0], 0], [1.01 * so[1], 0], 'r')
    
    ax.legend([r'$\phi\leq0$', r'$\phi>0$', r'$\phi = -\pi$', r'$\phi = 0$'], fontsize=11, loc="upper left")
    # ax.set_xlabel(r'$\dot{\rho}_D$', fontsize=16)
    # ax.set_ylabel(r'$\dot{\rho}_I$', fontsize=16)
    # ax.grid()
    # ax.axis('equal')

# compare this function to get_phi(..) to see the difference
# Calculates the semipermeable radius based on the slopes of 
# the vectogram, which is used to determine the boundary of the region that the defender can control.
def semipermeable_r(r1, r2):
    """
    Calculates the angle between the semipermeable directions in the vectogram.

    Parameters:
    r1 (float): Radial distance of the defender from the target center.
    r2 (float): Radial distance of the intruder from the target center.

    Returns:
    float: Angle between the semipermeable directions.
    """
    def get_v(phi, r1, r2):
            psi = acos(vd / vi * cos(phi))
            psi = -abs(psi)
            alpha = acos((r ** 2 + r1 ** 2 - r2 ** 2) / (2 * r1 * r))
            beta = pi - acos((r ** 2 + r2 ** 2 - r1 ** 2) / (2 * r2 * r))

            v1 = -vd * cos(alpha + phi)
            v2 = -vi * cos(beta + psi)

            return v1, v2
    
    def slope_p(phi, r1=r1, r2=r2):
        v1, v2 = get_v(phi, r1, r2)
        return atan2(v2, v1)

    def slope_n(phi, r1=r1, r2=r2):
        v1, v2 = get_v(phi, r1, r2)
        return -atan2(v2, v1)

    ang_p = slope_p(minimize(slope_n, 0).x)
    ang_n = slope_p(minimize(slope_p, 0).x)
    # print(ang_p)
    # print(ang_n)
    # print(ang_p - ang_n)

    return pi - (ang_p - ang_n)

