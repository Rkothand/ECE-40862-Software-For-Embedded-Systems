from machine import Pin, Timer, RTC, TouchPad, deepsleep
from neopixel import NeoPixel
import machine
import network
import ntptime
from time import sleep
import utime


#2.2
def connectWifi():
    ssid = 'Rk Iphone'
    password = 'Rk123456789'


    wlan = network.WLAN(network.STA_IF)  
    wlan.active(True) 
    wlan.connect(ssid, password)  

    while not wlan.isconnected():
        pass

    print("Connected to WiFi network:", ssid)
    print("IP address:", wlan.ifconfig()[0])
#2.3.1
writeAPIKey = 'https://api.thingspeak.com/update?api_key=0578NQIP8MXGAZFV'

def measureTemp():
    return esp32.raw_temperature()

def measureHall():
    return esp32.hall_sensor()

def connection_to_thingspeak(temperature, hall):
    urltemp = writeAPIKey + '&field1' + str(temperature)
    urlhall = writeAPIKey + '&field2' + str(hall)
    responseTemp = urequests.get(urltemp)
    responsehall = urequests.get(urlhall)
    
    print("Temperature is " + responseTemp + "Hall sensor is" + responsehall)

timer1 = machine.Timer(0)
s = socket.socket()
address = None

def main()
    connectWifi()
    tempMeasurement = measureTemp()
    hallSensor = measureHall()
    connection_to_thingspeak(tempMeasurement, hallsensor)


