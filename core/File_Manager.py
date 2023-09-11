import os
import glob
import random
import string
from typing import List
from core import Canvas_Manager as cm
from draw_elements import element as el

BASEDIR = os.path.dirname(__file__)

class Media:
    def __init__(self, type='Generic', file_path='', parent_folder=None, name=None):
        self.type = type
        self.file_path = file_path
        self.parent_folder = parent_folder
        self.name = name
        self.screen_position = (0,0)
        self.screen_widthHeight = (0,0)
        self.canvasManager = cm.CanvasManager()

        if not self.check_path():
            print('broken file')

        if self.parent_folder is None:
            self.parent_folder = os.path.basename(os.path.dirname(self.file_path))

        if self.name is None:
            self.name = os.path.basename(self.file_path)

    def add_element(self, element):
        if isinstance(element, el.Element):
            self.canvasManager.elements.append(element)
        else:
            print('not an element')

    def get_elements(self):
        return self.canvasManager.elements

    def get_draw_mode(self):
        return self.canvasManager.currentDrawMode
    
    def set_draw_mode(self, mode):
        self.canvasManager.currentDrawMode = mode
    
    def check_path(self):
        return os.path.exists(self.file_path)
    
    def __eq__(self, other):
        if isinstance(other, Media):
            return self.parent_folder == other.parent_folder and self.name == other.name
        return False

class File_Manager:
    def __init__(self):
        self.Media_Types_and_Extensions = {
            'Generic': [],
            'Image': ['.png', '.jpg', '.jpeg', 'webp'],
            'Video': ['.mp4', '.webm'],
            'Sound': ['.mp3', '.wav'],
            'Text': ['.txt'],
        }
        self.Current_Media_Set: List[Media] = []
        self.Current_Media_Index = -1
        self.Current_Media: Media = None
        self.Logic_Extension = '.logic'

    def generate_unique_string(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def get_media_length(self):
        return len(self.Current_Media_Set)

    def get_media_file_path(self):
        return self.Current_Media.file_path
    
    def get_media_path_by_index(self, index):
        if (index > -1) and (index < len(self.Current_Media_Set)):
            return self.Current_Media_Set[index].file_path
        else:
            return None
    
    def get_media_index(self):
        return self.Current_Media_Index

    def get_media_obj_by_index(self, index):
        if (index > -1) and (index < len(self.Current_Media_Set)):
            return self.Current_Media_Set[index]
        else:
            return None

    def determine_media_type(self, file_path):
        extension = os.path.splitext(file_path)[-1]
        for media_type, extensions in self.Media_Types_and_Extensions.items():
            if extension in extensions:
                return media_type
        return 'Generic'

    def reset_current(self, before: Media, after: Media, isCurrent: bool):
        if isCurrent:
            if after is None:
                if before is None:
                    if self.Current_Media_Set[0] is None:
                        self.Current_Media = None
                        self.Current_Media_Index = -1
                        return
                    else:
                        self.Current_Media = self.Current_Media_Set[0]
                        self.Current_Media_Index = 0
                        return
                else:
                    self.Current_Media = before
                    self.Current_Media_Index = self.Current_Media_Set.index(before)
                    return
            else:
                self.Current_Media = after
                self.Current_Media_Index = self.Current_Media_Set.index(after)
                return
        else:
            self.Current_Media_Index -= (self.Current_Media_Set.index(before) + 1)

    def Add_Media_By_Path(self, file_path):
        media = Media(self.determine_media_type(file_path), file_path)
        self.Current_Media_Set.append(media)
        if self.Current_Media is None:
            self.Current_Media = media
            self.Current_Media_Index = 0
        print(self.get_media_length())

    def Delete_Media_By_Path(self, file_path):
        copy_m = Media(self.determine_media_type(file_path), file_path)
        for m in self.Current_Media_Set:
            if copy_m == m:
                self.Current_Media_Set.remove(m)
                if self.Current_Media == m:
                    prev_index = max(0, self.Current_Media_Index - 1)
                    next_index = min(len(self.Current_Media_Set) - 1, self.Current_Media_Index + 1)
                    self.reset_current(self.Current_Media_Set[prev_index], 
                                       self.Current_Media_Set[next_index], True)
                else:
                    index = self.Current_Media_Set.index(m)
                    prev_index = max(0, index - 1)
                    next_index = min(len(self.Current_Media_Set) - 1, index + 1)
                    self.reset_current(self.Current_Media_Set[prev_index], 
                                       self.Current_Media_Set[next_index],
                                       False)

    def Add_Folder_Contents(self, folder_path):
        folder_contents = glob.glob(os.path.join(folder_path, '*'))
        
        # flatten the list of acceptable extensions
        acceptable_extensions = [ext for extensions in self.Media_Types_and_Extensions.values() for ext in extensions]
        
        for f in folder_contents:
            # check if file has an acceptable extension
            if os.path.splitext(f)[-1] in acceptable_extensions:
                self.Add_Media_By_Path(f)
        if self.Current_Media_Index == -1:
            self.Current_Media_Index = 0

    def Delete_Folder_Contents(self, folder_path):
        folder_contents = glob.glob(os.path.join(folder_path, '*'))
        for f in folder_contents:
            self.Delete_Media_By_Path(f)

    def update_index(self, int):
        if self.get_media_obj_by_index(int) is not None:
            self.Current_Media = self.get_media_obj_by_index(int)
            self.Current_Media_Index = int
        else:
            print('Invalid media index')
    
if __name__ == '__main__':
    print('bob')