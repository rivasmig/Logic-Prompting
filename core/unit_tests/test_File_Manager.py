import os
import unittest
import tempfile
import shutil
import random
from ..File_Manager import File_Manager
from ..media import Media

def add_files_in_folder(folder_path, file_list):
    if not os.path.isdir(folder_path):
        print(f"The provided folder path '{folder_path}' is not a valid directory.")
        return
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(str(file_path))

class TestFileManager(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for the tests
        self.test_dir = tempfile.mkdtemp()
        self.file_manager = File_Manager()
        self.sample_images_folder = 'assets/test_images'
        self.sample_Image_name = '829675_nature_512x512.png'
        self.listOfImagePaths = []  # This needs to be updated with actual image paths
        self.empty_file_manager = None
        self.single_media_file_manager = None
        self.all_images_file_manager = None
        self.random_index_file_manager = None
        

    def tearDown(self):
        # Clean up the temporary directory after each test
        shutil.rmtree(self.test_dir)

    def setUpFileManagers(self):
        # Set up image path list
        self.listOfImagePaths = []
        add_files_in_folder(self.sample_images_folder, self.listOfImagePaths)

        # Create File_Managers with different configurations
        self.empty_file_manager = File_Manager()  # 1) Empty File_Manager

        self.single_media_file_manager = File_Manager()  # 2) File_Manager with only 1 media item
        sample_image_path = os.path.join(self.sample_images_folder, self.sample_Image_name)
        self.single_media_file_manager.Add_Media_By_Path(sample_image_path)

        self.all_images_file_manager = File_Manager()  # 3) File_Manager with all images in sample_images_folder
        for image_path in self.listOfImagePaths:
            self.all_images_file_manager.Add_Media_By_Path(image_path)

        self.random_index_file_manager = File_Manager()  # 4) Same as 3, but current media index is random
        for image_path in self.listOfImagePaths:
            self.random_index_file_manager.Add_Media_By_Path(image_path)
        
        random_index = random.randint(0, len(self.listOfImagePaths) - 1)
        self.random_index_file_manager.update_index(random_index)
        self.saved_random_index = random_index

    def test_get_media_length(self):
        self.setUpFileManagers()
        # Test for empty File_Manager
        self.assertEqual(self.empty_file_manager.get_media_length(), 0)

        # Test for single media File_Manager
        self.assertEqual(self.single_media_file_manager.get_media_length(), 1)

        # Test for all images File_Manager
        self.assertEqual(self.all_images_file_manager.get_media_length(), len(self.listOfImagePaths))

        # Test for random index File_Manager
        self.assertEqual(self.random_index_file_manager.get_media_length(), len(self.listOfImagePaths))

    def test_add_media_by_path(self):
        self.setUpFileManagers()
        # Test for empty File_Manager
        test_file_path = os.path.join(self.sample_images_folder, self.sample_Image_name)
        self.empty_file_manager.Add_Media_By_Path(test_file_path)
        self.assertEqual(self.empty_file_manager.Current_Media_Index, 0)
        self.assertEqual(self.empty_file_manager.get_media_length(), 1)
        self.assertEqual(self.empty_file_manager.get_media_file_path(), test_file_path)

    def test_delete_media_by_path(self):
        self.setUpFileManagers()
        # Test for single media File_Manager
        test_file_path = os.path.join(self.sample_images_folder, self.sample_Image_name)
        self.empty_file_manager.Add_Media_By_Path(test_file_path)
        self.empty_file_manager.Delete_Media_By_Path(test_file_path)
        # should be 1, since started with 1
        self.assertEqual(self.empty_file_manager.get_media_index(), -1)
        self.assertEqual(self.empty_file_manager.get_media_length(), 0)
        
        # More tests for other configurations can be added here...

    def test_add_folder_contents(self):
        self.setUpFileManagers()
        # Test for empty File_Manager
        self.empty_file_manager.Add_Folder_Contents(self.sample_images_folder)
        self.assertEqual(self.empty_file_manager.get_media_length(), len(self.listOfImagePaths))

        # More tests for other configurations can be added here...

    def test_delete_folder_contents(self):
        self.setUpFileManagers()
        self.empty_file_manager.Add_Folder_Contents(self.sample_images_folder)
        self.empty_file_manager.Delete_Folder_Contents(self.sample_images_folder)
        self.assertEqual(self.empty_file_manager.get_media_index(), -1)
        self.assertEqual(self.empty_file_manager.get_media_length(), 0)

        # More tests for other configurations can be added here...

    def test_get_all_image_paths(self):
        self.setUpFileManagers()
        # Test for empty File_Manager
        self.assertEqual(len(self.empty_file_manager.get_all_image_paths()), 0)

        # Test for single media File_Manager
        self.assertEqual(len(self.single_media_file_manager.get_all_image_paths()), 1)
        
        # Test for all images File_Manager
        self.assertEqual(len(self.all_images_file_manager.get_all_image_paths()), len(self.listOfImagePaths))
