import time
from random import choice
from time import sleep
import board
import neopixel
import digitalio as dio
from adafruit_debouncer import Debouncer


lever_pin = dio.DigitalInOut(board.D10)
lever_pin.direction = dio.Direction.INPUT
lever_pin.pull = dio.Pull.UP
lever = Debouncer(lever_pin)


# On CircuitPlayground Express, and boards with built in status NeoPixel -> board.NEOPIXEL
# Otherwise choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D1
pixel_pin = board.NEOPIXEL #D4

# On a Raspberry pi, use this instead, not all pins are supported
# pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 1 #64

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
        print(self.locations)

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


class Knob():
    def __init__(self, seesaw, matrix: Mtx, color):
        self.seesaw = seesaw
        self.matrix = matrix
        self.color = color
        seesaw_product = (self.seesaw.get_version() >> 16) & 0xFFFF
        print(f"Found product {seesaw_product}")
        if seesaw_product != 4991:
            print("Wrong firmware loaded?  Expected 4991")

        self.button = sdio.DigitalIO(seesaw, 24)
        self.button_held = False
        self.encoder = rotaryio.IncrementalEncoder(self.seesaw)
        self.last_position = 0
        self.last_change = 0

    def update(self):
        position = -self.encoder.position
        if position > self.last_position:
            print(f"Position increased to: {position}, diff {position - self.last_position}")
            if ((position - self.last_change) > RESOLUTION):
                # print("ADD "*15)
                self.matrix.add_pxls(1, self.color)
                self.last_change = position
            self.last_position = position
        elif position < self.last_position:
            print(f"Position decreased to: {position}, diff {self.last_position - position}")
            if ((self.last_change - position) > RESOLUTION):
                # print("REMOVE "*15)
                self.matrix.remove_pxls(1, self.color)
                self.last_change = position
            self.last_position = position
        if not self.button.value and not self.button_held:
            self.button_held = True
            print("Button pressed")
        if self.button.value and self.button_held:
            self.button_held = False
            print("Button released")



print("Boot complete, starting loop...")

while True:
    lever.update()
    if lever.rose or lever.fell:
        print("Button changed!")

