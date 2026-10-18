import re
from textnode import TextNode, TextType

class InvalidSyntaxException(RuntimeError):
    def __init__(self):
        super().__init__("Invalid markdown syntax")

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    result = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        tokens = node.text.split(delimiter)
        if len(tokens)%2==0:
            raise InvalidSyntaxException()

        is_special = False
        for token in tokens:
            result.append(TextNode(text=token, text_type=(TextType.TEXT if not is_special else text_type)))
            is_special = not is_special


    return result

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        temp_text = node.text
        image_tuples = extract_markdown_images(temp_text)

        for alt,src in image_tuples:
            tokens = temp_text.split(f"![{alt}]({src})", 1)

            if tokens[0]!="":
                result.append(TextNode(text=tokens[0], text_type=TextType.TEXT))

            result.append(TextNode(text=alt, url=src, text_type=TextType.IMAGE))

            temp_text = tokens[1]

        if temp_text!="":
            result.append(TextNode(text=temp_text, text_type=TextType.TEXT))

    return result


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        temp_text = node.text
        link_tuples= extract_markdown_links(temp_text)

        for text,url in link_tuples:
            tokens = temp_text.split(f"[{text}]({url})", 1)

            if tokens[0]!="":
                result.append(TextNode(text=tokens[0], text_type=TextType.TEXT))

            result.append(TextNode(text=text, url=url, text_type=TextType.LINK))

            temp_text = tokens[1]

        if temp_text!="":
            result.append(TextNode(text=temp_text, text_type=TextType.TEXT))

    return result

def extract_markdown_images(text:str):
    # ![rick roll](https://i.imgur.com/aKaOqIh.gif)
    return re.findall(r"!\[(.+?)\]\((.+?)\)", text)

def extract_markdown_links(text:str):
    # [to boot dev](https://www.boot.dev)
    return re.findall(r"\[(.+?)\]\((.+?)\)", text)

def text_to_textnodes(text):
    result = split_nodes_delimiter([TextNode(text)], "**", TextType.BOLD)
    result = split_nodes_delimiter(result, "_", TextType.ITALIC)
    result = split_nodes_delimiter(result, "`", TextType.CODE)
    result = split_nodes_image(result)
    result = split_nodes_link(result)

    return result
