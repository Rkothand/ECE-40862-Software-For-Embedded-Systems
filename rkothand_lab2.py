import machine
from machine import RTC, Timer, ADC, Pin, PWM

flag =0

year = (int(input("Year? ")))
month = (int(input("Month? ")))
day = (int(input("Day? ")))
weekday = (int(input("Weekday? ")))
hour = (int(input("Hour? ")))
minute = (int(input("Minute? ")))
second = (int(input("Second? ")))
microseconds = (int(input("Microseconds? ")))

rtc = RTC()
rtc.datetime((year,month,day,weekday,hour, minute, second, microseconds))

adc = ADC(Pin(34))
adc.atten(ADC.ATTN_11DB)

    

led = Pin(27)
ledPwm = PWM(led, freq = 10, duty = 512)

frequencyInput = False
dutyControl = True

ledTimer = Timer(0)
#dutyTimer = Timer(1)

def updateLED(timer):
    potentiometer_value = adc.read()
    if flag != 0:
        if frequencyInput:
            freq = 1 + int(potentiometer_value / 4095 * 20)
            ledPwm.freq(freq)
        if dutyControl:
            duty = 1 + int(potentiometer_value / 4095 * 20)
            ledPwm.duty(duty)

ledTimer.init(period=100, mode =Timer.PERIODIC, callback=updateLED)

        
def switchPress(x):
    global frequencyInput, dutyControl, flag
    flag =1
    if frequencyInput:
        frequencyInput = False
        dutyControl = True
        print("control switched to duty cycle")
    elif dutyControl:
        frequencyInput = True
        dutyControl = False
        print("control switched to frequency")

buttonPressInterupt = Pin(38,Pin.IN,Pin.PULL_UP)
buttonPressInterupt.irq(trigger=Pin.IRQ_FALLING, handler= switchPress)

def printdatetime(x):
    print(rtc.datetime())
displayTimer = Timer(-1)   
displayTimer.init(period=30000, mode=Timer.ONE_SHOT, callback=printdatetime)
