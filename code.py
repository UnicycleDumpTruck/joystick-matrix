import time
from time import sleep
from collections import deque
import board
import neopixel
import digitalio as dio
from adafruit_debouncer import Debouncer

import joystick
import cursor

TAIL_LENGTH = 8

js = joystick.Joystick(board.D13, board.D12, board.D11, board.D10)
curs = cursor.Cursor(8,8)

btn_a_pin = dio.DigitalInOut(board.D9)
btn_a_pin.direction = dio.Direction.INPUT
btn_a_pin.pull = dio.Pull.UP
btn_a = Debouncer(btn_a_pin)

btn_b_pin = dio.DigitalInOut(board.D6)
btn_b_pin.direction = dio.Direction.INPUT
btn_b_pin.pull = dio.Pull.UP
btn_b = Debouncer(btn_b_pin)

pixel_pin = board.D4

num_pixels = 64
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=255, auto_write=True, pixel_order=ORDER
)

pixels.fill((0,0,0))


class Mtx():
    def __init__(self, height, width, neopixels):
        self.height = height
        self.width = width
        self.pixels = neopixels
        self.length = height * width

        self.x_cursor_row = list(range(0,self.width))
        self.y_cursor_column = [self.width * y for y in range(0,self.height)] 
        
        self.tail = deque([0], TAIL_LENGTH) # Track pixel path behind cursor, fade end to black

        print(self.locations)

    def set_pixel(self, xy, color):
        """Given xy tuple and RGB color tuple, set pixel to color."""
        line_position = (xy[1] * self.width) + xy[0]
        self.pixels[line_position] = color
        outgoing = tail.popleft()
        self.pixels[outgoing] = (0,0,0)
        print(f"Popped {outgoing} from tail")
        tail.append(line_position)
        print(f"Appended {line_position} to tail")

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


mat = Mtx(8,8, pixels)
brush_color = [255, 0, 255]

print("Boot complete, starting loop...")

while True:
    btn_a.update()
    btn_b.update()
    jsv = js.vector()
    if jsv != (0,0):
        curs.increment_vector(jsv)
        c_pos = curs.position()
        mat.set_cursor(c_pos, (0,255,0))
        # mat.set_pixel((0, c_pos[0]), (0,255,0))
        # mat.set_pixel((c_pos[1], 0), (0,255,0))
        mat.set_pixel(curs.position(), brush_color)
    print(f"Joystick: {jsv}, cursor now: {curs.position()}")
    # print(curs.position())
    if btn_a.fell:
        if brush_color[0] == 0:
            brush_color[0] = 255
            print("Added red")
        else:
            brush_color[0] = 0
            print("Subtracted red")
    if btn_b.fell:
        if brush_color[2] == 0:
            brush_color[2] = 255
            print("Added blue")
        else:
            brush_color[2] = 0
            print("Subtracted blue")

