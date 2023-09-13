import os
import glob
import random
import string
import json
from typing import List
from draw_elements import element as el
from draw_elements import point
from core.media import Media

BASEDIR = os.path.dirname(__file__)

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
        self.Current_Media:Media = None
        self.Logic_Extension = '.logic'
        self.projectName = None
        self.projectFolder = None

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
                    next_index = min(len(self.Current_Media_Set) - 1, 
                                     self.Current_Media_Index + 1)
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
        acceptable_extensions = [ext for extensions 
                                 in self.Media_Types_and_Extensions.values() 
                                 for ext in extensions]
        
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
    
    def serialize_element(self, element):
        """Convert an Element object into a serializable dictionary."""
        serialized_element = {
            'localName': element.localName,
            'type': element.attributes[1],
            'attributes': element.attributes
        }
        
        # If the element is of type 'Point', save its image attribute
        if isinstance(element, point.Point):
            serialized_element['image'] = element.image

        return serialized_element

    def deserialize_element(self, serialized_element):
        """Recreate an Element object from serialized data."""
        element_type = serialized_element['type']

        if element_type == 'Point':
            element = point.Point()
            element.image = serialized_element['image']
        else:
            # Default case for the base Element class.
            # If you add more Element subclasses, add their deserialization logic here.
            element = el.Element()

        element.attributes = serialized_element['attributes']
        element.localName = serialized_element['localName']
        return element

    def Load_Logic_File(self, logic_file_path):
        if logic_file_path.endswith(self.Logic_Extension):
            with open(logic_file_path, 'r') as file:
                data = json.load(file)
            
            # Set the project details
            self.projectName = data['projectName']
            self.projectFolder = data['projectFolder']
            
            # Create Media objects from the stored data
            for media_data in data['mediaSet']:
                media = Media(media_data['type'], media_data['file_path'], 
                            media_data['parent_folder'], media_data['name'])
                media.elements = [self.deserialize_element(element_data) 
                                  for element_data in media_data['elements']]
                self.Current_Media_Set.append(media)
            
            # Set the current media index
            self.update_index(data['currentMediaIndex'])
        else:
            print(f"Incorrect file type. Wanted type {self.Logic_Extension}")
    
    def Create_Logic_File(self):
        data = {
            'projectName': self.projectName,
            'projectFolder': self.projectFolder,
            'currentMediaIndex': self.Current_Media_Index,
            'mediaSet': []
        }
        
        for media in self.Current_Media_Set:
            media_data = {
                'type': media.type,
                'file_path': media.file_path,
                'parent_folder': media.parent_folder,
                'name': media.name,
                'elements': [self.serialize_element(element) for element in media.elements]
            }
            data['mediaSet'].append(media_data)
        
        # Store this data in a file with the custom extension inside the project folder
        logic_file_path = os.path.join(self.projectFolder, 
                                       f"{self.projectName}{self.Logic_Extension}")
        
        with open(logic_file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def get_all_image_paths(self) -> List[str]:
        return [media.file_path for media in 
                self.Current_Media_Set if media.type == "Image"]
