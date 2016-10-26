from frigeometry import FriGeometry

class FriCirc(FriGeometry):
    def __init__(self,center,radius):
        self.center = center
        self.radius = radius

    def within(self,point):
        #bla bla liegt der point im circle?
        return (point[0] - self.center[0])**2 + (point[1] - self.center[1])**2 < self.radius**2

    def drawShape(self,onFrame):

        return onFrame
