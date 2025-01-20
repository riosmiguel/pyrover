
import math
for xx in range (-10,10):
    for yy in range (-10,10):
        phi = (90 - math.degrees(math.atan2(yy, xx)) + 360) % 360 + 180
        phi = phi + 360 * ((phi<0) -(phi>360))
        print(xx, yy, round(phi))
        