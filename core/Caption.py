# You might need the `emoji` library for emoji recognition. You can install it via pip: pip install emoji

class Caption:
    def __init__(self):
        # Initialize all class variables
        self.total_caption_string = ""
        self.element_and_attribute_directory = {}
        self.symbol_directory = {
            '⟐': 'element',
            'τ': 'text_description',
            'χ': 'position',
            'Δ': 'function_name',
            'λ': 'logic_head',
            #... add more symbols as needed
        }
    
    def load_caption(self, txt_path):
        """Load caption from a text file and populate element_and_attribute_directory."""
        
        # Read the file content
        with open(txt_path, 'r') as file:
            content = file.read()
            
            # Split elements based on '⟐' assuming elements are separated by '⟐'
            elements = content.split('⟐')
            
            # Parse each element and identify attributes
            for elem in elements:
                # For simplicity, considering that each element starts with a text description followed by a position
                text_description = elem.split('τ')[1]
                position = elem.split('χ')[1] if 'χ' in elem else None
                
                self.element_and_attribute_directory[text_description] = {
                    'description': text_description,
                    'position': position
                }

                # Check if any unrecognized symbol exists
                for symbol in elem:
                    if symbol not in self.symbol_directory:
                        raise ValueError(f"Unrecognized symbol: {symbol}")
                        
        self.total_caption_string = content
                        
    def clear_caption(self):
        """Clear the caption string and directory."""
        
        self.total_caption_string = ""
        self.element_and_attribute_directory.clear()
        
    def add_element(self, element_name):
        """Add an element to the directory."""
        
        self.element_and_attribute_directory[element_name] = {}
         
    def add_position_attribute(self, element_name, position):
        """Add a position attribute to an element in the directory."""
        
        if not isinstance(position, tuple) or len(position) != 2:
            raise ValueError("Position should be a tuple of (x, y).")
        
        formatted_position = f'x@{position[0]}y@{position[1]}'
        
        if element_name in self.element_and_attribute_directory:
            self.element_and_attribute_directory[element_name]['position'] = formatted_position
        else:
            raise ValueError(f"Element {element_name} does not exist in the directory.")

        
    def add_descriptive_attribute(self, element_name, description):
        """Add a description attribute to an element in the directory."""
        
        if element_name in self.element_and_attribute_directory:
            self.element_and_attribute_directory[element_name]['description'] = description
        else:
            raise ValueError(f"Element {element_name} does not exist in the directory.")
    
    def get_caption(self):
        """Generate the total caption string based on the element and attribute directory."""
        
        captions = []  # Create an empty list to hold individual captions

        # Assuming the caption follows the provided format
        for element, attributes in self.element_and_attribute_directory.items():
            description = attributes.get('description', "")
            position = attributes.get('position', "")

            # Create element caption based on what attributes are present
            element_caption = '⟐'
            if description:
                element_caption += f' τ {description} τ'
            if position:
                element_caption += f' χ{position}χ'
            element_caption += ' ⟐'
            
            captions.append(element_caption)

        # Combine individual captions and ensure no trailing "|"
        self.total_caption_string = '|'.join(captions)

        return self.total_caption_string

