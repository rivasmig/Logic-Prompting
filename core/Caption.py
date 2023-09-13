from draw_elements import point, element
from core import media
import json

class Caption:
    def __init__(self):
        self.total_caption_string = ""
        self.element_and_attribute_directory = {}
        self.decimalPlaces = 4

        # Dictionary of symbols
        self.symbols = {
            'element': '⟐',
            'position': 'χ',
            'text': 'τ',
            'x_position': 'x@',
            'y_position': 'y@',
            'separation': '|'
        }

    def generate_caption_from_elements(self, elements: list):
        self.element_and_attribute_directory.clear()
        for elem in elements:
            description = elem.getTextAttribute()
            position = None
            unique_key = elem.localName  # Using the localName as a unique key
            for i, attr in enumerate(elem.attributes):
                if attr == "Position":
                    position = elem.attributes[i+1]

            self.element_and_attribute_directory[unique_key] = {
                'description': description,
                'position': position
            }

        self.get_caption()

    def load_caption(self, caption_string):
        self.total_caption_string = caption_string
        elements = caption_string.split(self.symbols['element'])[1:-1]

        parsed_elements = []

        for elem in elements:
            description = elem.split(self.symbols['text'])[1].strip()
            position_str = elem.split(self.symbols['position'])[1] if self.symbols['position'] in elem else None
            position = (float(position_str.split(self.symbols['x_position'])[1].split(self.symbols['y_position'])[0]), 
                        float(position_str.split(self.symbols['y_position'])[1])) if position_str else None

            element_obj = point.Point()
            element_obj.add_text_attribute(description)
            if position:
                element_obj.add_pos_attribute(*position)

            parsed_elements.append(element_obj)

        return parsed_elements

    def get_caption(self):
        captions = []
        for key, value in self.element_and_attribute_directory.items():
            description = value.get('description')
            position = value.get('position')
            formatted_position = None
            if position:
                px, py = position
                px = round(px, self.decimalPlaces)
                py = round(py, self.decimalPlaces)
                formatted_position = self.symbols['position'] + \
                    self.symbols['x_position'] + str(px) + self.symbols['y_position'] + \
                    str(py) + self.symbols['position']

            element_caption = self.symbols['element']
            if description:
                element_caption += self.symbols['text'] + " " + description + " " + self.symbols['text']
            if formatted_position:
                element_caption += " " + formatted_position
            element_caption += " " + self.symbols['element']

            captions.append(element_caption)

        self.total_caption_string = self.symbols['separation'].join(captions)

        return self.total_caption_string
    
    def load_caption_from_logic(self, logic_file_path: str):
        # Open and read the logic file
        with open(logic_file_path, 'r') as file:
            logic_file_content = json.load(file)

        # Extract elements from the current media based on currentMediaIndex
        current_media_elements = logic_file_content['mediaSet'][logic_file_content['currentMediaIndex']]['elements']
        
        elements = []
        for elem_data in current_media_elements:
            element_obj = point.Point()
            for i, attr in enumerate(elem_data['attributes']):
                if attr == "Position":
                    element_obj.add_pos_attribute(*elem_data['attributes'][i+1])
                elif attr == "Text":
                    element_obj.add_text_attribute(elem_data['attributes'][i+1])
            elements.append(element_obj)
        
        # Generate the caption based on these elements
        self.generate_caption_from_elements(elements)
        return self.total_caption_string
    
    @staticmethod
    def generate_caption_from_media(media_obj: media.Media) -> str:
        # Create a Caption instance
        caption_instance = Caption()
        
        # Use the elements from the media object to generate the caption
        caption_instance.generate_caption_from_elements(media_obj.get_elements())
        
        # Return the generated caption
        return caption_instance.total_caption_string

