import re
from enum import Enum
from src.htmlnode import HTMLNode
from src.leafnode import LeafNode
from src.parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "PARAGRAPH"
    HEADING = "HEADING"
    CODE = "CODE"
    QUOTE = "QUOTE"
    UNORDERED_LIST = "UNORDERED_LIST"
    ORDERED_LIST = "ORDERED_LIST"

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

def markdown_to_blocks(markdown:str):
    lines = markdown.split("\n\n")

    return [line.strip() for line in lines if line.strip()!=""]

def block_to_block_type(markdown:str) -> BlockType:
    stripped_markdown = markdown.strip()

    if stripped_markdown.startswith("#"):
        return BlockType.HEADING
    elif stripped_markdown.startswith("```\n") and stripped_markdown.endswith("\n```"):
        return BlockType.CODE
    else:
        lines = stripped_markdown.split("\n")

        is_quote = is_ul = is_ol = True
        for i in range(len(lines)):
            line = lines[i]
            if not line.startswith(">"):
                is_quote = False
            if not line.startswith("- "):
                is_ul = False
            if not line.startswith(f"{i+1}. "):
                is_ol = False

        if is_quote:
            return BlockType.QUOTE
        if is_ul:
            return BlockType.UNORDERED_LIST
        if is_ol:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown:str) -> HTMLNode:
    result = ParentNode(children=[], tag="div")

    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            result.children.append(ParentNode(tag="p", children=[text_node_to_html_node(text_node) for text_node in text_to_textnodes(block)]))
        elif block_type == BlockType.HEADING:
            heading_rank = block.index("# ")
            block = block[heading_rank+2:]
            result.children.append(ParentNode(tag=f"h{heading_rank+1}", children=[text_node_to_html_node(text_node) for text_node in text_to_textnodes(block)]))
        elif block_type == BlockType.CODE:
            block = block.replace("```\n", "").replace("\n```", "")
            result.children.append(ParentNode(tag="pre", children=[LeafNode(tag="code", value=block)]))
        elif block_type == BlockType.QUOTE:
            block = "\n".join([line[2:] for line in block.split("\n")])
            result.children.append(LeafNode(tag="blockquote", value=block))
        elif block_type == BlockType.UNORDERED_LIST:
            block = "".join([f"<li>{line[2:]}</li>" for line in block.split("\n")])
            result.children.append(LeafNode(tag="ul", value=block))
        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            for i in range(len(lines)):
                lines[i] = f"<li>{lines[i][(3 if i<9 else 4):]}</li>"

            result.children.append(LeafNode(tag="ol", value="".join(lines)))

    return result
