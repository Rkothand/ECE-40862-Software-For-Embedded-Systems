from machine import SoftI2C, Pin
import mpu6050
from machine import Timer, RTC, TouchPad, deepsleep
from neopixel import NeoPixel
import machine
import network
import ntptime
from time import sleep
import utime
import socket
import esp32
import urequests


ssid = 'Rk Iphone'
password = 'Rk123456789'
wlan = network.WLAN(network.STA_IF)  
wlan.active(True) 
wlan.connect(ssid, password)  
while not wlan.isconnected():
    pass
print("Connected to WiFi network:", ssid)
print("IP address:", wlan.ifconfig()[0])



i2c = SoftI2C(scl=Pin(14), sda=Pin(22))
accelerometer = mpu6050.accel(i2c)

out = Pin(0, Pin.OUT)
np_power = Pin(2, Pin.OUT)
np = NeoPixel(out, 1)
out.value(1)
np_power.value(1)

# print(calibrationVal)

timer = machine.Timer(0)
timer2 = machine.Timer(1)

IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/notif_motion/with/key/koLbqdcOW9JDKc5_OA1kq3W68MiBkV8ZBs9aOW_NW-a'

def checkMotion():
    if((accelerometer.get_values()['AcX'] + accelerometer.get_values()['AcY'] + accelerometer.get_values()['AcZ'])>0.1):
        return 1
    else:
        return 0

#mpuAPIkey='koLbqdcOW9JDKc5_OA1kq3W68MiBkV8ZBs9aOW_NW-a'
def checkMPU(timer2):
    values = accelerometer.get_values()
    calibrated_values = accelerometer.calibrate()
    if checkMotion():
        print (calibrated_values)
        print("Motion detected!")
        np_power.value(1)
        np[0] = (255, 0, 0) 
        np.write()
        web_hook = urequests.get(IFTTT_WEBHOOKS_URL)
        web_hook.close()
        
        utime.sleep_ms(500)
        np[0] = (0, 255, 0)
        np.write()
        

        
        sensor_readings = {'value1': calibrated_values["AcX"], 'value2': calibrated_values["AcY"], 'value3': calibrated_values["AcZ"]}
        
        # Send sensor readings to IFTTT
        request_headers = {'Content-Type': 'application/json'}
        request_ifttt = urequests.post(IFTTT_WEBHOOKS_URL, json=sensor_readings)
        request_ifttt.close()

        
        


def thingspeak(channelNum, readAPIkey= 'https://api.thingspeak.com/channels/2375268/feeds.json?api_key=762B4RKGYC14D34F&results=2'):
    try:
        response = urequests.get(readAPIkey)
        if response.status_code == 200:
            data = response.json()

            if 'feeds' in data and data['feeds']:
                last_entry = data['feeds'][0]
                
                field_value = int(last_entry.get('field1', 0))
                if field_value == 0:
                    timer2.init(period=5000, mode=machine.Timer.PERIODIC, callback=checkMPU)
                    np[0] = (0, 255, 0)
                    np.write()
                    return
                    
                else:
                    print("not armed")
                    np[0] = (0, 0, 0)
                    np.write()
                    return None
            
            else:
                print("No data available for the specified channel and field.")
                return None
        
        else:
            print(f"Error: {response.status_code}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None
    response.close()
    

timer.init(period=30000, mode=machine.Timer.PERIODIC, callback=thingspeak)
# {'GyZ': -235, 'GyY': 296, 'GyX': 16, 'Tmp': 26.64764, 'AcZ': -1552, 'AcY': -412, 'AcX': 16892}
