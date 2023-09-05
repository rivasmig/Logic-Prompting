import os
import random
import string
import pygame

class Image:
    def __init__(self, outer_panel, image_path, width=None, height=None, position=(0, 0), max_size=None):
        self.name = self.generate_unique_name()
        self.Outer_Panel = outer_panel
        self.image_path = image_path
        self.position = position
        self.width = width
        self.height = height
        self.max_size = max_size
        self.image = self.load_image()
        
        if self.image and (width is None or height is None):
            img_width, img_height = self.image.get_size()
            if width is None:
                self.width = img_width
            if height is None:
                self.height = img_height

    def find_screen(self):
        panel = self.Outer_Panel
        while panel is not None:
            if panel.Screen is not None:
                return panel.Screen
            panel = panel.Outer_Panel
        return None

    def calculate_actual_position(self):
        x, y = self.position
        ow, oh = self.Outer_Panel.calculate_width_and_height()
        ox, oy = self.Outer_Panel.calculate_actual_position()
        
        img_width = self.width * ow
        img_height = self.height * oh

        x = ox + (ow - img_width) / 2 + x * ow
        y = oy + (oh - img_height) / 2 + y * oh
        
        return x, y

    def generate_unique_name(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name

    def load_image(self):
        if os.path.exists(self.image_path):
            return pygame.image.load(self.image_path)
        print(f"Image file {self.image_path} not found.")
        return None

    def draw(self):
        x, y = self.calculate_actual_position()
        screen = self.find_screen()
        if screen and self.image:
            screen.blit(self.image, (int(x), int(y)))

    def resize_image(self, amount):
        # Get the current size of the image
        img_width, img_height = self.image.get_size()
        
        # Calculate the new dimensions based on the scaling amount
        new_width = int(img_width * amount)
        new_height = int(img_height * amount)
        
        # Perform the actual resizing
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        panel_width, panel_height = self.Outer_Panel.calculate_width_and_height()
        
        # Store the new normalized width and height
        self.width = new_width / panel_width
        self.height = new_height / panel_height

    def automatic_resize(self, keep_aspect_ratio):
        # Get the actual size of the image
        img_width, img_height = self.image.get_size()

        # Get the size and actual position of the panel the image is in
        panel_width, panel_height = self.Outer_Panel.calculate_width_and_height()
        panel_x, panel_y = self.Outer_Panel.calculate_actual_position()

        # Compute the image's ending x and y position relative to the panel
        end_x = self.position[0] + img_width
        end_y = self.position[1] + img_height

        # Calculate how much the image exceeds the panel dimensions
        width_excess = max(0, end_x - panel_width)
        height_excess = max(0, end_y - panel_height)

        # If the image is within the panel dimensions, no resizing is needed
        if width_excess == 0 and height_excess == 0:
            return

        # Calculate new dimensions
        if keep_aspect_ratio:
            aspect_ratio = img_width / img_height
            if width_excess > height_excess:
                new_width = img_width - width_excess
                new_height = new_width / aspect_ratio
            else:
                new_height = img_height - height_excess
                new_width = new_height * aspect_ratio
        else:
            new_width = img_width - width_excess
            new_height = img_height - height_excess

        # Perform the actual resizing
        self.image = pygame.transform.scale(self.image, (int(new_width), int(new_height)))
        self.width = new_width / panel_width  # Store normalized width
        self.height = new_height / panel_height  # Store normalized height


