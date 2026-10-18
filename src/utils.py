import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    result = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        tokens = node.text.split(delimiter)
        if not len(tokens) in [1,3]:
            raise Exception("Invalid markdown syntax")

        result.append(TextNode(text=tokens[0], text_type=TextType.TEXT))

        if len(tokens) == 3:
            result.append(TextNode(text=tokens[1], text_type=text_type))
            result.append(TextNode(text=tokens[2], text_type=TextType.TEXT))

    return result

def extract_markdown_images(text:str):
    # ![rick roll](https://i.imgur.com/aKaOqIh.gif)
    return re.findall(r"!\[(.+?)\]\((.+?)\)", text)

def extract_markdown_links(text:str):
    # [to boot dev](https://www.boot.dev)
    return re.findall(r"\[(.+?)\]\((.+?)\)", text)