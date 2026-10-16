from enum import Enum

class TextType(Enum):
    PLAIN = "plain text"
    BOLD = "**bold**"
    ITALIC = "_italic_"
    CODE = "`code`"
    LINK = "[text](url)"
    IMAGE = "![alt](url)"

class TextNode:

    def __init__(self, text:str, text_type:TextType, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text, self.text_type, self.url) == (other.text, other.text_type, other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
