from frigeometry import FriGeometry

class FriCirc(FriGeometry):
    def __init__(self,center,radius):
        self.center = center
        self.radius = radius

    def within(self,point):
        #bla bla liegt der point im circle?
        return (point['x'] - self.center['x'])^2 + (point['y'] - self.center['y'])**2 < self.radius**2

    def drawShape(self,onFrame):

        return onFrame
