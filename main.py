testing = False

if testing:
    import traccion_test as traccion
    import gps_test_tracc as gps
else:    
    import traccion
    import gps

if testing:
    from collections import namedtuple
    Button = namedtuple('Button', ['value'])
    button = Button(value = 0)
else:    
    from gpiozero import Button
    button = Button(4)

import puntos
pts = puntos.pts

import log, joystick

joystick.inicializar()
log.inicializar()
traccion.inicializar()
traccion.set_pwm_and_ratio(0, 0)
gps.inicializar()

def t(s):
    # agrega tabs para imprimir
    return "\t"+s+"="

import time, math, sys

start_time = 0
pt = pts.pop(0)
keyRatio = 0
keyPwm = 0

def tick():
    global start_time, pt
    global keyRatio
    e_phi = 0
    d_pwm = 0
    target_phi = 0

    if button.value == 1:
        traccion.set_pwm_and_ratio(0, 0)
        print("-", end="")

    elif 1==12:
        traccion.set_pwm_and_ratio(20, 0)

    elif joystick.key != "a":
        key = joystick.key.lower()
        if key == " ":
            keyRatio = 0
            keyPwm = 0
        if key == "i":
            keyRatio = 0
            keyPwm += 10
        if key == "k":
            keyRatio = 0
            keyPwm -= 10
        if key == "l":
            keyRatio += 0.1
        if key == "j":
            keyRatio -= 0.1
        if keyPwm > 100: keyPwm = 100
        if keyPwm < 0: keyPwm = 0
        if keyRatio > 1: keyRatio = 1
        if keyRatio < 0: keyRatio = 0
        traccion.set_pwm_and_ratio(keyPwm, keyRatio)
        print("+", end="")

    elif gps.fix < 4 or button.value == 1:
        traccion.set_pwm_and_ratio(0, 0)

    else:
        if start_time == 0:
            start_time = time.time()
        
        elapsed_secs = time.time() - start_time

        if (elapsed_secs < 2): # empieza moviendo en recta 3s
            pwm = 10 * elapsed_secs + 5
            traccion.set_pwm_and_ratio(pwm, 0)

        else:
            #calcular PWM usando phi (dirección real del rover) y target_phi (dirección ideal)
            dx = pt[0] - gps.x
            dy = pt[1] - gps.y
            while(dx*dx + dy*dy < 100 * 100):
                if(len(pts)==0):
                    traccion.set_pwm_and_ratio(0,0)
                    sys.exit()
                pt = pts.pop(0)
                dx = pt[0] - gps.x
                dy = pt[1] - gps.y

            target_phi = math.degrees(math.atan2(dx, dy)) # % 360

            e_phi = (target_phi - gps.phi + 180) % 360 - 180
            d_pwm = e_phi / 80

            if testing and round(elapsed_secs * 1.6 % 6)==5: d_pwm = 0.35
            
            traccion.set_pwm_and_ratio(20, d_pwm)

    print (gps.fix, \
        "\t",round(gps.x), \
        "\t",round(gps.y), \
        "\t",round(gps.phi), \
        "\t  |", \
        "\t",round(pt[0]), \
        "\t",round(pt[1]), \
        "\t",round(target_phi), \
        "\t  |", \
        "\t",round(gps.vel), \
        "\t",len(pts) \
    )
    

import threading, traceback

while True:
    interval = 0.125
    tick_start_time = time.time()
    try:
        tick()
    except Exception:
        print(traceback.format_exc(-1))

    try:
        duration = time.time() - tick_start_time
        #log.print("cpu %", duration * 100 / interval, 0)
        if(duration > interval):
            print ("Tick no pudo mantener intervalo")
            print ("duracion: ",duration,"    intervalo: ",interval)
        else:
            time.sleep(interval - time.time() % interval)
    except Exception:
        traccion.set_pwm_and_ratio(0,0)
        print("parando")

