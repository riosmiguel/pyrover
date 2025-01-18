import log

import sys, os, threading, time

pwm = 0
ratio = 0

def inicializar():
	threading.Thread(target=go_teclado, daemon=True).start()

def set_pwm_and_ratio(_pwm, _ratio):
	global pwm, ratio
	
	if _ratio > 1: _ratio = 1
	if _ratio < -1: _ratio = -1
	
	pwm = _pwm
	ratio = _ratio

def go_teclado():
	sys.stdin.read(1)
	time.sleep(0.1)
	os._exit(0) # para la ejecucion del programa