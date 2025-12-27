# implement a class that can generate the next point in a spiral pattern
import math

class ArchimedeanSpiral:
    def __init__(self,step=0.2,a=0.5):
        self.step = step # 0.2 radians about 11.46 degrees a small step
        self.theta = 0 # angle in radians
        self.a = a

    def next_point(self):
        # get next point in the spiral
        # r = a * θ
        self.theta += self.step
        r = self.a * self.theta
        x = r * math.cos(self.theta)
        y = r * math.sin(self.theta)

        return x,y
    
    def reset(self):
        self.theta = 0


    

        