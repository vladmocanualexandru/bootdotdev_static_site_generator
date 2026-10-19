import re, os, shutil
from enum import Enum
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
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

class MissingTitleException(RuntimeError):
    def __init__(self):
        super().__init__("Markdown is missing a title")

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
            result.children.append(ParentNode(tag="ul", children=[text_node_to_html_node(text_node) for text_node in text_to_textnodes(block)]))
        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            for i in range(len(lines)):
                lines[i] = f"<li>{lines[i][(3 if i<9 else 4):]}</li>"

            block = "".join(lines)

            result.children.append(ParentNode(tag="ol", children=[text_node_to_html_node(text_node) for text_node in text_to_textnodes(block)]))

    return result

def extract_title(markdown:str) -> str:
    markdown = markdown.strip()

    if not markdown.startswith("# "):
        raise MissingTitleException()

    return markdown.split("\n",1)[0][2:].strip()

def copy_contents(source:str, destination:str):
    for filename in os.listdir(destination):
        file_path = os.path.join(destination, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                print(f'Deleting file {file_path}')
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                print(f'Deleting folder {file_path}')
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    for filename in os.listdir(source):
        source_file_path = os.path.join(source, filename)
        destination_file_path = os.path.join(destination, filename)
        try:
            if os.path.isfile(source_file_path) or os.path.islink(source_file_path):
                print(f'Copying file {source_file_path} to {destination}')
                shutil.copyfile(source_file_path, destination_file_path)
            elif os.path.isdir(source_file_path):
                print(f'Creating folder {destination_file_path}')
                os.makedirs(destination_file_path)

                copy_contents(source_file_path, destination_file_path)

        except Exception as e:
            print('Failed to create %s. Reason: %s' % (destination_file_path, e))


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}...")

    content = template = None

    with open(from_path, "r") as file:
        content = file.read()

    with open(template_path, "r") as file:
        template = file.read()

    if not content or not template:
        raise Exception("Unable to read content file and/or template")

    title = extract_title(content)
    content_html = markdown_to_html_node(content).to_html()

    page_html = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)

    with open(dest_path, "w") as file:
        file.write(page_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        source_file_path = os.path.join(dir_path_content, filename)

        try:
            if os.path.isfile(source_file_path) and source_file_path.endswith(".md"):
                destination_file_path = os.path.join(dest_dir_path, filename)[:-3]+".html"

                print(f'Using md file {source_file_path} to generate {destination_file_path}')

                generate_page(source_file_path, template_path, destination_file_path)
            elif os.path.isdir(source_file_path):
                print(f'Looking inside folder {source_file_path}')

                destination_file_path = os.path.join(dest_dir_path, filename)

                os.makedirs(destination_file_path)
                generate_pages_recursive(source_file_path, template_path, destination_file_path)

        except Exception as e:
            print('Failed to parse %s. Reason: %s' % (source_file_path, e))
