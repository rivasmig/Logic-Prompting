from .Panel import Panel
from .Button import Button
import pygame

class ScrollBar(Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_button = ScrollButton(outer_panel=self)
        self.Panel_Manager.add_button(self.scroll_button)
        self.scroll_button.adjust_size_and_position()

    def set_Height(self, height):  # Changed method name to match super class
        super().set_Height(height)
        self.scroll_button.adjust_size_and_position()
    
    def set_Width(self, width):  # Changed method name to match super class
        super().set_Width(width)
        self.scroll_button.adjust_size_and_position()

    def update_scroll_button_position(self, percentage):
        # Update the position of the scroll button based on the given percentage.
        max_scroll = self.Height - self.scroll_button.Height
        self.scroll_button.set_Position(0, percentage * max_scroll)

    def draw(self):
        super().draw()
        self.scroll_button.draw()


class ScrollButton(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def adjust_size_and_position(self):
        # Adjust the size and position based on the size of the parent ScrollBar
        if hasattr(self.Outer_Panel, 'Width') and hasattr(self.Outer_Panel, 'Height'):  # Handle potential AttributeError
            self.set_width(self.Outer_Panel.Width)
            self.set_height(max(20, self.Outer_Panel.Height * 0.1))  # Example height
            self.draw()  # Ensure the button is redrawn


class ScrollablePanel(Panel):
    def __init__(self, *args, content_height=1.0, scroll_speed=0.1, **kwargs):
        super().__init__(*args, **kwargs)
        self.ContentPanel = Panel(outer_panel=self, width=1, height=content_height, color=(255, 0, 0))
        self.ScrollBar = ScrollBar(outer_panel=self, width=0.05, height=1, position=(0.95, 0))
        self.Panel_Manager.add_panel(self.ContentPanel)
        self.Panel_Manager.add_panel(self.ScrollBar)
        self.scroll_percentage = 0  # Represents the current scroll position as a percentage
        self.scroll_speed = scroll_speed  # Customizable scroll speed

        # Edge Case: Check if the ContentPanel is smaller or equal to the ScrollablePanel
        self.check_content_height()

    def check_content_height(self):
        if self.ContentPanel.Height <= self.Height:
            self.ScrollBar.hide_Panel()

    def handle_event(self, event):
        super().Panel_Manager.handle_event(event)
        self.ContentPanel.Panel_Manager.handle_event(event)  # Propagate event to ContentPanel
        self.ScrollBar.Panel_Manager.handle_event(event)     # Propagate event to ScrollBar
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.scroll(-self.scroll_speed)
            elif event.button == 5:  # Scroll down
                self.scroll(self.scroll_speed)

    def scroll(self, percentage_delta):
        self.scroll_percentage = max(0, min(1, self.scroll_percentage + percentage_delta))
        
        # Edge Case: Check if the ContentPanel is smaller or equal to the ScrollablePanel
        self.check_content_height()  # Added this line
        
        self.ContentPanel.set_Position(0, -self.scroll_percentage * (self.ContentPanel.Height - self.Height))
        self.ScrollBar.update_scroll_button_position(self.scroll_percentage)
        self.redraw()  # Redraw the ScrollablePanel to update the visuals

    def set_scroll_speed(self, new_speed):
        self.scroll_speed = new_speed

    def get_scroll_speed(self):
        return self.scroll_speed

    def draw(self):
        # First, call the draw method of the base class to draw the panel itself
        super().draw()

        # Next, draw the content panel and all its contained elements
        self.ContentPanel.draw()

        # Lastly, draw the scrollbar and its button, ensuring it's on top
        self.ScrollBar.draw()