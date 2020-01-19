# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Updated by Ugoogalizer 20190108 to enable exit handling to turn off display when python exits (to save OLED display)
# Note: Source code of the Python library used to interface with the OLED can be found here: 
# https://github.com/adafruit/Adafruit_CircuitPython_SSD1306/blob/master/adafruit_ssd1306.py
#
# - 20200109 - Read in aqi sensor data direct from json file
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
 
 
# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!
import sys
import time
import subprocess
 
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import atexit

import json
 
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from datetime import datetime


def redraw():
    global text_size
    global display_text
    global text_x
    global text_y

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, max(width,text_size[0]), height), outline=0, fill=0)

    draw.text((text_x,text_y),display_text,font=font32,fill=255)

    # Display image.
    disp.image(image)
    disp.show()

def read_data():
    global text_size
    global display_text
    global text_x
    global text_y

    # if True:
    try:
        #Proper way to extract from json file by reading json structure
        with open("/var/www/html/aqi.json", "r") as read_file:
            measurementdata = json.load(read_file)
            measurement = measurementdata[-1]
            #print(measurement)
            aqipm10 = "pm10:" + str(measurement['pm10'])
            aqipm25 = "pm2.5:" + str(measurement['pm25'])
            aqiDateTime = datetime.fromisoformat(measurement['time'])

        #aqiHeader = "Air Quality Sensor"

        #print(aqiHeader)
        print(aqiDateTime)
        print(aqipm25)
        print(aqipm10)

        # Write four lines of text.
        #draw.text((x, top+0), aqiHeader, font=font, fill=255)
#        draw.text((x, top+0), aqiDateTime, font=font10, fill=255)
 #       draw.text((x, top+10), aqipm25+" "+aqipm10, font=font16, fill=255)

        display_text=aqipm25+" "+aqipm10+" "+aqiDateTime.strftime("%d%b%Y %H:%M:%S")
        text_size = font32.getsize(display_text)
        text_x = x
        text_y = top+0

    except json.decoder.JSONDecodeError:
        print("JSON parse failed")
        pass
    # except:
        # e = sys.exc_info()[0]
        # print("Exception %s" % e)

def on_created(event):
    #print(f"{event.src_path} has been created!")
    read_data()
    # redraw()

def on_deleted(event):
    print(f"deleted {event.src_path}!")

def on_modified(event):
    #print(f"{event.src_path} has been modified")
    read_data()
    #redraw()

def on_moved(event):
    print(f"moved {event.src_path} to {event.dest_path}")

if __name__ == "__main__":

    patterns = ["*.json"]
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved


    path = "/var/www/html"
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    # Create the I2C interface.
    i2c = busio.I2C(SCL, SDA)
    
    # Create the SSD1306 OLED class.
    # The first two parameters are the pixel width and pixel height.  Change these
    # to the right size for your display!
    disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
    
    # Clear display.
    disp.fill(0)
    disp.show()
    
    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))
    
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)
    
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    
    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = height-padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0
    
    font_size=10

    # Load default font.
    # font = ImageFont.load_default()
    
    # Alternatively load a TTF font.  Make sure the .ttf font file is in the
    # same directory as the python script!
    # Some other nice fonts to try: http://www.dafont.com/bitmap.php
    #font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)
    font10 = ImageFont.truetype('VCR_OSD_MONO_1.001.ttf', 10)
    font16 = ImageFont.truetype('VCR_OSD_MONO_1.001.ttf', 16)
    font32 = ImageFont.truetype('VCR_OSD_MONO_1.001.ttf', 32)


    #  variable to hold current width of text in pixels
    display_text = "Air Quality Sensor"
    text_size = font32.getsize(display_text) #(128, 32)
    text_x = x
    text_y = top+0

    scroll_px = 5

    #function to clear the screen on exit
    def disableDisplay():
        disp.poweroff()
    atexit.register(disableDisplay)

    # draw file content up front
    read_data()
    redraw()
    my_observer.start()
    
    try:
        while True:

            if text_size[0] > 128:
                time.sleep(2)
                print("scrolling left")
                while text_x > x - (text_size[0]-128):
                # for i in range(128,text_size[0]),-scroll_px:
                    text_x -= scroll_px
                    redraw()
                    # disp.scroll(-6,0)
                    # disp.show()
                    time.sleep(0.01)
                    # print(text_x)

                time.sleep(2)
                print("scrolling right")
                # for i in range(128,text_size[0],scroll_px):
                while text_x < x:
                    text_x += scroll_px
                    redraw()
                    # disp.scroll(6,0)
                    # disp.show()
                    time.sleep(0.01)
                    # print(text_x)
                

            time.sleep(0.01)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
    finally:
        disableDisplay()
