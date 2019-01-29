import time
from random import randint
from pythonwifi.iwlibs import Wireless
import RPi.GPIO as GPIO

SLEEP = 0.05
GPIO.setmode(GPIO.BCM)
WIFI_CARD_NAME = 'wlan0'    #NAME OF NETWORK CARD TO MONITOR
wifi = Wireless(WIFI_CARD_NAME)
leds = [
    17,27,22,23,24,25,16,26,4,18
]


def setup():    #Set the raspberry pins to output mode and do a little lightshow
    leds.reverse()
    print ("Setting up pins...")
    for pin in leds:
        GPIO.setup(pin, GPIO.OUT) 

    print ("Running startup sequence...")
    for pin in leds:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(SLEEP)
        GPIO.output(pin, GPIO.LOW)

    for pin in leds[::-1]:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(SLEEP)
        GPIO.output(pin, GPIO.LOW)

    for x in range(0,50):
        led = randint(0,9)
        GPIO.output(leds[led], GPIO.HIGH)
        time.sleep(0.025)
        GPIO.output(leds[led], GPIO.LOW)


#THRESHOLDS
#230+ Sweet life
#220-230 Still life
#215-220 Good
#210-215 Good
#205-210 Good
#200-205 OK
#195-200 Deteriorating
#190-195 Uh oh
#185-190 Halp
#<185 RIP

def main():
    wifivalue = 0
    shiny = 0
    try:
        setup()
        while True:
            #Check signal strength and turn on correct amount of leds
            wifivalue = wifi.getStatistics()[1].getSignallevel()
            print (wifivalue)
            if wifivalue > 230:
                shiny = 10
            elif wifivalue > 220:
                shiny = 9
            elif wifivalue > 215:
                shiny = 8
            elif wifivalue > 210:
                shiny = 7
            elif wifivalue > 205:
                shiny = 6
            elif wifivalue > 200:
                shiny = 5
            elif wifivalue > 195:
                shiny = 4
            elif wifivalue > 190:
                shiny = 3
            elif wifivalue > 185:
                shiny = 2
            elif wifivalue <= 185:
                shiny = 1
            
            print (shiny)

            for x in range(0,shiny):
                GPIO.output(leds[x], GPIO.HIGH)
            for x in range(shiny, 10):
                GPIO.output(leds[x], GPIO.LOW)
            
            #Update every second
            time.sleep(1)
            
    except KeyboardInterrupt:
            print("\nKeyboard interrupt!")
    except Exception as e:
            print(e)
    finally:
            GPIO.cleanup()


if __name__ == "__main__":
    main()