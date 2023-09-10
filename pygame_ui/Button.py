import pygame
import random
import string

class Button:
    def __init__(self, outer_panel, width=0, height=0, position=(0, 0),
                 button_image=None, button_hover_image=None, default_color=(255, 255, 255),
                 default_hover_color=(200, 200, 200), hover_color_transparency=0.5,
                 default_text="", shadow_transparency=0, shadow_offset=(0, 0),
                 is_visible=True, one_time_action=None, hold_action=None):
        
        self.Name = self.generate_unique_name()
        self.Outer_Panel = outer_panel
        self.Width = width
        self.Height = height
        self.Position = position
        self.Button_Image = button_image
        self.Button_Hover_Image = button_hover_image
        self.Default_Color = default_color
        self.Default_Hover_Color = default_hover_color
        self.Hover_Color_Transparency = hover_color_transparency
        self.Default_Text = default_text
        self.Shadow_Transparency = shadow_transparency
        self.Used_Shadow_Transparency = shadow_transparency
        self.Shadow_Offset = shadow_offset
        self.Is_Visible = is_visible
        self.hold_action = hold_action
        self.one_time_action = one_time_action
        self.Original_Color = default_color
        self.Is_Hovering = False
        self._clicked = False
        self.draw_order = 0

    def get_draw_order_value(self):
        return self.draw_order
    
    def set_draw_order_value(self, int):
        self.draw_order = int

    def set_width(self, width):
        """
        Set the width of the button.
        
        :param width: The new width of the button.
        """
        self.Width = width

    def set_height(self, height):
        """
        Set the height of the button.
        
        :param height: The new height of the button.
        """
        self.Height = height

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

    def find_screen(self):
        panel = self.Outer_Panel  # Start from the Outer_Panel of the current object
        while panel is not None:
            if panel.Screen is not None:
                return panel.Screen  # Return the screen once found
            panel = panel.Outer_Panel  # Move to the next Outer_Panel
        return None  # Return None if no screen is found

    def generate_unique_name(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name

    def draw(self):
        self.update()
        if not self.Is_Visible:
            return

        screen = self.find_screen()

        # Calculate the actual position and dimensions using Outer_Panel
        x, y = self.calculate_actual_position()
        ow, oh = self.Outer_Panel.calculate_width_and_height()
        width = self.Width * ow
        height = self.Height * oh

        # Set the clipping area to the dimensions of the Outer_Panel
        ox, oy = self.Outer_Panel.calculate_actual_position()
        screen.set_clip(pygame.Rect(ox, oy, ow, oh))

        # Create a new surface with the same dimensions as the rectangle you want to draw.
        shadow_surface = pygame.Surface((int(width), int(height)), pygame.SRCALPHA)

        # Fill the surface with the color and transparency you want.
        shadow_surface.fill((0, 0, 0, int(self.Used_Shadow_Transparency * 255)))  # Assuming self.Shadow_Transparency is between 0 and 1

        # Draw shadow
        shadow_x = x + self.Shadow_Offset[0]
        shadow_y = y + self.Shadow_Offset[1]
        screen.blit(shadow_surface, (shadow_x, shadow_y))

        # Draw the button
        if self.Button_Image:
            image = pygame.image.load(self.Button_Image)
            image = pygame.transform.scale(image, (int(width), int(height)))
            screen.blit(image, (int(x), int(y)))
        else:
            pygame.draw.rect(screen, self.Default_Color, (int(x), int(y), int(width), int(height)))

        # Draw text if any
        if self.Default_Text:
            font = pygame.font.SysFont(None, 36)
            text_surface = font.render(self.Default_Text, True, (0, 0, 0))
            screen.blit(text_surface, (int(x) + int(width) // 2 - text_surface.get_width() // 2, 
                                    int(y) + int(height) // 2 - text_surface.get_height() // 2))

        # Remove the clipping area to allow drawing on the entire screen again
        screen.set_clip(None)

    def hide_Button(self):
        self.Is_Visible = False

    def set_Action(self, action):
        self.Action = action

    def mouse_in_range(self):
        x, y = pygame.mouse.get_pos()
        button_x, button_y = self.calculate_actual_position()
        button_width, button_height = self.Outer_Panel.calculate_width_and_height()
        button_width *= self.Width
        button_height *= self.Height
        if button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height:
            self.Is_Hovering = True
            return True
        else:
            self.Is_Hovering = False
            return False

    def handle_event(self, event):
            if self.mouse_in_range():
                if event.type == pygame.MOUSEBUTTONDOWN and not self._clicked:
                    # Run the one-time action if the button is clicked
                    if self.one_time_action:
                        self.one_time_action()
                    self._clicked = True  # Set the flag to indicate that the button has been clicked

                elif event.type == pygame.MOUSEBUTTONUP:
                    self._clicked = False  # Reset the clicked flag when the mouse button is released

                elif event.type == pygame.MOUSEMOTION:
                    # Check if the mouse is still over the button (hovering)
                    if event.buttons[0]:  # Left mouse button is pressed
                        # Run the hold action if the button is being held down
                        if self.hold_action:
                            self.hold_action()

    def update(self):
        if self.mouse_in_range():
            self.Default_Color = self.Default_Hover_Color  # Change to the hover color
            self.Used_Shadow_Transparency = self.Shadow_Transparency + (1-self.Shadow_Transparency)/2
        else:
            self.Default_Color = self.Original_Color  # Change back to the original color
            self.Used_Shadow_Transparency = self.Shadow_Transparency