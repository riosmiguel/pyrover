
for e_phi in range(-130, 130, 10):
    d_pwm = e_phi * (abs(e_phi) < 50) + 50*(e_phi > 50) - 50*(e_phi < -50)
    print(e_phi,"\t",d_pwm)
