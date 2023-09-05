
class UI_Manager:
    def __init__(self):
        self.Panel_List = []
        self.Button_List = []
        self.Image_List = []
        self.Text_List = []
        self.Vertice_List = []
        
    def add_panel(self, panel):
        self.Panel_List.append(panel)
        
    def remove_panel(self, panel):
        self.Panel_List.remove(panel)
        
    def add_button(self, button):
        self.Button_List.append(button)
        
    def remove_button(self, button):
        self.Button_List.remove(button)
        
    def add_image(self, image):
        self.Image_List.append(image)
        
    def remove_image(self, image):
        self.Image_List.remove(image)
        
    def add_text(self, text):
        self.Text_List.append(text)
        
    def remove_text(self, text):
        self.Text_List.remove(text)
        
    def add_vertice(self, vertice):
        self.Vertice_List.append(vertice)
        
    def remove_vertice(self, vertice):
        self.Vertice_List.remove(vertice)
    
    def draw(self):
        # Draw panels
        for panel in self.Panel_List:
            panel.draw()

        # Update and draw buttons
        for button in self.Button_List:
            button.redraw()  # Calling redraw will update the button's state and draw it

        # Draw other UI elements
        for image in self.Image_List:
            image.draw()
        for text in self.Text_List:
            text.draw()
        for vertice in self.Vertice_List:
            vertice.draw()

    def handle_event(self, event):
        # Handling events for buttons
        for button in self.Button_List:
            button.handle_event(event)  # This will now just handle events, not draw the button

        # Handling events for panels (and their nested elements)
        for panel in self.Panel_List:
            if panel.Is_Visible:
                panel.Panel_Manager.handle_event(event)
