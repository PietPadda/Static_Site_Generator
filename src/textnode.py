from enum import Enum

from htmlnode import LeafNode

class TextType(Enum):
    # Cover all types of text nodes
    TEXT = "normal text"
    BOLD = "bold text"
    ITALIC = "italic text"
    CODE = "code text"
    LINK = "Links"
    IMAGE = "images"


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

# It's a FUNCTION, not a method. define OUT of class
# convert textnode to htmlnodes, specifically leafnodes!
#note: LeafNode(self, tag, value, props=None)
#note: TextNode(self, text, text_type, url=None)
def text_node_to_html_node(text_node):  # note, no self, it's a FUNC, not METH!
    # texttype match:case block
    match text_node.text_type:
        # TEXT type case
        case TextType.TEXT:
            # no tag, raw text value
            return LeafNode(None, text_node.text)
        # BOLD type case
        case TextType.BOLD:
            # b tag, raw text value
            return LeafNode("b", text_node.text)
        # ITALIC type case
        case TextType.ITALIC:
            # i tag, raw text value
            return LeafNode("i", text_node.text)
        # CODE type case
        case TextType.CODE:
            # code tag, raw text value
            return LeafNode("code", text_node.text)
        # LINK type case
        case TextType.LINK:
            # a tag, anchor text, dict_prop = "href" url
            return LeafNode("a", text_node.text, {"href": text_node.url})
        # IMAGE type case
        case TextType.IMAGE:
            # ![alt text for image](url/of/image.jpg)
            # img tag, emtpy str text, dict_prop = "src" img url, "alt" text
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        # default case
        case _:  # if it gets a TextNode type that we don't have
            raise Exception("This is an invalid TextNode type!")
