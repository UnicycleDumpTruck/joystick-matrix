import time
from random import choice
from time import sleep
import board
import neopixel
import digitalio as dio
from adafruit_debouncer import Debouncer

import joystick
import cursor

js = joystick.Joystick(board.D13, board.D12, board.D11, board.D10)
curs = cursor.Cursor(8,8)

lever_pin = dio.DigitalInOut(board.D9)
lever_pin.direction = dio.Direction.INPUT
lever_pin.pull = dio.Pull.UP
lever = Debouncer(lever_pin)


# On CircuitPlayground Express, and boards with built in status NeoPixel -> board.NEOPIXEL
# Otherwise choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D1
pixel_pin = board.D4

# On a Raspberry pi, use this instead, not all pins are supported
# pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 64

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=255, auto_write=True, pixel_order=ORDER
)


pixels.fill((0,0,64))
#pixels.show()

RESOLUTION = 1  # Only change on every nth position.


class Mtx():
    colors = {'off': (0, 0, 0), 'red': (255, 0, 0),
              'green': (0, 255, 0), 'blue': (0, 0, 255)}

    color_names= {(0, 0, 0): 'off', (255, 0, 0):'red',
              (0, 255, 0):'green', (0, 0, 255):'blue'}


    def __init__(self, height, width, neopixels):
        self.height = height
        self.width = width
        self.pixels = neopixels
        self.length = height * width
        self.line = [Mtx.colors['off'] for _ in range(self.length)]
        self.locations = {key: [] for key in Mtx.colors.keys()}
        self.locations['off'] = [i for i in range(self.length)]

        self.x_cursor_row = list(range(0,self.width))
        self.y_cursor_column = [self.width * y for y in range(0,self.height)] 
                
        print(self.locations)

    def set_pixel(self, xy, color):
        """Given xy tuple and RGB color tuple, set pixel to color."""
        line_position = (xy[1] * self.width) + xy[0]
        self.pixels[line_position] = color
    def set_cursor(self, xy, color):
        for px in self.x_cursor_row:
            self.pixels[px] = (0,0,0)
        for py in self.y_cursor_column:
            self.pixels[py] = (0,0,0)
        self.pixels[self.x_cursor_row[xy[0]]] = (0,255,0)
        self.pixels[self.y_cursor_column[xy[1]]] = (0,255,0)


    def print_grid(self):
        for row in range(self.height):
            for column in range(self.width):
                print(str(self.line[row*column + column]).strip(), end="  ")
            print("")
        self.show_grid()

    def show_grid(self):
        for i, pxl in enumerate(self.line):
            self.pixels[i] = pxl
        self.pixels.show()

    def add_pxls(self, number, color):
        for _ in range(number):
            if len(self.locations['off']):
                loc = choice(self.locations['off'])
                self.line[loc] = Mtx.colors[color]
                self.pixels[loc] = Mtx.colors[color]
                self.locations['off'].remove(loc)
                self.locations[color].append(loc)
            else:
                print("No off pixels.")
        # self.print_grid()

    def remove_pxls(self, number, color):
        for _ in range(number):
            if len(self.locations[color]):
                loc = choice(self.locations[color])
                self.line[loc] = Mtx.colors['off']
                self.pixels[loc] = Mtx.colors['off']
                self.locations[color].remove(loc)
                self.locations['off'].append(loc)
            else:
                print(f"No more {color} pixels left.")
        # self.print_grid()
    def push(self, index, color):
        # print(f"Pushing index:{index} color:{color}")
        prev_color = Mtx.color_names[self.line[index]]
        self.locations[color].append(index)
        self.locations[prev_color].remove(index)
        self.line[index] = Mtx.colors[color]
        self.pixels[index] = Mtx.colors[color]
    def pop(self, index):
        color = Mtx.color_names[self.line[index]]
        # print(f"Index: {index} Color name:{color}")
        self.locations[color].remove(index)
        self.line[index] = Mtx.colors['off']
        self.locations['off'].append(index)
        self.pixels[index] = Mtx.colors['off']
        return color


mat = Mtx(8,8, pixels)

print("Boot complete, starting loop...")

while True:
    lever.update()
    jsv = js.vector()
    if jsv != (0,0):
        curs.increment_vector(jsv)
        c_pos = curs.position()
        mat.set_cursor(c_pos, (0,255,0))
        # mat.set_pixel((0, c_pos[0]), (0,255,0))
        # mat.set_pixel((c_pos[1], 0), (0,255,0))
    print(f"Joystick: {jsv}, cursor now: {curs.position()}")
    # print(curs.position())
    if lever.rose or lever.fell:
        print("Button changed!")
    if lever.fell:
        mat.set_pixel(curs.position(), (255,0,0))

