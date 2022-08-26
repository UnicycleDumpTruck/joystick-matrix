#! /bin/python
import time
import board
import digitalio
from adafruit_debouncer import Debouncer

"""Class for 4-switch joystick."""

REPEAT_RATE = 0.2 # Seconds between repeate for held switch

class Joystick():
  """Debounced joystick."""
  def __init__(self, up_pin, down_pin, left_pin, right_pin):
    """Initialize debounced joystick control. Pin format is board.D12"""
    self.up_pin = digitalio.DigitalInOut(up_pin)
    self.up_pin.direction = digitalio.Direction.INPUT
    self.up_pin.pull = digitalio.Pull.UP
    self.up_switch = Debouncer(self.up_pin)
    self.up_last = 0
    
    self.down_pin = digitalio.DigitalInOut(down_pin)
    self.down_pin.direction = digitalio.Direction.INPUT
    self.down_pin.pull = digitalio.Pull.UP
    self.down_switch = Debouncer(self.down_pin)
    self.down_last = 0
    
    self.left_pin = digitalio.DigitalInOut(left_pin)
    self.left_pin.direction = digitalio.Direction.INPUT
    self.left_pin.pull = digitalio.Pull.UP
    self.left_switch = Debouncer(self.left_pin)
    self.left_last = 0
    
    self.right_pin = digitalio.DigitalInOut(right_pin)
    self.right_pin.direction = digitalio.Direction.INPUT
    self.right_pin.pull = digitalio.Pull.UP
    self.right_switch = Debouncer(self.right_pin)
    self.right_last = 0
    
    
  def vector(self):
    self.up_switch.update()
    self.down_switch.update()
    self.left_switch.update()
    self.right_switch.update()

    x = 0
    y = 0
    
    if self.up_switch.fell or (self.up_last and ((time.monotonic() - self.up_last) > REPEAT_RATE)):
      y += 1
      self.up_last = time.monotonic()
    elif self.up_switch.rose:
      self.up_last_repeat = 0
      
    if self.down_switch.fell or (self.down_last and ((time.monotonic() - self.down_last) > REPEAT_RATE)):
      y -= 1
      self.down_last = time.monotonic()
    elif self.down_switch.rose:
      self.down_last_repeat = 0

    if self.left_switch.fell or (self.left_last and ((time.monotonic() - self.left_last) > REPEAT_RATE)):
      x -= 1
      self.left_last = time.monotonic()
    elif self.left_switch.rose:
      self.left_last_repeat = 0
      
    if self.right_switch.fell or (self.right_last and ((time.monotonic() - self.right_last) > REPEAT_RATE)):
      x += 1
      self.right_last = time.monotonic()
    elif self.right_switch.rose:
      self.right_last_repeat = 0
      
    return (x,y)
