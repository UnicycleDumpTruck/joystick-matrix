#! /bin/python
"""Cursor for LED matrix drawing."""

class Cursor():
  def __init__(self, width, height):
    self.x_max = width - 1
    self.y_max = height - 1
    self.x = 0
    self.y = 0
    
  def increment_vector(self, xy)
    x_inc, y_inc = *xy
    self.x += x_inc
    self.x = min(self.x_max, self.x)
    self.x = max(0, self.x)
    self.y += y_inc
    self.y = min(self.y_max, self.y)
    self.y = max(0, self.y)
    
  def set_to(self, xy)
    self.x, self.y = *xy
