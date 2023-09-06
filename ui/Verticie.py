import pygame
import random
import string

class Verticie:
    def __init__(self, outer_panel, placement_order, icon=None, default_color=(255, 0, 0), 
                 width=0.1, height=0.1, position=(0, 0), caption=None, maintain_aspect_ratio=True):
        
        # Basic attributes
        self.Outer_Panel = outer_panel
        self.Placement_Order = placement_order
        self.Icon = icon
        self.Default_Color = default_color
        self.Width = width
        self.Height = height
        self.width = width  # Width of the verticie, either image or circle
        self.height = height  # Height of the verticie, either image or circle
        self.maintain_aspect_ratio = maintain_aspect_ratio  # Whether to maintain aspect ratio when resizing
        self.Position = position
        self.Caption = caption  # This will be an instance of the Caption class in the future
        self.Maintain_Aspect_Ratio = maintain_aspect_ratio
        self.Next_Verticie = None  # For linked list feature
        self.draw_order = 0
        self.Name = "vert"
        # Load the icon if provided
        self.load_icon()

    def get_draw_order_value(self):
        return self.draw_order
    
    def set_draw_order_value(self, int):
        self.draw_order = int

    def load_icon(self):
        if self.Icon:
            self.Image = pygame.image.load(self.Icon)  # Load the image from the path
            if self.Maintain_Aspect_Ratio:
                # Resize logic here, maintaining aspect ratio
                pass
            else:
                # Resize logic here, stretching as needed
                pass
        else:
            self.Image = None  # No image, will draw a circle instead
    
    def set_outer_panel(self, panel):
        self.Outer_Panel = panel

    def get_outer_panel(self):
        return self.Outer_Panel

    def set_position(self, x, y):
        self.Position = (x, y)

    def get_position(self):
        return self.Position

    def set_icon(self, icon_path):
        self.Icon = icon_path
        self.load_icon()

    def __len__(self):
        count = 1
        current = self
        while current.Next_Verticie is not None:
            current = current.Next_Verticie
            count += 1
        return count
    
    def peek(self):
        current = self
        while current.Next_Verticie is not None:
            current = current.Next_Verticie
        return current

    def pop(self):
        if self.Next_Verticie is None:
            return None
        else:
            current = self
            while current.Next_Verticie.Next_Verticie is not None:
                current = current.Next_Verticie
            popped = current.Next_Verticie
            current.Next_Verticie = None
            return popped

    def push(self, verticie):
        last_verticie = self.peek()
        last_verticie.Next_Verticie = verticie

    def resize(self, scale_factor, maintain_aspect_ratio=None):
        if maintain_aspect_ratio is None:
            maintain_aspect_ratio = self.maintain_aspect_ratio
        
        new_width = self.width * scale_factor
        new_height = self.height * scale_factor
        
        if maintain_aspect_ratio:
            # When maintaining aspect ratio, new_width and new_height will be the same
            new_width = new_height = max(new_width, new_height)
        
        if self.Icon:  # If an image icon is present
            self.Icon = pygame.transform.scale(self.Icon, (int(new_width), int(new_height)))
        else:  # If no image icon, just a circle
            pass  # In the case of a circle, you'll likely adjust its radius in the rendering function
        
        self.width = new_width
        self.height = new_height

    def draw(self):
        screen = self.Outer_Panel.find_screen()
        x, y = self.Outer_Panel.calculate_actual_position()
        width, height = self.Outer_Panel.calculate_width_and_height()
        
        actual_x = int(x + self.Position[0] * width)
        actual_y = int(y + self.Position[1] * height)
        
        if self.Image:  # If an icon exists
            screen.blit(self.Image, (actual_x, actual_y))
        else:  # Draw default circle
            radius = int(self.Width * width / 2)  # Assuming Width and Height are the same for a circle
            pygame.draw.circle(screen, self.Default_Color, (actual_x, actual_y), radius)
