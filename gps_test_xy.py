
test_list = [
    [-82, -266], \
    [-81, -266], \
    [-78, -266], \
    [-73, -264], \
    [-68, -261], \
    [-62, -258], \
    [-55, -256], \
    [-46, -254], \
    [-37, -252], \
    [-28, -248], \
    [-16, -245], \
    [-4, -243], \
    [6, -232], \
    [13, -212], \
    [13, -187], \
    [13, -166], \
    [13, -147], \
    [15, -132], \
    [17, -119]
]

lecturas = 0	# contador
fix = 0			# fix quality del gps: 0 = Bad, 1 = GPS, 2 = DGPS, 4 = RTK Fixed, 5 = RTK Float
x = 0
y = 0
phi = 0
vel = 0
x_tras = -100 	# en test_xy se ignora
y_tras = -100	# en test_xy se ignora

def inicializar():
	import threading
	threading.Thread(target=go_gps_test, daemon=True).start()

def go_gps_test():
	global test_list, fix, x, y, phi, vel, lecturas

	import time
	import math
	import sys

	time.sleep(0.125)
	fix = 5
	while(lecturas<len(test_list)):
		valores = test_list[lecturas]
		x_viejo = x
		y_viejo = y
		x = valores[0]
		y = valores[1]
		dx = x - x_viejo
		dy = y - y_viejo
		if ((dx != 0 or dy != 0) and (lecturas > 0)):
			#phi = (90 - math.degrees(math.atan2(dx, dy)) + 360) % 360 # da la direccion en grados respecto al Norte
			phi = math.degrees(math.atan2(dx, dy))
		vel = math.sqrt(dx*dx + dy*dy) / 2 #cm/s
		lecturas = lecturas + 1
		time.sleep(0.125)
	
	sys.exit()
