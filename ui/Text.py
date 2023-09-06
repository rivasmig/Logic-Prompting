import random
import string
import pygame
import textwrap

class Text:
    def __init__(self, outer_panel, text, pos=(0, 0), font_size=24, color=None, bg_color=None,
                 outline_width=0, outline_color=None, wrap_width=None):
        self.Name = self.generate_unique_name()
        self.Outer_Panel = outer_panel
        self.text = text
        self.pos = pos
        self.font_size = font_size
        self.font = pygame.font.Font(None, self.font_size)
        self.color = color
        self.bg_color = bg_color
        self.outline_width = outline_width
        self.outline_color = outline_color
        self.wrap_width = wrap_width
        self.draw_order = 0

        self.draw()

    def get_draw_order_value(self):
        return self.draw_order
    
    def set_draw_order_value(self, int):
        self.draw_order = int

    def generate_unique_name(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name

    def update(self):
        self.lines = textwrap.wrap(self.text, self.wrap_width) if self.wrap_width else [self.text]
        self.surfaces = [self.font.render(line, True, self.color, self.bg_color) for line in self.lines]

    def find_screen(self):
        panel = self.Outer_Panel
        while panel is not None:
            if panel.Screen is not None:
                return panel.Screen
            panel = panel.Outer_Panel
        return None

    def calculate_actual_position(self):
            x, y = self.pos
            ow, oh = self.Outer_Panel.calculate_width_and_height()
            ox, oy = self.Outer_Panel.calculate_actual_position()
            
            # Calculate the width and height of the button
            txt_width = len(self.text)*0.314*self.font_size
            txt_height = self.font_size
            
            # Adjust the position so (0,0) represents the center of the panel
            x = ox + (ow - txt_width) / 2 + x * ow
            y = oy + (oh - txt_height) / 2 + y * oh
            
            return x, y

    def draw(self):
        self.update()
        screen = self.find_screen()
        if screen is None:
            return

        # Calculate the actual position using Outer_Panel
        x, y = self.calculate_actual_position()
        ow, oh = self.Outer_Panel.calculate_width_and_height()
        x += self.pos[0] * ow
        y += self.pos[1] * oh

        # Set the clipping area to the dimensions of the Outer_Panel
        ox, oy = self.Outer_Panel.calculate_actual_position()
        screen.set_clip(pygame.Rect(ox, oy, ow, oh))

        for i, text_surface in enumerate(self.surfaces):  # Changed this line
            if self.outline_width > 0:
                outline_surface = self.font.render(self.lines[i], True, self.outline_color, self.bg_color)
                for dx in range(-self.outline_width, self.outline_width + 1):
                    for dy in range(-self.outline_width, self.outline_width + 1):
                        screen.blit(outline_surface, (x + dx, y + dy + i * self.font_size))

            screen.blit(text_surface, (x, y + i * self.font_size))

        # Remove the clipping area to allow drawing on the entire screen again
        screen.set_clip(None)

