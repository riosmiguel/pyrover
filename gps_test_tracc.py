import traccion_test
import random

random.seed(0)

lecturas = 0
fix = 0
x = 100
y = -230
phi = 0
vel = 0

def inicializar():
	import threading
	threading.Thread(target=go_gps_test, daemon=True).start()

def go_gps_test():
	global  fix, x, y, phi, vel, lecturas
	import time, math, sys

	time.sleep(0.125 / 2)
	fix = 5
	while(True):
		lecturas = lecturas + 1
		vel = traccion_test.pwm / 2
		phi += traccion_test.ratio * 3 * vel
		#phi += random.gauss(0,lecturas/10)		

		x += vel * math.sin(math.radians(phi))
		y += vel * math.cos(math.radians(phi))
		
		time.sleep(0.125)
	
	sys.exit()
