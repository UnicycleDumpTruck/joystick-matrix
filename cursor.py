"""Cursor for LED matrix drawing."""

class Cursor():
  def __init__(self, width, height):
    self.x_max = width - 1
    self.y_max = height - 1
    self.x = 0
    self.y = 0
  
  def position(self):
    return (self.x, self.y)

  def increment_vector(self, xy):
    """Increment cursor by vector."""
    x_inc = xy[0]
    y_inc = xy[1]
    self.x += x_inc
    self.x = min(self.x_max, self.x)
    self.x = max(1, self.x)
    self.y += y_inc
    self.y = min(self.y_max, self.y)
    self.y = max(1, self.y)
    
  def set_to(self, xy):
    self.x = xy[0]
    self.y = xy[1]
