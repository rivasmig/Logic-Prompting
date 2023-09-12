from draw_elements import element
import os

class Point(element.Element):
    def __init__(self):
        super().__init__()
        self.image = os.path.join(self.single.BASEDIR, 'assets/icons/pointLilSquare.png')
        self.attributes.append('Point')