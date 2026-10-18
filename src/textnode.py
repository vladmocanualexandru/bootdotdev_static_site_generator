from enum import Enum

from leafnode import LeafNode

class TextType(Enum):
    TEXT = "plain text"
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

    
def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode(value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(value=text_node.text, tag="b")
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(value=text_node.text, tag="i")
    elif text_node.text_type == TextType.CODE:
        return LeafNode(value=text_node.text, tag="code")
    elif text_node.text_type == TextType.LINK:
        return LeafNode(value=text_node.text, tag="a", props={"href":text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", props={"alt":text_node.text, "src":text_node.url})
        