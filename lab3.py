from machine import Pin, Timer, RTC, TouchPad, deepsleep
from neopixel import NeoPixel
import machine
import network
import ntptime
from time import sleep
import utime


#2.1
ssid = 'Rk Iphone'
password = 'Rk123456789'


wlan = network.WLAN(network.STA_IF)  
wlan.active(True) 
wlan.connect(ssid, password)  

while not wlan.isconnected():
    pass

print("Connected to WiFi network:", ssid)
print("IP address:", wlan.ifconfig()[0])

#2.2
'''
ntptime.host = "pool.ntp.org"
ntptime.settime()

utc_offset = -5 * 3600  
utc_time = utime.mktime(utime.gmtime()) + utc_offset
machine.RTC().datetime(utime.localtime(utc_time))

def display_time(timer):
    rtc_time = machine.RTC().datetime()
    formatted_time = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(rtc_time[0], rtc_time[1], rtc_time[2], rtc_time[3], rtc_time[4], rtc_time[5])
    print(formatted_time)

timer = Timer(0)
timer.init(period=150, mode=Timer.PERIODIC, callback=display_time)
'''

#2.3
touch = TouchPad(Pin(14))
def neopixel_control():
    if touch.read() < 500:
        n_pixel[0] = (0, 200, 0)
        n_pixel.write()
    else:
        n_pixel[0] = (0, 0, 0)
        n_pixel.write()
timer = Timer(0)
timer.init(period=150, mode=Timer.PERIODIC, callback=neopixel_control)





