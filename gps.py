
lecturas = 0	# contador usado para inicializacion
fix = 0			# fix quality del gps: 0 = Bad, 1 = GPS, 2 = DGPS, 4 = RTK Fixed, 5 = RTK Float
x = 0
y = 0
phi = 0
vel = 0

def lecturaValida():
	global fix, lecturas
	if(fix >= 4 and lecturas > 2):
		return True
	else:
		return False
	
def go_gps():
	global lat, lon, alt, utc, vel, fix  # valores directos leidos del gps
	
	# abrir puerto serial hacia el RTK
	import serial
	puerto_com = serial.Serial('/dev/serial0', 115200, 8, "N", 1, timeout=1)

	while True:

		while(not puerto_com.is_open):
			fix = -1
			puerto_com.open()
	
		mensaje = puerto_com.readline().decode().split(',')
		del mensaje[-1] # Borrar ultimo item del mensaje array porque es un CRC
		#Si se quiere guardar todos los mensajes, usar este código:
		# for c in mensaje: file.write(str(c)), file.write("\t")

		if mensaje[0] == '$GNVTG':
			#dir = strToFloat(mensaje[1]) - no usamos dir del gps 
			vel = strToFloat(mensaje[7])

		if mensaje[0] == '$GNGGA':
			lat = dmmToFloat(mensaje[2],mensaje[3])
			lon = dmmToFloat(mensaje[4],mensaje[5])
			alt = strToFloat(mensaje[9])
			utc = strToFloat(mensaje[1])
			fix = strToInt(mensaje[6]) 	
			if(fix >= 4):
				procesar(lat, lon, alt)


def inicializar():
	import threading
	threading.Thread(target=go_gps, daemon=True).start()


def strToInt(s):
	try:
		return int(s)
	except:
		return -1


def strToFloat(s):
	try:
		return float(s) # s es variable str local
	except:
		return float('nan')


def dmmToFloat(s, hemisphere):
	try:
		v = float(s) / 100 # v es variable local, no condundir con v:float de setValue
		v = int(v) + (v-int(v))/0.6
		if hemisphere=='W' or hemisphere=='S': v = -v
		return v
	except:
		return float('nan')
	
# ---------------------------------------------- procesar ------------------

import navpy, math

def procesar(lat, lon, alt): # datos
	global x, y, z 			# coordenadas NED 
	global sm_dx, sm_dy		# delta x, delta y, suavizadas
	global phi	  			# direccion calculada luego de suavizar
	global lecturas			# contador usado para inicializacion


	x_viejo = x
	y_viejo = y

	ned = navpy.lla2ned(lat, lon, alt, -31.713,-55.987, 140)
	y = ned[0]
	x = ned[1]
	z = -ned[2]

	lecturas = lecturas + 1

	if(lecturas == 1):	return False # dx y dy no son validas todavia
	
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