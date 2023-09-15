import os
import unittest
import tempfile
import shutil

from ..File_Manager import File_Manager
from ..media import Media
from draw_elements import element

class TestMedia(unittest.TestCase):
    def setUp(self):
        # make an empty Media obj
        # make a couple Media Obj from a random image in assets/test_images
        # of those:
        # - make one with no elements
        # - make one with a single element
        # - make one with 5 elements
        # these will be used for testing
        pass
    def tearDown(self) -> None:
        return super().tearDown()
    def test_add_element(self):
        pass
    def test_delete_element(self):
        pass
    def test_add_text_attribute_to_latest(self):
        pass
    def test_get_elements(self):
        pass
