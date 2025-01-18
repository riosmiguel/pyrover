import math, random

random.seed(0)

for i in range(-360, 360, 45):
    #print (i,"\t", (i+180) % 360 - 180)
    print(random.gauss(0,0))

exit(0)

def phi(dx, dy):
    phi = (90 - math.degrees(math.atan2(dy, dx)) + 360) % 360
    phi2 = math.degrees(math.atan2(dx, dy)) % 360
    print(dx,dy,"\t", round(phi), "\t", round(phi2))


phi( 1, 10)
phi(10, -1)
phi(-1, -10)
phi(-10, 1)