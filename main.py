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
    
    if 1==10:
        traccion.set_pwm_and_ratio(0, 0)

    elif button.value == 1:
        traccion.set_pwm_and_ratio(0, 0)
        print("-", end="")

    elif gps.fix < 3 or button.value == 1:
        traccion.set_pwm_and_ratio(0, 0)

    else:
        if start_time == 0:
            start_time = time.time()
        
        elapsed_secs = time.time() - start_time

        if(elapsed_secs < 3): # empieza moviendo en recta 3s
            pwm = 3 * elapsed_secs + 10
            traccion.set_pwm_and_ratio(pwm, 0)

        elif(en_campo.parar == 1): # terminar cuando termina el trabajo
            traccion.set_pwm_and_ratio(0,0)
            print("parar")

        else: # trabaja
            #calcular PWM usando phi (dirección real del rover) y target_phi (dirección ideal)
            e_phi = en_campo.target_phi - gps.phi

            if (abs(e_phi) > 180):
                if(e_phi>0):
                    e_phi = abs(e_phi) - 360
                else:
                    e_phi = 360 - abs(e_phi)
            
            d_pwm = e_phi / 90
            traccion.set_pwm_and_ratio(25, d_pwm)


    print (gps.fix, \
        t("x"),round(en_campo.xx), \
        t("y"),round(en_campo.yy), \
        t("g_phi"),round(gps.phi), \
        t("e"),en_campo.etapa, \
        t("dist rp"),round(en_campo.dist_rp), \
        t("Y0_p"),round(en_campo.Y0_p), \
        t("t_phi"),round(en_campo.target_phi), \
        t("e_phi"),round(e_phi) \
    )

import threading, traceback

while True:
    interval = 0.2
    tick_start_time = time.time()
    try:
        tick()
    except Exception:        print(traceback.format_exc(-1))

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

