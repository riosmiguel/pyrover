testing = False

if testing:
    import traccion_test as traccion
    #import rpm_test as rpm
else:    
    import traccion
    #import rpm
    
import en_campo
import log
import time
traccion.inicializar()

#print("prueba motores...")
#traccion.set_pwm_suma_y_diff(50, 0) 
#time.sleep(2)
traccion.set_pwm_suma_y_diff(0, 0) 
print("parado..")
time.sleep(3)

#exit(0)

log.inicializar()
#rpm.inicializar()
en_campo.inicializar()

start_time = 0


traccion.set_pwm_suma_y_diff(0, 0) 
print("parado..")
#time.sleep(2)

def tick():
    global start_time
    d_phi = 0
    elapsed_secs = 0
    d_pwm = 0

    gps = en_campo.gps
    if start_time != 0:
        elapsed_secs = time.time() - start_time
    
    if gps.fix < 3: # espera
        traccion.set_pwm_suma_y_diff(0, 0)

    else:
        if start_time == 0: start_time = time.time()

        if(elapsed_secs < 15): # empieza moviendo en recta 3s
            traccion.set_pwm_suma_y_diff(20, 0)
            #traccion.set_pwm_suma_y_diff(-15*elapsed_secs, 0)
            print ("f",gps.fix,"  e", "^", "  gps phi", round(gps.phi),"  d_pwm ","","  x=",round(en_campo.xx),"  y=",round(en_campo.yy))
            #print ("f",gps.fix,"  x=",round(en_campo.xx),"  y=",round(en_campo.yy))

        elif(en_campo.parar == 1): # terminar cuando termina el trabajo
            traccion.set_pwm_suma_y_diff(0,0)
            print("parar")

        else: # trabaja
            #calcular PWM usando phi (dirección real del rover) y target_phi (dirección ideal)
            d_phi = gps.phi - en_campo.target_phi

            if (abs(d_phi) > 180):
                if(d_phi>0):
                    d_phi = abs(d_phi) - 360
                else:
                    d_phi = 360 - abs(d_phi)
            
            d_pwm = d_phi *(abs(d_phi) < 50) + 50*(d_phi > 50) - 50*(d_phi < -50)
            #traccion.set_pwm_suma_y_diff(25, d_pwm)
            traccion.set_pwm_suma_y_diff(0,0)

            print ("f",gps.fix,"  e",en_campo.etapa,"  d_phi", round(d_phi),"  d_pwm=",round(d_pwm),"  x=",round(en_campo.xx),"  y=",round(en_campo.yy))
            exit(0)
    
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
