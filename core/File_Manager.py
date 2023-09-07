import os
import glob
import random
import string

class File_Manager:
    def __init__(self):
        self.Folder_Paths = []
        self.Current_Folder = None
        self.Current_Image_Set = None
        self.Current_Image_Index = None
        self.Image_Extensions = ['.png', '.jpg', '.jpeg']
        self.Text_Extensions = ['.txt']
        self.logic_prompt_extension = '.logic'

    def generate_unique_name(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def Clear_Folder_Path(self):
        self.Folder_Paths.clear()
        # Create a default folder if Folder_Paths is empty
        default_folder = ("./default_folder", "Default Folder")
        os.makedirs(default_folder[0], exist_ok=True)
        self.Folder_Paths.append(default_folder)

    def Add_Folder_Path(self, folder_path, folder_name=None):
        if folder_name is None:
            folder_name = self.generate_unique_name()
        self.Folder_Paths.append((folder_path, folder_name))

    def Delete_Folder_Path(self, folder_path):
        self.Folder_Paths = [f for f in self.Folder_Paths if f[0] != folder_path]

    def Set_Current_Folder(self, folder_name):
        folder = next((f for f in self.Folder_Paths if f[1] == folder_name), None)
        if folder:
            self.Current_Folder = folder
            # Set the Current_Image_Set based on the folder contents
            images = [(i, img, "") for i, img in enumerate(glob.glob(f"{folder[0]}/*")) if img.endswith(tuple(self.Image_Extensions))]
            self.Current_Image_Set = images

    def Get_Current_Folder(self):
        if self.Current_Folder:
            return self.Current_Folder[1]
        return "None"

    def Set_Current_Image_Caption(self, text):
        if self.Current_Image_Set and self.Current_Image_Index is not None:
            _, img_path, _ = self.Current_Image_Set[self.Current_Image_Index]
            self.Current_Image_Set[self.Current_Image_Index] = (self.Current_Image_Index, img_path, text)

    def Get_Current_Image_Path(self):
        if self.Current_Image_Set and self.Current_Image_Index is not None:
            return self.Current_Image_Set[self.Current_Image_Index][1]
        return None

    def Change_Image_Index(self, index_change):
        if self.Current_Image_Index is not None:
            self.Current_Image_Index += index_change
            self.Current_Image_Index = max(0, min(self.Current_Image_Index, len(self.Current_Image_Set) - 1))

    def Output_Finished_Folder(self):
        if self.Current_Folder:
            base_name = self.Current_Folder[1]
            counter = 1
            while os.path.exists(f"{self.Current_Folder[0]}/{base_name}_{counter:03}"):
                counter += 1
            output_folder = f"{self.Current_Folder[0]}/{base_name}_{counter:03}"
            os.makedirs(output_folder, exist_ok=True)
            
            for idx, img_path, caption in self.Current_Image_Set:
                image_name = os.path.basename(img_path)
