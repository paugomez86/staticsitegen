from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class BlockType(Enum):
    P = "paragraph"
    H = "heading"
    CODE = "code"
    BLOCKQUOTE = "quote"
    UL = "unordered_list"
    OL = "ordered_list"