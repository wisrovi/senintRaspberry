import RPi.GPIO as GPIO
import dht11
import time
import datetime

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 14
instance = dht11.DHT11(pin=14)


def instanciarSensor():
    return instance.read()

def leerTemperatura(result):
    return result.temperature

def leerHumedad(result):
    return result.humidity

def fechaHoraActual():
    return str(datetime.datetime.now())