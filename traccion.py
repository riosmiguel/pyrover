import log


#---------------------------------------- Traccion ----------------------------------

def inicializar():
	global motor_izq, motor_der
	motor_izq = Motor(12, 13)
	motor_der = Motor(18, 19)


def set_pwm_and_ratio(pwm, ratio):
	global motor_izq, motor_der

	if ratio > 1: ratio = 1
	if ratio < -1: ratio = -1

	diff = pwm * ratio

	motor_izq.set_pwm(pwm - diff)
	motor_der.set_pwm(pwm + diff)

#def set_pwm_suma_y_diff(suma, diff):
#	global motor_izq, motor_der

#	diff = diff / 2

#	if(suma + abs(diff) > 100) : suma = suma - abs(diff)
#	if(suma - abs(diff) < 100) : suma = suma + abs(diff)

#	motor_izq.set_pwm((suma - diff))
#	motor_der.set_pwm((suma + diff))


#---------------------------------------- Motores ----------------------------------

import gpiozero

class Motor:
	def __init__(self, pin_fw, pin_bw):
		self.gpio_fw = gpiozero.PWMOutputDevice(pin_fw)
		self.gpio_bw = gpiozero.PWMOutputDevice(pin_bw)
		self.stopped = False

	def stop(self):
		self.stopped = True
		self.set_pwm(0)

	def set_pwm(self, pwm):
		if(self.stopped):
			self.gpio_fw.value = 0
			self.gpio_bw.value = 0
		else:
			if(pwm>0):
				if(pwm>100) : pwm = 100
				self.gpio_bw.value = 0
				self.gpio_fw.value = pwm/100.0
				self.gpio_fw.frequency = 200+pwm * 10
			else:
				if(pwm<-100) : pwm = -100
				self.gpio_fw.value = 0
				self.gpio_bw.value = -pwm/100.0
				self.gpio_bw.frequency = 200-pwm * 10

	def getValue(self):
		if (self.gpio_fw.value > 0):
			return self.gpio_fw.value * 100.0
		else:
			return -self.gpio_bw.value * 100.0