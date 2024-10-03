

testing = True

if testing:
    import traccion_test as traccion
    import rpm_test as rpm
else:    
    import traccion
    import rpm
    
import en_campo
import log
import time

log.inicializar()
traccion.inicializar()
rpm.inicializar()
en_campo.inicializar()

start_time = 0

def tick():
    global start_time
    elapsed_secs = 0
    d_pwm = 0

    gps = en_campo.gps
    if start_time != 0:
        elapsed_secs = time.time() - start_time

    #log.print("secs", elapsed_secs)

    if gps.fix <= 3:
        #log.print("estado","espera") 
        traccion.set_pwm_suma_y_diff(0, 0)

    else:
        if start_time == 0: start_time = time.time()

        if(elapsed_secs < 1): # empieza moviendo en recta
            #log.print("estado","empezando") 
            traccion.set_pwm_suma_y_diff(50, 0)

        elif(en_campo.parar == 1): # terminar cuando termina el trabajo
            #log.print("estado","fin") 
            traccion.set_pwm_suma_y_diff(0,0)

        else:
            #log.print("estado","trabaja")

            # cuando sigue una paralela p, target_phi es la pendiente de p corregida por distancia rover-p
            # cuando va hacia un punto, es la dirección hacia ese punto
            target_phi = en_campo.target_phi
             
            #if(elapsed_secs < 15): target_phi = 40
            #elif(elapsed_secs < 20): target_phi = 220 
            #elif(elapsed_secs < 35): target_phi = 310 
            #elif(elapsed_secs < 40): target_phi = 40

            #calcular PWM basado en phi (dirección real del rover) y target_phi (dirección ideal)
            d_phi = gps.phi - target_phi
            if (abs(d_phi) > 180):
                if(d_phi>0):
                    d_phi = abs(d_phi) - 360
                else:
                    d_phi = 360 - abs(d_phi)

            d_pwm = d_phi / 1 # factor de conversion de grados a PWM (para correccion de la direccion)
            traccion.set_pwm_suma_y_diff(50, d_pwm)

    #log.print("d_pwm",d_pwm)
    #log.print("fix",gps.fix)
    #log.print("x",gps.x, 3)
    #log.print("y",gps.y, 3)
    #og.print("phi",gps.phi)
    #log.print("vel",gps.vel)
    #log.print("rpm",rpm.activation_count)

import threading, traceback

while True:
    interval = 0.2
    tick_start_time = time.time()
    try:
        tick()
    except Exception:
        print(traceback.format_exc(-1))

    duration = time.time() - tick_start_time
    #log.print("cpu %", duration * 100 / interval, 0)
    if(duration > interval):
        print ("Tick no pudo mantener intervalo")
        print ("duracion: ",duration,"    intervalo: ",interval)
    else:
        time.sleep(interval - time.time() % interval)