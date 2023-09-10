from draw_elements import element as el
from typing import List

class CanvasManager():
    def __init__(self):
        self.currentDrawMode = 'Select'
        self.currentBrushTrailImage = None
        self.elements: List[el.Element] = []