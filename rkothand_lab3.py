from machine import Pin, Timer, RTC, TouchPad, deepsleep
from neopixel import NeoPixel
import machine
import network
import ntptime
from time import sleep
import utime
import esp32

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
rtc = RTC()
rtc.init((2023, 10, 29, 0, 23, 48, 0, 0))


def setup_rtc():
    ntptime.settime()
    rtc = RTC()
    rtc.init((2023, 10, 29, 0, 23, 48, 0, 0)) 

def display_time(timerclock):
    year, month, day, x, hour, minute, second, milli,  = rtc.datetime()
    print("Date: {:02}/{:02}/{:04}".format(month, day, year))
    print("Time: {:02}:{:02}:{:02}".format(hour, minute, second))

timerclock = Timer(0)
timerclock.init(period=6000, mode=Timer.PERIODIC, callback=display_time)


#2.3
poweron = Pin(2,Pin.OUT)
poweron.value(1)
led = NeoPixel(Pin(0),1)
touch = TouchPad(Pin(14))
def neopixel_control(Neotimer):
    if touch.read() < 500:
        led[0] = (0, 255, 0)
        led.write()
    else:
        led[0] = (0, 0, 0)
        led.write()
Neotimer = Timer(1)
Neotimer.init(period=15, mode=Timer.PERIODIC, callback=neopixel_control)

#2.4
def WakeUp():
    reason = machine.wake_reason()
    if reason == machine.EXT0_WAKE:
        print("Woken up due to EXT0")
    else:
        print("Woken up due to timer")   

red_led = Pin(13,Pin.OUT)
red_led.off()

def sleep(Waketimer):
    print("I am going to sleep for 1 minute.")
    red_led.off()
    machine.deepsleep(60000)
    
Waketimer = Timer(2)  
Waketimer.init(period=30000, mode=machine.Timer.ONE_SHOT, callback=sleep)

ext0 = Pin(25, Pin.IN, Pin.PULL_UP)
esp32.wake_on_ext0(ext0, esp32.WAKEUP_ANY_HIGH)

while True:
    pass



