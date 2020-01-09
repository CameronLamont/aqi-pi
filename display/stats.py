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
 
import time
import subprocess
 
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import atexit

import json
 
 
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
 
 
# Load default font.
font = ImageFont.load_default()
 
# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
#font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)

#function to clear the screen on exit
def disableDisplay():
    disp.poweroff()

atexit.register(disableDisplay)

while True:
 
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
 
    # Shell scripts for system monitoring from here:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%d GB  %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")

    #Crappy way to extract from json file
    #aqiHeader = "Air Quality Sensor"
    #cmd = "tail -n 1 /var/www/html/aqi.json | awk '{print \"\",$6,$7}'"
    #aqiDateTime = subprocess.check_output(cmd, shell=True).decode("utf-8")
    #cmd = "tail -n 1 /var/www/html/aqi.json | awk '{print \"PM10:\",$4}'"
    #aqipm10 = subprocess.check_output(cmd, shell=True).decode("utf-8")
    #cmd = "tail -n 1 /var/www/html/aqi.json | awk '{print \"PM2.5:\",$2}'"
    #aqipm25 = subprocess.check_output(cmd, shell=True).decode("utf-8")

    #Proper way to extract from json file by reading json structure
    with open("/var/www/html/aqi.json", "r") as read_file:
        measurementdata = json.load(read_file)
        measurement = measurementdata[-1]
        #print(measurement)
        aqipm10 = "PM10: " + str(measurement['pm10'])
        aqipm25 = "PM2.5: " + str(measurement['pm25'])
        aqiDateTime = str(measurement['time'])
    
    aqiHeader = "Air Quality Sensor"
    # Write four lines of text.
 
    #draw.text((x, top+0), "IP: "+IP, font=font, fill=255)
    #draw.text((x, top+8), CPU, font=font, fill=255)
    #draw.text((x, top+16), MemUsage, font=font, fill=255)
    #draw.text((x, top+25), Disk, font=font, fill=255)

    draw.text((x, top+0), aqiHeader, font=font, fill=255)
    draw.text((x, top+8), aqiDateTime, font=font, fill=255)
    draw.text((x, top+16), aqipm10, font=font, fill=255)
    draw.text((x, top+25), aqipm25, font=font, fill=255)
 
    # Display image.
    disp.image(image)
    disp.show()
    time.sleep(.1)
    