
class FriGeometry( object ):
    """Some description that tells you it's abstract,
    often listing the methods you're expected to supply."""

    def within(self,x,y ):
        raise NotImplementedError( "Should have implemented this" )

    def drawShape(self, onFrame ):
        raise NotImplementedError( "Should have implemented this" )
