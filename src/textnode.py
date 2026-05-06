from enum import Enum

from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url = None):
        if not isinstance(text_type, TextType):
            raise Exception("text_type value is not a valid type")
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
    def text_node_to_html_node(self):
        match self.text_type:
            case self.text_type.TEXT:
                return LeafNode(None, self.text, None)
            case self.text_type.BOLD:
                return LeafNode("b", self.text, None)
            case self.text_type.ITALIC:
                return LeafNode("i", self.text, None)
            case self.text_type.CODE:
                return LeafNode("code", self.text, None)
            case self.text_type.LINK:
                return LeafNode("a", self.text, {"href": {self.url}})
            case self.text_type.IMAGE:
                return LeafNode("img", None, {"src": {self.url}, "alt": {self.text}})
            case _:
                raise Exception("invalid text type")