from qt_ui import logic_window as lw
import random
import string

class Element():
    def __init__(self):
        self.single = lw.Logic_Window.getInstance()
        self.attributes = []
        self.localName = self.generate_unique_string()
        self.attributes.append('Type')
    def generate_unique_string(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    def add_pos_attribute(self, x, y):
        self.attributes.append('Position')
        self.attributes.append((x,y))
    def add_text_attribute(self, text):
        self.attributes.append('Text')
        self.attributes.append(text)
    def add_non_standardized_attributes(self, text):
        self.attributes.append('Other')
        self.attributes.append(text)
    def remove_last_attribute(self):
        self.attributes.pop()
        self.attributes.pop()
    def getTextAttribute(self):
        if 'Text' in self.attributes:
            return self.attributes[self.attributes.index('Text') + 1]
        else:
            return ''
    def  get_non_standardized_attributes(self):
        pass
    def __eq__(self, other):
        if isinstance(other, Element):
            if other.localName == self.localName:
                return True
        return False