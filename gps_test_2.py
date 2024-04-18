
lecturas = 0	# contador usado para inicializacion
fix = 0			# fix quality del gps: 0 = Bad, 1 = GPS, 2 = DGPS, 4 = RTK Fixed, 5 = RTK Float
x = 0
y = 0
phi = 0
vel = 0

def inicializar():
	pass

test_dict = {
	0.0: [1.0, 1.0],
	5.0: [1.0, 0.0]
}

import navpy, math

test_vx = 0
test_vy = 0

def lecturaValida():
	global x, y, fix, test_vx, test_vy, test_dict
	global sm_dx, sm_dy		# delta x, delta y, suavizadas
	global phi	  			# direccion calculada luego de suavizar
	global lecturas			# contador usado para inicializacion

	x_viejo = x
	y_viejo = y

	secs = lecturas/10.0
	if secs in test_dict:
		test_vx = test_dict[secs][0]/10.0
		test_vy = test_dict[secs][1]/10.0

	x = x + test_vx
	y = y + test_vy

	lecturas = lecturas + 1

	if(lecturas == 1):	
		return False  # dx y dy no son validas todavia
	else: 
		fix = 4
	
	dx = x - x_viejo
	dy = y - y_viejo

	if(lecturas==2): # inicializar variables suavizadas
		sm_dx = dx
		sm_dy = dy

	alpha = 2 # cociente de suavizacion
	sm_dx = (sm_dx * alpha + dx) / (alpha + 1)
	sm_dy = (sm_dy * alpha + dy) / (alpha + 1)

	phi = (90 - math.degrees(math.atan2(sm_dy, sm_dx)) + 360) % 360 # da la direccion en grados respecto al Norte

	return True