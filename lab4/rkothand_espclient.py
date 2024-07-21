from machine import Pin, Timer, RTC, TouchPad, deepsleep
from neopixel import NeoPixel
import machine
import network
import ntptime
from time import sleep
import utime
import socket
import esp32
import urequests

#2.2 CONNECT TO WIFI
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

def thingSpeak(temperature, hall):
    url = writeAPIKey + "&field1=" + str(temperature) + "&field2=" + str(hall) + "\r\n\r\n"
    response = urequests.get(url)
    print("Data successfully sent to ThingSpeak.")
    response.close()

def timer_callback(timer):
    temperature = measureTemp()
    hall = measureHall()
    print("Temperature:", temperature, "Hall Sensor Data:", hall)
    thingSpeak(temperature, hall)

timer = machine.Timer(0)
timer.init(period=300, mode=machine.Timer.PERIODIC, callback=timer_callback)

def timer_deinit(interrupt_timer):
    timer.deinit()
    interrupt_timer.deinit()
    
interrupt_timer = machine.Timer(1)
interrupt_timer.init(period=300000, mode=machine.Timer.ONE_SHOT, callback=timer_deinit)


