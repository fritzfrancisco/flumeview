from frigeometry import FriGeometry

class FriRect(FriGeometry):
    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2

    def within(self,point):
        #return("Rectangle")
        return (self.p2[0]>=point[0]>=self.p1[0] and self.p2[1]>=point[1]>=self.p1[1])

    def drawShape(self,onFrame):
        #draw operations bla bla
        return onFrame
