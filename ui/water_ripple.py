import pygame
from . import ui_animation
import numpy as np

class water_ripple(ui_animation.ui_animation):
    def __init__(self, *args, outer_panel, reference, splash_size, amount_of_ripples=5, 
                 ripple_decay_length=20, this_ripple_num=0, splash_decay=0.9, **kwargs):
        super().__init__(*args, **kwargs)
        self.Outer_Panel = outer_panel
        self.reference = reference
        self.splash_size = splash_size
        self.ripple_decay_length = ripple_decay_length
        self.amount_of_ripples = amount_of_ripples
        self.this_ripple_num = this_ripple_num
        self.splash_decay = splash_decay
        self.Width = self.reference.Width
        self.Height = self.reference.Height
        self.Position = self.reference.Position
        self.timer = 1
        self.Is_Visible = True

    def sigmoid(self, x):
        return 1.0 / (1.0 + (0.1*np.exp(-(x - (self.ripple_decay_length/2)))))

    def find_screen(self):
        panel = self.Outer_Panel  # Start from the Outer_Panel of the current object
        while panel is not None:
            if panel.Screen is not None:
                return panel.Screen  # Return the screen once found
            panel = panel.Outer_Panel  # Move to the next Outer_Panel
        return None  # Return None if no screen is found

    def draw_blue_rect_water(self, screen, rect, increased, thickness, transparency):
        # Create a new transparent surface with per-pixel alpha channel
        new_rect = pygame.Rect(rect)  # Create a copy of the rect to avoid modifying the original rect
        new_rect.width *= increased
        new_rect.height *= increased

        # Adjust the new_rect's x and y properties to ensure its center aligns with the rect's center
        width_diff = new_rect.width - rect.width
        height_diff = new_rect.height - rect.height
        new_rect.x -= width_diff / 2
        new_rect.y -= height_diff / 2

        surface = pygame.Surface(new_rect.size, pygame.SRCALPHA)
        
        # Color values
        blue = (0, 100, 160, min(int(255 * transparency), 255))
        colorkey = (127, 33, 33)
        
        # Fill the surface with colorkey
        surface.fill(colorkey)

        # Draw the filled rectangle with blue color on the surface
        pygame.draw.rect(surface, blue, (0, 0, new_rect.width, new_rect.height))

        # Draw a smaller rectangle inside with the colorkey to cut out the inside
        pygame.draw.rect(surface, colorkey, (thickness, thickness, new_rect.width - 2 * thickness, new_rect.height - 2 * thickness))

        # Set the colorkey to make it transparent
        surface.set_colorkey(colorkey)

        # Blit the surface onto the main screen at the rectangle's position
        screen.blit(surface, new_rect.topleft)

    
    def calculate_width_and_height(self):
        width, height = self.Width, self.Height
        if self.Outer_Panel:
            ow, oh = self.Outer_Panel.calculate_width_and_height()
            width *= ow
            height *= oh
        return width, height

    def calculate_actual_position(self):
        x, y = self.Position
        ow, oh = self.Outer_Panel.calculate_width_and_height()
        ox, oy = self.Outer_Panel.calculate_actual_position()
        
        # Calculate the width and height of the button
        button_width = self.Width * ow
        button_height = self.Height * oh
        
        # Adjust the position so (0,0) represents the center of the panel
        x = ox + (ow - button_width) / 2 + x * ow
        y = oy + (oh - button_height) / 2 + y * oh
        
        return x, y
    
    def boarder_expand(self, screen):

        #behavior of ripple over time
        non_zero_self = max(self.timer, 0.001)
        inc = self.sigmoid(self.timer) + self.splash_size
        thk = max(((1/non_zero_self) * 5), 0.1)
        alpha = self.ripple_decay_length/max(self.timer*2, 0.1)
        x, y = self.calculate_actual_position()

        width, height = self.calculate_width_and_height() # if such a function exists
        this_rect = pygame.Rect(x, y, width, height)

        self.draw_blue_rect_water(screen=screen, rect=this_rect, 
                                  increased=inc, thickness=thk,
                                  transparency=alpha)
        
        #create new ripple
        if (self.timer == (self.ripple_decay_length / max(self.amount_of_ripples, 0.1))):
            wr = water_ripple(outer_panel=self.Outer_Panel, reference=self.reference, 
                          splash_size=(self.splash_size*self.splash_decay),
                          ripple_decay_length= (self.ripple_decay_length 
                                                - (self.ripple_decay_length / max(self.amount_of_ripples,0.1))), 
                          amount_of_ripples= self.amount_of_ripples - 1, this_ripple_num=self.this_ripple_num + 1, 
                          splash_decay= self.splash_decay*self.splash_decay)
            self.Outer_Panel.Panel_Manager.add_animation(wr, self.reference)

    def draw(self):
        super().draw()
        if not self.Is_Visible:
            return
        
        screen = self.find_screen()
        if screen is None:
            return
        
        #getting variables for making ripple
        x, y = self.calculate_actual_position()
        ow, oh = self.Outer_Panel.calculate_width_and_height()
        width = self.Width * ow
        height = self.Height * oh
        ox, oy = self.Outer_Panel.calculate_actual_position()
        screen.set_clip(pygame.Rect(ox, oy, ow, oh))

        self.boarder_expand(screen = screen)

        #pygame.draw.rect(screen, (100,130,30), (x, y, width, height))

        #end of ripple life
        if (self.timer < self.ripple_decay_length):
            self.timer += 1
        else:
            self.Is_Visible = False
            self.Outer_Panel.Panel_Manager.remove_animation(self)
        
        screen.set_clip(None)
