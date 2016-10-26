from frigeometry import FriGeometry

class FriRect(FriGeometry):
    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2


    def within(self,point):

        return (p2[0]>=point['x']>=p1[0] and p2[1]>=point['y']>=p1[1])

    def drawShape(self,onFrame):
        #draw operations bla bla
        return onFrame
