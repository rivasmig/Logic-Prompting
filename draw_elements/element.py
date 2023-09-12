from qt_ui import logic_window as lw
class Element():
    def __init__(self):
        self.single = lw.Logic_Window.getInstance()
        self.attributes = []
        self.attributes.append('Type')
    def add_pos_attribute(self, x, y):
        self.attributes.append('Position')
        self.attributes.append((x,y))
    def add_text_attribute(self, text):
        self.attributes.append('Text')
        self.attributes.append(text)
    def remove_last_attribute(self):
        self.attributes.pop()
        self.attributes.pop()