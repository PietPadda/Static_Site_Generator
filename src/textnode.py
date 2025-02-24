from enum import Enum

class TextType(Enum):
    # Cover all types of text nodes
    NORMAL = "normal text"
    BOLD = "bold text"
    ITALIC = "italic text"
    CODE = "code text"
    LINKS = "Links"
    IMAGES = "images"


class TextNode:
    # url default=None in case not image/link
    def __init__(self, text, text_type, url=None):
        self.text = text  # text content of code
        self.text_type = text_type  # type of text, enum
        self.url = url  # url of link/image

    def __eq__(self, other):
        # checks if all properties of two TextNode objects are equal
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False
    
    
    def __repr__(self):
        # returns str representation of TextNode object w properties
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        # use .value to get name of value