
testing = True

import log
import time

if testing:
    import gps_test_2 as gps
    import traccion_test as traccion
else:    
    import gps
    import traccion

log.inicializar()
gps.inicializar()
traccion.inicializar()

def tick():
    start_time = 0
    elapsed_secs = 0
    d_pwm = 0

    if start_time != 0:
        elapsed_secs = time.time() - start_time

    log.print("secs", elapsed_secs)

    if not gps.lecturaValida():
        log.print("estado","espera") 
        traccion.set_pwm_suma_y_diff(0, 0)

    else:
        if start_time == 0: start_time = time.time()

        if(elapsed_secs < 1):
            log.print("estado","empezando") 
            traccion.set_pwm_suma_y_diff(50, 0)

        elif(elapsed_secs > 40):
            log.print("estado","fin") 
            traccion.set_pwm_suma_y_diff(0,0)

        else:
            log.print("estado","trabajando") 
            #calcular target_phi
            if(elapsed_secs < 15): target_phi = 40
            elif(elapsed_secs < 20): target_phi = 220 
            elif(elapsed_secs < 35): target_phi = 310 
            elif(elapsed_secs < 40): target_phi = 40

            #calcular PWM basado en phi y target_phi
            d_phi = gps.phi - target_phi
            if (abs(d_phi) > 180):
                if(d_phi>0):
                    d_phi = abs(d_phi) - 360
                else:
                    d_phi = 360 - abs(d_phi)

            d_pwm = d_phi / 1 # factor de conversion de grados a PWM (para correccion de la direccion)
            traccion.set_pwm_suma_y_diff(50, d_pwm)

    log.print("d_pwm",d_pwm)
    log.print("fix",gps.fix)
    log.print("x",gps.x, 3)
    log.print("y",gps.y, 3)
    log.print("phi",gps.phi)
    log.print("vel",gps.vel)

import threading, traceback

while True:
    interval = 0.1
    tick_start_time = time.time()
    try:
        tick()
    except Exception:
        log.print_msg(traceback.format_exc(-1))

    duration = time.time() - tick_start_time
    log.print("cpu %", duration * 100 / interval, 0)
    if(duration > interval):
        log.print_msg("Tick no pudo mantener intervalo")
    else:
        time.sleep(interval - time.time() % interval)