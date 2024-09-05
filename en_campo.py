# RECORRE RECTAS PARALELAS AL PRIMER LADO ENTRE PUNTOS DE CORTE DE 
# ESTAS PARALELAS CON LOS DEMÁS LADOS, HALLADOS EN en_casa.py


import math
import gps
import time

# ------------------ INPUTS = OUTPUTS DE EN_CASA ------------------------------------
import en_casa
tg_p = en_casa.tg_p # cte, pendiente de paralelas
ancho = en_casa.ancho
num_par = en_casa.num_par
target_phi = 0 # se usa en main en mov real y en este módulo en simulación
x1 = en_casa.x1 # array de abscisas de cortes entre aristas y paralelas desde V1 en sentido creciente
y1 = en_casa.y1
x2 = en_casa.x2 # array de abscisas de cortes desde V0 en sentido decreciente
y2 = en_casa.y2
X = en_casa.X
Y = en_casa.Y

x = 9 # punto arranque del rover en simulación
y = 5

# ---------------- IR HACIA EL ORIGEN -----------------------
print()
print("va al origen")
# x = gps.x
# y = gps.y  
dist_rO_sq = 100

while dist_rO_sq > 3:
    # x = gps.x
    # y = gps.y
    x = x + math.sin(target_phi * 3.141593 / 180) # simular mov del rover
    y = y + math.cos(target_phi * 3.141593 / 180)
    dist_rO_sq = x**2 + y**2 # cuadrado de distancia al origen
    target_phi = (90 - math.degrees(math.atan2(y, x)) + 360) % 360 + 180 # sentido hacia el origen
    # print("phi =", target_phi, "    x =", x, "    y =", y)

print ("     llegó al origen   x2(0) =", x2[0], "y2(0) =", y2[0])
print("empieza recorrido")
aux = (tg_p**2 + 1)**0.5

# ----------------- RECORRER 4 SEGMENTOS ---------------------------

for i in range (0, num_par, 2): # loop por cada 2 paralelas
    
    phi_par = (90 - math.degrees(math.atan2(tg_p, 1)) + 360) % 360 # direccion, entre 0=Norte y 180=Sur
    Y0_p = ancho * aux * i
    print ("paralelas", i,"+",i+1, "                       direccion=", round(phi_par))

    # ---- SEGUIR PARALELA DESDE (x2(i),y2(i)) A (x1(i),y1(i) ----

    while  (x - x1[i])**2 + (y - y1[i])**2 > 100: # cuadrado de distancia de r al vértice Vi+1
        
        #x = gps.x
        #y = gps.y

        x = x + 10*math.sin(target_phi * 3.141593 / 180) # simular mov del rover
        y = y + 10*math.cos(target_phi * 3.141593 / 180)
        dist_rp = (y - x*tg_p - Y0_p)/aux # distancia rover a paralela i
        target_phi = phi_par + dist_rp * 1 # 1 = factor de corrección de distancia (cm) a ángulo (grados)
    
    print("      llegó al corte x1(",i,")=",x1[i],"  y1(",i,")=",y1[i])
    if i+1 >= num_par :
            print ("terminó el trabajo por el lado 1")
            exit()
    
    # ------------- DOBLAR 90 GRADOS A LA IZQUIERDA ------------------------

    target_phi = phi_par - 90 + 360 *(phi_par < 90)

    # ------------------ IR HACIA CORTE P(x1(i+1),y1(i+1))-----------------------
    dist_rP_sq = 100

    while dist_rP_sq > 3:
        # x = gps.x # en movimiento real
        # y = gps.y
        x = x + math.sin(target_phi * 3.141593 / 180) # en simulacion
        y = y + math.cos(target_phi * 3.141593 / 180)
        dist_rP_sq = (x-x1[i+1])**2 + (y-y1[i+1])**2 
        target_phi = (90 - math.degrees(math.atan2(y-y1[i+1], x-x1[i+1])) + 360) % 360 + 180 
        # print("phi =", target_phi, "    x =", x, "    y =", y)

    print ("      llegó al corte x1(",i+1,")=",x1[i+1],"  y1(",i+1,")=", y1[i+1])

    # ------------------------ DOBLAR 90 GRADOS A LA IZQUIERDA ------------

    # target_phi = phi_par - 180 + 360 *(phi_par < 180) # en movimiento real

    # -------------SEGUIR PARALELA DESDE (x1(i+1),y1(i+1)) A (x2(i+1),y2(i+1) -----------------
    Y0_p = ancho * aux * (i+1)
    phi_par = phi_par - 180 + 360 *(phi_par < 180)

    print("                                      direccion=", round(phi_par))

    while  (x - x2[i+1])**2 + (y - y2[i+1])**2 > 100: # cuadrado distancia de r al corte
        
        #x = gps.x
        #y = gps.y

        x = x + 10*math.sin(target_phi * 3.141593 / 180) 
        y = y + 10*math.cos(target_phi * 3.141593 / 180)

        dist_rp = (y - x*tg_p - Y0_p)/aux # distancia rover a paralela i+1

        target_phi = phi_par - dist_rp * 1 # 1 = factor de corrección de distancia (cm) a ángulo (grados)
    
    print("      llegó al corte x2(",i+1,")=",x2[i+1],"  y2(",i+1,")=",y2[i+1])
    
    # ------------- DOBLAR 90 GRADOS A LA DERECHA ------------------------

    target_phi = phi_par + 90 - 360 *(target_phi > 270) # doblar 90 gr a la izquierda

    # --------------- IR HACIA (x2(i+2),y2(i+2) -------------------------
    dist_rP_sq = 100

    while dist_rP_sq > 3:
        # x = gps.x # en movimiento real
        # y = gps.y
        x = x + math.sin(target_phi * 3.141593 / 180) # en simulacion
        y = y + math.cos(target_phi * 3.141593 / 180)
        if i+2 > num_par :
            print ("terminó el trabajo por el lado 2")
            exit()
        dist_rP_sq = (x-x2[i+2])**2 + (y-y2[i+2])**2 
        target_phi = (90 - math.degrees(math.atan2(y-y2[i+2], x-x2[i+2])) + 360) % 360 + 180 

    print ("      llegó al corte x2(",i+2,")=",x2[i+2],"  y2(",i+2,")=",y2[i+2])
print("terminó el trabajo por el lado 2")
exit() 