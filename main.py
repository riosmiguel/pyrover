testing = False

if testing:
    import traccion_test as traccion
else:    
    import traccion
    
import en_campo
import log
import time

from gpiozero import Button
button = Button(4)

log.inicializar()

traccion.inicializar()
traccion.set_pwm_and_ratio(0, 0)
en_campo.inicializar()

def t(s):
    # agrega tabs para imprimir
    return "\t"+s+"="

start_time = 0
def tick():
    global start_time
    e_phi = 0
    d_pwm = 0

    gps = en_campo.gps
    
    if button.value == 1:
        traccion.set_pwm_and_ratio(0, 0)
        print("-", end="")

    elif 1==1:
        traccion.set_pwm_and_ratio(20, 0)

    elif gps.fix < 4 or button.value == 1:
        traccion.set_pwm_and_ratio(0, 0)

    else:
        if start_time == 0:
            start_time = time.time()
        
        elapsed_secs = time.time() - start_time

        if(elapsed_secs < 2): # empieza moviendo en recta 3s
            pwm = 10 * elapsed_secs + 10
            traccion.set_pwm_and_ratio(pwm, 0)

        elif(en_campo.parar == 1): # terminar cuando termina el trabajo
            traccion.set_pwm_and_ratio(0,0)
            print("parar")

        else: # trabaja
            #calcular PWM usando phi (dirección real del rover) y target_phi (dirección ideal)
            e_phi = en_campo.target_phi - gps.phi

            if abs(e_phi) > 180 :
                if (e_phi > 0):
                    e_phi = abs(e_phi) - 360
                else:
                    e_phi = 360 - abs(e_phi)
            
            d_pwm = e_phi / 90
            traccion.set_pwm_and_ratio(25, d_pwm)

    print (gps.fix, \
        t("x"),round(en_campo.xx), \
        t("y"),round(en_campo.yy), \
        t("g_phi"),round(gps.phi), \
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

