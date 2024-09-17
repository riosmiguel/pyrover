
import RPi.GPIO as GPIO
import time

activation_count = 0

def inicializar():
    import threading
    threading.Thread(target=go_rpm, daemon=True).start()

def sensor_callback(channel):# Callback para manejar cada interrupción del sensor
    global activation_count
    activation_count += 1

def go_rpm():
    SENSOR_PIN = 17  # BCM del pin del sensor (lugar 11)

    GPIO.setmode(GPIO.BCM)  # Usa la numeración BCM de los pines
    GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Configura el pin como entrada con resistencia pull-up

    GPIO.add_event_detect(SENSOR_PIN, GPIO.FALLING, callback=sensor_callback)
    
    global activation_count
    try:
        while True:
            activation_count = 0

            time.sleep(1)

            #print(f"Activaciones por segundo: {activation_count}")

    except KeyboardInterrupt:
        print("Programa terminado por el usuario")

    finally:
        # Limpia la configuración GPIO
        GPIO.cleanup()
