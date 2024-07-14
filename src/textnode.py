from htmlnode import LeafNode
from enum import Enum

class text_type_enum(Enum):
    type_text = "text"
    type_bold = "bold"
    type_italic = "italic"
    type_code = "code"
    type_link = "link"
    type_image = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, node):
        if self.text == node.text and self.text_type == node.text_type and self.url == node.url:
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case text_type_enum.type_text:
            return LeafNode(None, text_node.text,)
        case text_type_enum.type_bold:
            return LeafNode("b", text_node.text,)
        case text_type_enum.type_italic:
            return LeafNode("i", text_node.text,)
        case text_type_enum.type_code:
            return LeafNode("code", text_node.text,)
        case text_type_enum.type_link:
            return LeafNode("a", text_node.text, {"href": text_node.url,})
        case text_type_enum.type_image:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")