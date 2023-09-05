import random
import string
import pygame
from . import UI_Manager

class Panel:
    def __init__(self, outer_panel=None, width=0, height=0, position=(0, 0),
                 color=(255, 255, 255), transparency=1, shadow_transparency=0,
                 shadow_offset=(0, 0), is_visible=True, screen=None):
        
        self.Name = self.generate_unique_name(outer_panel)
        self.Outer_Panel = outer_panel
        self.Width = width
        self.Height = height
        self.Position = position
        self.Color = color
        self.Transparency = transparency
        self.Shadow_Transparency = shadow_transparency
        self.Shadow_Offset = shadow_offset
        self.Panel_Manager = UI_Manager.UI_Manager()  # Replace with your actual UI_Manager class
        self.Is_Visible = is_visible
        self.Screen = screen

    def generate_unique_name(self, outer_panel):
        while True:
            name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            if not self.is_name_taken(name, outer_panel):
                return name

    def is_name_taken(self, name, panel):
        if panel is None:
            return False
        if panel.Name == name:
            return True
        return self.is_name_taken(name, panel.Outer_Panel)

    def find_screen(self):
        panel = self
        while panel is not None:
            if panel.Screen is not None:
                return panel.Screen
            panel = panel.Outer_Panel
        return None

    def calculate_width_and_height(self):
        width, height = self.Width, self.Height
        if self.Outer_Panel:
            ow, oh = self.Outer_Panel.calculate_width_and_height()
            width *= ow
            height *= oh
        return width, height

    def calculate_actual_position(self):
        x, y = self.Position
        if self.Outer_Panel:
            ox, oy = self.Outer_Panel.calculate_actual_position()
            ow, oh = self.Outer_Panel.calculate_width_and_height()
            x = ox + x * ow
            y = oy + y * oh
        return x, y

    def draw(self):
        if not self.Is_Visible:
            return
        
        screen = self.find_screen()
        if screen is None:
            return

        x, y = self.calculate_actual_position()
        width, height = self.calculate_width_and_height()

        # If there's an Outer_Panel, set the clip
        if self.Outer_Panel is not None:
            ox, oy = self.Outer_Panel.calculate_actual_position()
            ow, oh = self.Outer_Panel.calculate_width_and_height()
            screen.set_clip(pygame.Rect(ox, oy, ow, oh))

        # Draw shadow first
        if self.Shadow_Transparency > 0:
            shadow_x = x + self.Shadow_Offset[0]
            shadow_y = y + self.Shadow_Offset[1]
            shadow_color = (0, 0, 0, self.Shadow_Transparency)
            pygame.draw.rect(screen, shadow_color, (shadow_x, shadow_y, width, height))

        # Draw the panel itself
        pygame.draw.rect(screen, self.Color, (x, y, width, height))

        # Draw elements managed by Panel_Manager
        self.Panel_Manager.draw()

        # Remove the clipping area to allow drawing on the entire screen again
        screen.set_clip(None)

    def hide_Panel(self):
        self.Is_Visible = False

    def show_Panel(self):
        self.Is_Visible = True
        self.draw()

    def set_Position(self, x, y):
        self.Position = (x, y)

    def set_Width(self, width):
        self.Width = width

    def set_Height(self, height):
        self.Height = height

    def set_Position_User(self, mouse_x, mouse_y):
        # Calculate position in terms of Outer_Panel
        screen = self.find_screen()
        if screen is None:
            return
        screen_width, screen_height = screen.get_size()
        panel_x, panel_y = self.calculate_actual_position()
        rel_x = (mouse_x - panel_x) / screen_width
        rel_y = (mouse_y - panel_y) / screen_height
        self.Position = (rel_x, rel_y)

    def set_Width_User(self, mouse_x):
        # Calculate width in terms of Outer_Panel
        screen = self.find_screen()
        if screen is None:
            return
        screen_width, _ = screen.get_size()
        panel_x, _ = self.calculate_actual_position()
        rel_width = (mouse_x - panel_x) / screen_width
        self.Width = rel_width

    def set_Height_User(self, mouse_y):
        # Calculate height in terms of Outer_Panel
        screen = self.find_screen()
        if screen is None:
            return
        _, screen_height = screen.get_size()
        _, panel_y = self.calculate_actual_position()
        rel_height = (mouse_y - panel_y) / screen_height
        self.Height = rel_height

    def set_Color(self, color):
        self.Color = color
