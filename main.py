    
import piloto
import log
import time

log.inicializar()
piloto.inicializar()

def t(s):
    # agrega tabs para imprimir
    return "\t"+s+"="

start_time = 0

def tick():
    global start_time
    e_phi = 0

    if start_time == 0:
            start_time = time.time()
        
    elapsed_secs = time.time() - start_time

    if(elapsed_secs < 1): # empieza moviendo en recta 1s
        time.sleep(0.1)
            
    if(piloto.parar == 1): # terminar cuando termina el trabajo
            print("parar")

    else: # trabaja        
            e_phi = piloto.e_phi

            if (abs(e_phi) > 180):
                if(e_phi>0):
                    e_phi = abs(e_phi) - 360
                else:
                    e_phi = 360 - abs(e_phi)

    print (
        t("e"),piloto.etapa, \
        t("x"),round(piloto.xx), \
        t("y"),round(piloto.yy), \
        t("phi"),round(piloto.phi), \
        t("dist rp"),round(piloto.dist_rp), \
        t("target"),round(piloto.target_phi), \
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

