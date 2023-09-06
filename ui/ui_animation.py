import random
import string

class ui_animation:
    def __init__(self, draw_order=0):
        self.draw_order = 0
        self.Name = self.generate_unique_name()

    def generate_unique_name(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def get_draw_order_value(self):
        return self.draw_order
    
    def set_draw_order_value(self, int):
        self.draw_order = int

    def draw(self):
        pass