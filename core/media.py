from typing import List
from draw_elements import element as el
from draw_elements import point
import os

class Media:
    def __init__(self, type='Generic', file_path='', parent_folder=None, name=None):
        self.invoker = MediaInvoker()
        self.type = type
        self.file_path = file_path
        self.parent_folder = parent_folder
        self.name = name
        self.screen_position = (0,0)
        self.screen_widthHeight = (0,0)
        self.currentDrawMode = 'Select'
        self.currentBrushTrailImage = None
        self.elements: List[el.Element] = []

        if not self.check_path():
            print('broken file')

        if self.parent_folder is None:
            self.parent_folder = os.path.basename(os.path.dirname(self.file_path))

        if self.name is None:
            self.name = os.path.basename(self.file_path)

    def add_element(self, element):
        add_element_cmd = AddElementToMedia(self, element)
        self.invoker.storeAndExecute(add_element_cmd)

    def delete_element(self, element):
        delete_element_cmd = DeleteElementFromMedia(self, element)
        self.invoker.storeAndExecute(delete_element_cmd)

    def add_text_attribute_to_latest(self, text):
        add_text_attribute = AddTextAttribute(self, text)
        self.invoker.storeAndExecute(add_text_attribute)

    def print_elements(self):
        elements = self.get_elements()
        if elements:
            for e in elements:
                print(e.attributes)

    def get_elements(self):
        return self.elements

    def get_draw_mode(self):
        return self.currentDrawMode
    
    def set_draw_mode(self, mode):
        self.currentDrawMode = mode
    
    def check_path(self):
        return os.path.exists(self.file_path)
    
    def __eq__(self, other):
        if isinstance(other, Media):
            return self.parent_folder == other.parent_folder and self.name == other.name
        return False


class MediaInterface():
    def __init__(self, media):
        self.media:Media = media
        self.previous = None
        self.next = None
    
    def execute(self):
        pass

    def undo(self):
        pass

    def redo(self):
        pass

class AddElementToMedia(MediaInterface):
    def __init__(self, media, addedElement):
        super().__init__(media)
        self.addedElement = addedElement

    def execute(self):
        if isinstance(self.addedElement, el.Element):
            self.media.elements.append(self.addedElement)
        else:
            print('not an element')
    
    def undo(self):
        self.media.elements.pop()
        super().undo()
    
    def redo(self):
        self.execute()
        super().redo()

class AddTextAttribute(MediaInterface):
    def __init__(self, media, text):
        super().__init__(media)
        self.text = text
    
    def execute(self):
        self.media.elements[-1].add_text_attribute(self.text)
        super().execute()
    
    def undo(self):
        self.media.elements[-1].remove_last_attribute()
        super().undo()
        if self.media.elements[-1].getTextAttribute() == '':
            self.media.invoker.undo()
    
    def redo(self):
        self.execute()
        super().redo()

class DeleteElementFromMedia(MediaInterface):
    def __init__(self, media, element):
        super().__init__(media)
        self.element = element
        self.index_removed = None
    def execute(self):
        for idx, e in enumerate(self.media.elements):
            if e == self.element:
                self.index_removed = idx
                self.media.elements.remove(e)
                break  # Exit the loop after removing the element
        super().execute()
    def undo(self):
        if self.index_removed is not None:
            # Insert the element back to its original position
            self.media.elements.insert(self.index_removed, self.element)
        super().undo()
    def redo(self):
        self.execute()
        super().redo()

class MediaInvoker():
    def __init__(self):
        self.command_history = []
        self.undo_stack = []
    
    def storeAndExecute(self, cmd):
        cmd.execute()
        self.command_history.append(cmd)
        self.undo_stack.clear()
    
    def undo(self):
        if not self.command_history:
            return
        cmd = self.command_history.pop() # added text
        cmd.undo()
        self.undo_stack.append(cmd)
    
    def redo(self):
        if not self.undo_stack:
            return
        cmd = self.undo_stack.pop() # added element
        cmd.redo()
        self.command_history.append(cmd)
