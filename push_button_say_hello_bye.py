#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import sys

import TypetalkApi

BTN_PIN = 12
LED_PIN = 11
BOUNCE_TIME = 3000
ON = False

ApiHelper = None

def init():
    global ApiHelper
    if (None != sys.argv) and len(sys.argv) > 2:
        KEY = sys.argv[1]
        SECRET = sys.argv[2]
        auth = TypetalkApi.TypetalkAuthentication(KEY, SECRET)
        ApiHelper = TypetalkApi.TypetalkApiHelper(auth)

def buttonClickCallback(channel):
    #print "Clicked"
    global ApiHelper
    if None == ApiHelper:
        init()

    global ON
    ON = (not ON)
    if ON:
        result = TypetalkApi.sendMessage(ApiHelper, "13575", "@nulab+ hello")
        if not result:
            print "Send message fail"
        else:
            result = TypetalkApi.receiveMessage(ApiHelper, "13575", '(?<=Hello )john')
            if result:
                print "Got it"
                GPIO.output(LED_PIN, GPIO.HIGH)
            else:
                print "No...."
                ON = (not ON)    
    else:
        result = TypetalkApi.sendMessage(ApiHelper, "13575", "@nulab+ bye")
        if not result:
            print "Send message fail"
        else:
            result = TypetalkApi.receiveMessage(ApiHelper, "13575", '(?<=Bye )john')
            if result:
                print "Got it"
                GPIO.output(LED_PIN, GPIO.LOW)
            else:
                print "No...."
                ON = (not ON)

if (None == sys.argv) or len(sys.argv) <= 2:
    print "Not enough command arguments"
    exit()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)
try:
    GPIO.add_event_detect(BTN_PIN, GPIO.FALLING, callback=buttonClickCallback, bouncetime=BOUNCE_TIME)
    while True:
        print "listening..."
        time.sleep(10)
except KeyboardInterrupt:
    GPIO.cleanup()
