from frigeometry import FriGeometry
from frirect import FriRect
from fricirc import FriCirc

def someFunction(friGeo):
    print(friGeo.within({'x':10,'y':10}))
    print(friGeo.within({'x':1,'y':1}))


#circle
circ = FriCirc({'x':1,'y':2},4.5)

#rectangle
rect = FriRect({'x':1,'y':2},{'x':3,'y':4})

someFunction(circ)
# print()
someFunction(rect)
