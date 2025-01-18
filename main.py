testing = True

if testing:
    import traccion_test as traccion
    import gps_test_xy as gps
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

import log
import time, math

log.inicializar()
traccion.inicializar()
traccion.set_pwm_and_ratio(0, 0)
gps.inicializar()

def t(s):
    # agrega tabs para imprimir
    return "\t"+s+"="

start_time = 0
pt = pts.pop(0)
def tick():
    global start_time, pt
    e_phi = 0
    d_pwm = 0
    target_phi = 0

    if button.value == 1:
        traccion.set_pwm_and_ratio(0, 0)
        print("-", end="")

    elif 1==12:
        traccion.set_pwm_and_ratio(20, 0)

    elif gps.fix < 4 or button.value == 1:
        traccion.set_pwm_and_ratio(0, 0)

    else:
        if start_time == 0:
            start_time = time.time()
        
        elapsed_secs = time.time() - start_time

        if (elapsed_secs < 2): # empieza moviendo en recta 3s
            pwm = 10 * elapsed_secs + 10
            traccion.set_pwm_and_ratio(pwm, 0)

        elif (len(pts) == 0): # terminar cuando termina el trabajo
            traccion.set_pwm_and_ratio(0,0)
            print("parar")

        else: 
            #calcular PWM usando phi (dirección real del rover) y target_phi (dirección ideal)
            pt = pts.pop(0)
            dx = pt[0] - gps.x
            dy = pt[1] - gps.y
        
            dist_sq = dx*dx + dy*dy
            target_phi = math.degrees(math.atan2(dx, dy)) # % 360

            e_phi = (target_phi - gps.phi) % 360 - 180
            d_pwm = e_phi / 90
            traccion.set_pwm_and_ratio(25, d_pwm)

    print (gps.fix, \
        t("gps_x"),round(gps.x), \
        t("gps_y"),round(gps.y), \
        t("gps_phi"),round(gps.phi), \
        
        t("pt_x"),round(pt[0]), \
        t("pt_y"),round(pt[1]), \
        t("pt_phi"),round(target_phi), \
        t("e_phi"),round(e_phi) \
    )
    

import threading, traceback

while True:
    interval = 0.2
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

