from machine import Pin, Timer, RTC, TouchPad, deepsleep
from neopixel import NeoPixel
import machine
import network
import ntptime
from time import sleep
import utime

ssid = 'Rk Iphone'
password = 'Rk123456789'


wlan = network.WLAN(network.STA_IF)  
wlan.active(True) 
wlan.connect(ssid, password)  

while not wlan.isconnected():
    pass

print("Connected to WiFi network:", ssid)
print("IP address:", wlan.ifconfig()[0])