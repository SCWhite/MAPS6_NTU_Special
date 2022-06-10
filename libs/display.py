# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
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

import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime

#fix here
#DEVICE_ID = ""
#DEVICE_IP = ""


# Raspberry Pi pin configuration:
RST = 24

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)


FONT_SIZE = 10

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
#padding = 2
#shape_width = 20
#top = padding
#bottom = height-padding

# Move left to right keeping track of the current x position for drawing shapes.
#x = padding

# Load default font.
#font = ImageFont.load_default()
font=ImageFont.truetype("../NotoSans-Medium.ttf", FONT_SIZE)
#font=ImageFont.truetype("../TaipeiSansTCBeta-Regular.ttf", s)
#font=ImageFont.truetype("../5x7_practical.ttf", s)

#set anchor
anchor_x = 0
anchor_y = 0

'''
# Write two lines of text.
draw.text((x, top),    'Hello',  font=font, fill=255)
draw.text((x, top+20), 'World!', font=font, fill=255)

# Display image.
disp.image(image)
disp.display()
'''

def set_size(s):
    global FONT_SIZE
    global font
    FONT_SIZE = s
    #font=ImageFont.truetype("../NotoSans-Medium.ttf", FONT_SIZE)

def show():
    disp.image(image)
    disp.display()

def clear():
    global anchor_x
    global anchor_y
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    show()
    anchor_x = 0
    anchor_y = 0

def setCursor(x,y):
    global anchor_x
    global anchor_y
    anchor_x = x
    anchor_y = y

def flush():
    global anchor_x
    global anchor_y
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    anchor_x = 0
    anchor_y = 0


#------------------------------------------------------------#

def draw_text(x,y,str):
    global FONT_SIZE
    draw.text((x, y*FONT_SIZE),str,  font=font, fill=255)
    show()


def draw_text_size(x,y,str,s=FONT_SIZE):
    global FONT_SIZE
    font=ImageFont.truetype("../NotoSans-Medium.ttf", s)
    draw.text((x, y*FONT_SIZE),str,  font=font, fill=255)
    show()

def line(in_str,s=FONT_SIZE):
    global FONT_SIZE
    global anchor_x
    global anchor_y
    font=ImageFont.truetype("../NotoSans-Medium.ttf", s)
    draw.text((anchor_x, anchor_y),in_str,  font=font, fill=255)
    #show()
    anchor_y = anchor_y + s

def display(DEVICE_ID="",temp=0,hum=0,pm25=0,co2=0,tvoc=0,flag="",version=""):
    #oled.clear()
    flush()
    pairs = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S").split(" ")
    line("ID: " + DEVICE_ID,14)
    #line("Date: " + str(pairs[0]))
    #line("Time: " + str(pairs[1]))
    line("Date: " + str(pairs[0]) + " " +str(pairs[1]))
    line("Temp: " + str(temp) + " / " + "RH: " + str(hum))
    line("PM2.5: " + str(pm25) + " μg/m3")
    line("TVOC: " + str(tvoc) + " ppb")
    if(co2 != 65535):
        line("CO2: " + str(co2) + " ppm")
    draw.text((76, 51),"v " + version,  font=font, fill=255)
    draw.text((117, 51),flag,  font=font, fill=255)
    #line("IP: " + DEVICE_IP)
    show()



'''
def line_d(in_str,s=FONT_SIZE):
    global FONT_SIZE
    global anchor_x
    global anchor_y
    font=ImageFont.truetype("../NotoSans-Medium.ttf", s)
    draw.text((anchor_x, anchor_y), in_str + ' ' + str(anchor_y), font=font, fill=255)
    show()
    anchor_y = anchor_y + s

def line_n(in_str,s=FONT_SIZE):
    global FONT_SIZE
    global anchor_x
    global anchor_y
    #font=ImageFont.truetype("../NotoSans-Medium.ttf", s)
    #font = ImageFont.load_default()
    font=ImageFont.truetype("../TaipeiSansTCBeta-Regular.ttf", s)
    draw.text((anchor_x, anchor_y), in_str + ' ' + str(anchor_y), font=font, fill=255)
    show()
    anchor_y = anchor_y + s

def line_57(in_str,s=FONT_SIZE):
    global FONT_SIZE
    global anchor_x
    global anchor_y
    font=ImageFont.truetype("../5x7_practical.ttf", s)
    draw.text((anchor_x, anchor_y), in_str + ' ' + str(anchor_y), font=font, fill=255)
    show()
    anchor_y = anchor_y + s
'''
