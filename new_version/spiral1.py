# in this file we create a spiral to generate positions
import math

def ArchimedeanSpiral(step=0.5):
    t = 0.0
    while True:
        r = step * t
        x = r * math.cos(t)
        y = r * math.sin(t)
        yield x,y
        t += 0.2