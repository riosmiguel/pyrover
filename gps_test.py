
test_list = [
	[-31.71300, -55.98700, 140],
	[-32.71300, -55.98700, 140],
	[-33.71300, -55.98700, 140],
	[-31.71300, -55.98700, 140],
	[-31.71299, -55.98699, 140], # 0.94 1.10 40
	[-31.71298, -55.98698, 140], # 1.89 2.21 40
	[-31.71297, -55.98697, 140], # 
	[-31.71296, -55.98696, 140],
	[-31.71295, -55.98695, 140], # 4.7 5.5
	[-31.7, -55.9, 140]
]

lecturas = 0	# contador usado para inicializacion
fix = 0			# fix quality del gps: 0 = Bad, 1 = GPS, 2 = DGPS, 4 = RTK Fixed, 5 = RTK Float
x = 0
y = 0
phi = 0
vel = 0
x_tras = -100
y_tras = -100


def inicializar():
	import threading
	threading.Thread(target=go_gps_test, daemon=True).start()

def go_gps_test():
	global lecturas, fix, test_list
	import time
	time.sleep(1)

	while(lecturas<len(test_list)):
		fix = 5
		valores = test_list[lecturas]
		procesar(valores[0], valores[1], valores[2])
		lecturas = lecturas + 1
		time.sleep(5)
	
	fix = 0


import navpy, math

def procesar(lat, lon, alt):
	global x, y, z 			# coordenadas NED
	global phi	  			# direccion calculada luego de suavizar
	global lecturas			# contador usado para inicializacion
	global x_tras, y_tras

	sm_dx = 0
	sm_dy = 0		# delta x, delta y, suavizadas

	lecturas = lecturas + 1

	if(lecturas > 1):	
		x_viejo = x
		y_viejo = y

	ned = navpy.lla2ned(lat, lon, alt, -31.8718,-55.33825, 130)
	y = ned[0] - y_tras
	x = ned[1] - x_tras
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