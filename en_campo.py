
# Calcular target_phi para usar en main
# cuando va hacia un punto, target_phi = dirección hacia ese punto

testing = False

if testing:
    import gps_test_xy as gps
else:
    import gps

import math
import time
import en_casa

target_phi = 0 # output para main
dist_rp = 0 # distancia rover a paralela
# der = 0 # variable bool, 1 = dobla derecha, 0 = dobla izquierda

def inicializar():
    gps.inicializar()
    import threading
    threading.Thread(target=go_en_campo, daemon=True).start()

def go_en_campo():
    global target_phi, parar, etapa
    global xx, yy
    
    tg_p = en_casa.tg_p # cte, pendiente de paralelas
    ancho = en_casa.ancho
    num_par = en_casa.num_par
    x1 = en_casa.x1 # array de abscisas de cortes entre aristas y paralelas desde V1 en sentido creciente
    y1 = en_casa.y1
    x2 = en_casa.x2 # array de abscisas de cortes desde V0 en sentido decreciente
    y2 = en_casa.y2
    X = en_casa.X
    Y = en_casa.Y
    xx = 0
    yy = 0
    parar = 0
    etapa = 0
    phi_par = 0

    while(gps.fix < 4):
        #print( "\nfix =", gps.fix)
        time.sleep(0.1)

    # --- IR HACIA EL ORIGEN -----------------------
    # calcula target_phi = arco(yy/xx)
    
    dist_rO_sq = 2000 # cuadrado de distancia rover al origen en cm
    etapa = 1

    while dist_rO_sq > 1600:
        time.sleep(0.1) # sleep para que no quede usando 100% cpu
        xx = gps.x*100 - en_casa.xV_min 
        yy = gps.y*100 - en_casa.yV_min
        
        dist_rO_sq = xx**2 + yy**2 # cuadrado distancia al origen
        target_phi = (90 - math.degrees(math.atan2(yy, xx)) + 360) % 360 + 180 # sentido hacia el origen
        if target_phi > 360:
            target_phi = target_phi - 360
    
    print ("llegó al origen")

    phi_par = (90 - math.degrees(math.atan2(tg_p,1)) + 360) % 360 # direccion en grados de tg_p, entre 0 y 180
    aux = (tg_p**2 + 1)**0.5

    # --- DECIDIR PARA QUE LADO DOBLA Y DOBLAR POR 1S ----
    
    # der = (gps.phi - phi_par > 180) + (gps.phi - phi_par < 0) # der=1 derecha, der=0 izquierda
    # etapa = 2

    #for i in range (0,15): # doblar
        # target_phi = abs(gps.phi - phi_par)*((der == 0) - (der == 1))
        
        # xx = gps.x*100 - en_casa.xV_min # para print del main, ver la trayectoria 
        # yy = gps.y*100 - en_casa.yV_min

        # time.sleep(0.1)

    # --- RECORRER SEGMENTOS DE PARALELAS  -------------------------
    
    for i in range (0, num_par, 2): # loop para 2 paralelas i, i+1
        
        Y0_p = ancho * aux * i # corte con eje Oy de cada paralela

        # ---- SEGUIR PARALELA DESDE (x2(i),y2(i)) A (x1(i),y1(i) OESTE A ESTE ----

        while  (xx - x1[i])**2 + (yy - y1[i])**2 > 1600: # cuadrado de distancia en cm de r al corte (x1(i, y1(i))
            time.sleep(0.1) # calculo de target_phi cada 0.1s para que no use mucha cpu
            etapa = 2
           
            xx = gps.x*100 - en_casa.xV_min 
            yy = gps.y*100 - en_casa.yV_min

            dist_rp = (yy - xx*tg_p - Y0_p)/aux # distancia rover a paralela i
            target_phi = phi_par + dist_rp * 0.5 # 0.5= factor de corrección cm a grados
            #print ("phi_par=",round(phi_par)," dist_rp=",round(dist_rp)," target_phi=",round(target_phi)," gps.phi=",round(gps.phi))
        
        if i+1 >= num_par : # terminó el trabajo por el lado 1
                parar = 1
    
        # ------------- DOBLAR 90 + 90 GRADOS A LA IZQUIERDA ------------------------
        #etapa = 3
        #target_phi = phi_par - 90
        #target_phi = target_phi + 360 * (target_phi < 0)
        
        #for j in range (0,6): # dividir sleep para leer coordenadas
            #xx = gps.x*100 - en_casa.xV_min 
            #yy = gps.y*100 - en_casa.yV_min   
            #time.sleep(0.1)
        
        #target_phi = phi_par - 180
        #target_phi = target_phi + 360 * (target_phi < 0)
        
        #for j in range (0,6):
            #xx = gps.x*100 - en_casa.xV_min 
            #yy = gps.y*100 - en_casa.yV_min   
            #time.sleep(0.1)

        # -------------SEGUIR PARALELA DESDE (x1(i+1),y1(i+1)) A (x2(i+1),y2(i+1) ESTE A OESTE-----------------
        etapa = 4
        Y0_p = ancho * aux * (i+1)
        
        phi_par = phi_par - 180 # la paralela tiene dirección contraria
        if phi_par < 0:
            phi_par = phi_par + 360

        while  (xx - x2[i+1])**2 + (yy - y2[i+1])**2 > 1600: # cuadrado distancia de r al corte
            time.sleep(0.1) # para que no quede usando 100% cpu
            
            xx = gps.x*100 - en_casa.xV_min 
            yy = gps.y*100 - en_casa.yV_min

            dist_rp = (yy - xx*tg_p - Y0_p)/aux # distancia rover a paralela i+1
            target_phi = phi_par - dist_rp * 0.5
            # print ("phi_par=",round(phi_par)," dist_rp=",round(dist_rp)," target_phi=",round(target_phi)," gps.phi=",round(gps.phi))
        
        # ------------- DOBLAR 180 GRADOS A LA DERECHA ------------------------
        etapa = 5
        target_phi = phi_par + 180
        if target_phi > 360:
            target_phi = target_phi - 360
        time.sleep(4)

        if i+2 > num_par : # chequear indice de la siguiente paralela
            # print ("terminó el trabajo por el lado 2")
            parar = 1
            print("terminó el trabajo por el lado 2")
    print ("terminó")
    parar = 1