
class UI_Manager:
    def __init__(self):
        self.Panel_List = []
        self.Button_List = []
        self.Image_List = []
        self.Text_List = []
        self.Vertice_List = []
        self.Animation_List = []
        self.panel_draw_order_value = 0
        self.total_elements = 0
    
    def set_panel_draw_order_value(self, int):
        self.panel_draw_order_value = int

    def add_animation(self, animation, other_element):
        self.total_elements+=1
        animation.set_draw_order_value(other_element.get_draw_order_value()-1)
        self.Animation_List.append(animation)

    def remove_animation(self, animation):
        self.total_elements-=1
        self.Animation_List.remove(animation)

    def add_panel(self, panel):
        self.total_elements+=1
        v = panel.get_draw_order_value()
        panel.set_draw_order_value(v + self.total_elements + self.panel_draw_order_value)
        self.Panel_List.append(panel)
        
    def remove_panel(self, panel):
        self.Panel_List.remove(panel)
        self.total_elements -= 1
        
    def add_button(self, button):
        self.total_elements+=1
        v = button.get_draw_order_value()
        button.set_draw_order_value(v + self.total_elements + self.panel_draw_order_value)
        self.Button_List.append(button)
        
    def remove_button(self, button):
        self.Button_List.remove(button)
        self.total_elements -= 1
        
    def add_image(self, image):
        self.total_elements+=1
        v = image.get_draw_order_value()
        image.set_draw_order_value(v + self.total_elements + self.panel_draw_order_value)
        self.Image_List.append(image)
        
    def remove_image(self, image):
        self.Image_List.remove(image)
        self.total_elements -= 1
        
    def add_text(self, text):
        self.total_elements+=1
        v = text.get_draw_order_value()
        text.set_draw_order_value(v + self.total_elements + self.panel_draw_order_value)
        self.Text_List.append(text)
        
    def remove_text(self, text):
        self.Text_List.remove(text)
        self.total_elements -= 1
        
    def add_vertice(self, vertice):
        self.total_elements+=1
        v = vertice.get_draw_order_value()
        vertice.set_draw_order_value(v + self.total_elements + self.panel_draw_order_value)
        self.Vertice_List.append(vertice)
        
    def remove_vertice(self, vertice):
        self.Vertice_List.remove(vertice)
        self.total_elements -= 1
    
    def draw(self):
        all_elements = []
        
        # Add all the elements from the panel list, button list, image list, etc. into all_elements
        all_elements.extend(self.Panel_List)
        all_elements.extend(self.Button_List)
        all_elements.extend(self.Image_List)
        all_elements.extend(self.Text_List)
        all_elements.extend(self.Vertice_List)
        all_elements.extend(self.Animation_List)

        # Sort all_elements based on their get_draw_order_value()
        # In case of a tie, the order in the original list will decide the sequence
        all_elements.sort(key=lambda x: x.get_draw_order_value(), reverse=False)

        # Reassign draw_order_values to ensure they are unique and in sequence
        last_draw_order = 0
        for element in all_elements:
            current_draw_order = element.get_draw_order_value()
            if current_draw_order == last_draw_order:
                last_draw_order += 1
                element.set_draw_order_value(last_draw_order)
            else:
                last_draw_order = current_draw_order

        # Draw all elements in the desired order
        for element in all_elements:
            element.draw()

    def handle_event(self, event):
        # Handling events for buttons
        for button in self.Button_List:
            button.handle_event(event)  # This will now just handle events, not draw the button

        # Handling events for panels (and their nested elements)
        for panel in self.Panel_List:
            if panel.Is_Visible:
                panel.Panel_Manager.handle_event(event)
