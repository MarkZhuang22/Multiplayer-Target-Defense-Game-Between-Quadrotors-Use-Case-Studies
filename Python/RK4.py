def rk4(f, x0, dt):
	# one-step rk4 integration 
	k1 = f(x0)
	k2 = f(x0 + 0.5*k1*dt)
	k3 = f(x0 + 0.5*k2*dt)
	k4 = f(x0 + 1.0*k3*dt)
	k = (k1 + k2 + k2 + k3 + k3 + k4)/6
	return x0 + k*dt

	