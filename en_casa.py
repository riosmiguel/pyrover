import en_campo

# --------- INPUT POLÍGONO y DIAMETRO DE HELICE ----------- 
# en Google Earth, abrir un proyecto, ponerle nombre, ir a medir, dibujar un polígono CONVEXO Y CERRADO
# en los 3 puntos a la izquierda, exportar como archivo kml a carpeta de descargas
# abrir el archivo con notepad, buscar el string de coordenadas, copiar y pegar en polig abajo

# proyecto: 12nov
polig = (-55.98544927592471,-31.71126685000008,0 -55.98539615969337,-31.71121325013141,0 -55.98536837583899,-31.71110100240874,0 -55.98541744985553,-31.71114776202526,0 -55.98544927592471,-31.71126685000008,0)
ancho = 90 # es el ancho entre paralelas = diámetro de la hélice en cm

# --------------------------------------------------------

# 1) GUARDAR polig EN ARRAYS LLA_LAT y LLA_LON, PASAR A COORDENADAS XY, REDONDEAR A CENTIMETROS
aux_lat = 0
aux_lon = 0

import array as LLA_LAT
import array as LLA_LON
LLA_LAT = LLA_LAT.array ('f',[])
LLA_LON = LLA_LON.array ('f',[])

for i in range (0, len(polig)-2, 2): # incluye las dos últimas coordenadas distintas de 0 de polig. Las cifras se copian bien hasta el decimal 6 

    LLA_LON.append (polig[i])
    LLA_LAT.append (polig[i+1])
    
# print (LLA_LAT)
# print (LLA_LON)

cV = len (LLA_LAT) 
print ("cantidad de vertices ", cV-1) # el último punto repite al primero porque el poligono es cerrado 

import navpy, math

import array as X_aux
X_aux = X_aux.array ('f',[])
import array as Y_aux
Y_aux = Y_aux.array ('f',[])
alt = 130

for i in range (0, cV):
    
    ned = navpy.lla2ned (LLA_LAT [i], LLA_LON [i], alt, -31.711,-55.985, 0)

    Y_aux.append (round (ned[0]*100))
    X_aux.append (round (ned[1]*100))

# print("coordenadas XY sin ordenar")
# print (X_aux)
# print (Y_aux)

# 2) TOMAR EL VERTICE MÁS AL OESTE COMO PRIMER DATO Y HACER QUE SEA ORIGEN

xV_min = min (X_aux)
i_xV_min = X_aux.index(xV_min)
yV_min = Y_aux [i_xV_min]
# print ("punto mas al oeste =",i_xV_min, "   ", xV_min, yV_min,)

#en_campo.gps.x_tras = xV_min
#en_campo.gps.y_tras = yV_min

import array as X
X = X.array ('f',[])
import array as Y 
Y = Y.array ('f',[])

for i in range (i_xV_min, cV-1): # Pasar i_xV_min al lugar 0. Ignorar el elemento que cierra
    X.append (X_aux[i] - xV_min)
    Y.append (Y_aux[i] - yV_min)

for i in range (0, i_xV_min):
     X.append (X_aux[i] -xV_min)
     Y.append (Y_aux[i] -yV_min)

X.append (0) # cerrar el polígono repitiendo (0,0)
Y.append (0)

print ("coordenadas XY con (0,0) al Oeste ")
print("X= ", X)
print("Y= ", Y)

# 3) DETERMINAR LAS RECTAS PARALELAS QUE CORTAN AL POLIGONO

tg_p = (Y[1]/X[1]) # la primer paralela es la primer arista   p1: y = tg(Y(1)/X(1))
# print ("tg_P =", tg_p)

aux =(tg_p**2 +1)**0.5 # variable auxiliar en cálculo de distancias

# hallar distancias entre paralelas por vértices y origen para saber qué aristas corta cada paralela
import array as D 
D = D.array('f', []) 
D.append (0) # los 2 primeros vértices están a distancia 0
D.append (0)

for i in range(2, len(X)-1): # ignorar vértices 0, 1 y len(X), todos a distancia 0
    D.append (abs (round((tg_p * X[i]-Y[i]) / aux))) #  
# print("distancias    D =", D)

D_max = max (D) # distancia de la paralela por el vértice más alejado al origen
# print ("distancia máxima al origen =  ", D_max, "cm")

i_max = D.index (D_max)
# print ("indice del vértice más alejado i_max =", i_max)
num_par = math.trunc (D_max / ancho) 
print ("numero de paralelas =", num_par + 1) # incluye p0

# 4) HALLAR Y GUARDAR PARALELAS. HALLAR Y GUARDAR PUNTOS DE CORTE DE ARISTAS CON PARALELAS

import array as x1 # abscisas cortes aristas i <= i_max
x1 = x1.array ('f',[])
import array as y1
y1 = y1.array ('f',[])

x1.append (X[1]) # V1 comun a arista V0 V1 y paralela p0, es el elemento 0 del array de cortes
y1.append (Y[1])

i = 1 # índice arista arrancando por V1 V2
k = 1 # indice de las paralelas. Ignorar k = 0 

while (i < i_max): # hallar ecuaciones de aristas con vértices < i_max 

    tg_ai = (Y[i+1] -Y[i]) / (X[i+1] -X[i]) 
    Y0_ai = -tg_ai * X[i] + Y[i] # quedó definida ai: y = tg_ai*x + Y0_ai   Pasa por (0,Y0_ai)
    # print ("arista ", i,"a", i+1, "    y = ", tg_ai, " * x  +", Y0_ai)

    while (k * ancho < D[i+1]): # si se cumple esta condición, la paralela pk corta a la arista ai
    
        Y0_pk = aux * ancho * k # quedó definida la paralela pk: y = tg_p*x + Y0_pk
        
        # print("paralela ", k, "   y = ", tg_p, " * x + ", Y0_pk)

        # cortar ai con pk restando las ecuaciones de arriba. Guardar en arrays x1, y1
        coord_x = round (-(Y0_ai - Y0_pk) / (tg_ai - tg_p))  
        coord_y = round (tg_p * coord_x + Y0_pk)
        
        x1.append (coord_x)
        y1.append (coord_y)
    
        k = k + 1
    i = i + 1

i = cV-1 # arranca de nuevo por el origen contando aristas hacia atrás
k = 1 # arranca de nuevo por la primer paralela
import array as x2 # para aristas i >= i_max
x2 = x2.array ('f',[])
import array as y2
y2 = y2.array ('f',[])


x2.append (X[0]) # V0, vértice que cierra al polígono
y2.append (Y[0])

while (i > i_max): # hallar ecuaciones de aristas por vértices >= i_max
    
    # print("D(i-2) =", D[i-2])
    tg_ai = (Y[i-1] -Y[i]) / (X[i-1] -X[i]) 
    Y0_ai = -tg_ai * X[i] + Y[i] # quedó definida ai: y = tg_ai*x + Y0_ai   Pasa por (0,Y0_ai)
    # print("arista =", i,"a", i-1, "    y = ", tg_ai, " * x  +", Y0_ai)

    while (k * ancho < D[i-1]): # si se cumple esta condición, la paralela pk corta a la arista ai
    
        Y0_pk = aux * ancho * k # quedó definida la paralela pk: y = tg_p*x + aux*ancho*k
        # print("paralela ", k, "  y = ", tg_p, " * x * + ",Y0_pk)

        # cortar ai con pk restando ecuaciones  Guardar en arrays x, y
        coord_x = round (-(Y0_ai - Y0_pk) / (tg_ai - tg_p))
        coord_y = round (tg_p * coord_x + Y0_pk)

        x2.append (coord_x)
        y2.append (coord_y)

        k = k + 1
    i = i - 1



# ------------- OUTPUT: tg de las paralelas a arista V0 V1, coordenadas de cortes -------------
print ("tg_p= ", round(tg_p, 3))
print ("cortes del lado V1")
print ("x1=",x1)
print ("y1=",y1)
print ("cortes del lado V0")
print ("x2=",x2)
print ("y2=",y2)


#import pandas as pd  # Importar pandas para manejar el DataFrame

#mi_lista = list(x1) # Convertir el array a una lista para usarlo en un DataFrame de pandas

#df = pd.DataFrame({'Valores': mi_lista}) # Crear un DataFrame de pandas con la lista

#df.to_excel('data_py_rover.xlsx', index=True)  # Exporta el DataFrame a un archivo Excel

#print (mi_lista)