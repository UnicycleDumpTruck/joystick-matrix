# joystick-matrix
NeoPixel Matrix controlled by joystick in CircuitPython

main loop:
  cursor.increment(joystick.vector)
  if butts := buttons.pressed():
    matrix.paint(butts, cursor.postion())
