
lecturas = 0	# contador usado para inicializacion
fix = 0			# fix quality del gps: 0 = Bad, 1 = GPS, 2 = DGPS, 4 = RTK Fixed, 5 = RTK Float
vel = 0

def inicializar():
    pass

def lecturaValida():
	
	if(lecturas == 0):   
		procesar(-31.7131, -55.9871, 140)
		procesar(-31.7132, -55.9872, 140)
	elif(lecturas == 2): procesar(-31.7133, -55.9873, 140)
	elif(lecturas == 3): procesar(-31.7134, -55.9874, 140)
	elif(lecturas == 4): procesar(-31.7135, -55.9875, 140)
	
	return True

import navpy, math

def procesar(lat, lon, alt):
	global x, y, z 			# coordenadas NED
	global sm_dx, sm_dy		# delta x, delta y, suavizadas
	global phi	  			# direccion calculada luego de suavizar
	global lecturas			# contador usado para inicializacion

	lecturas = lecturas + 1

	if(lecturas > 1):	
		x_viejo = x
		y_viejo = y

	ned = navpy.lla2ned(lat, lon, alt, -31.713,-55.987, 140)
	y = ned[0]
	x = ned[1]
	z = -ned[2]

	if(lecturas > 1): 
		dx = x - x_viejo
		dy = y - y_viejo
	else:
		return # dx y dy no son validas todavia

	if(lecturas==2): # inicializar variables suavizadas
		sm_dx = dx
		sm_dy = dy

	alpha = 2 # cociente de suavizacion
	sm_dx = (sm_dx * alpha + dx) / (alpha + 1)
	sm_dy = (sm_dy * alpha + dy) / (alpha + 1)

	phi = (90 - math.degrees(math.atan2(sm_dy, sm_dx)) + 360) % 360 # da la direccion en grados respecto al Norte