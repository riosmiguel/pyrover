import log

import sys, os, threading, time

def inicializar():
	threading.Thread(target=go_teclado, daemon=True).start()

def set_pwm_and_ratio(pwm, ratio):
	pass


def go_teclado():
	sys.stdin.read(1)
	time.sleep(0.1)
	os._exit(0) # para la ejecucion del programa