import unittest
from utils import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, InvalidSyntaxException, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type, BlockType
from textnode import TextNode, TextType

class TestUtils(unittest.TestCase):
    def test_split_nodes_delimiter_split_count(self):
        test_node = TextNode("this is **bold** text", TextType.TEXT)

        split_nodes = split_nodes_delimiter([test_node], "**", TextType.BOLD)
        self.assertEqual(len(split_nodes), 3)

    def test_split_nodes_delimiter_split_two_bolds(self):
        test_node = TextNode("text1 **bold1** text2 **bold2** text3", TextType.TEXT)

        split_nodes = split_nodes_delimiter([test_node], "**", TextType.BOLD)

        self.assertEqual(len(split_nodes), 5)
        self.assertEqual(split_nodes[0], TextNode(text="text1 ", text_type=TextType.TEXT))
        self.assertEqual(split_nodes[1], TextNode(text="bold1", text_type=TextType.BOLD))
        self.assertEqual(split_nodes[2], TextNode(text=" text2 ", text_type=TextType.TEXT))
        self.assertEqual(split_nodes[3], TextNode(text="bold2", text_type=TextType.BOLD))
        self.assertEqual(split_nodes[4], TextNode(text=" text3", text_type=TextType.TEXT))

    def test_split_nodes_delimiter_split_two_nodes(self):
        test_node = TextNode("a**b**c", TextType.TEXT)

        split_nodes = split_nodes_delimiter([test_node, test_node], "**", TextType.BOLD)
        self.assertEqual(len(split_nodes), 6)

        self.assertEqual(split_nodes[0], TextNode(text="a", text_type=TextType.TEXT))
        self.assertEqual(split_nodes[1], TextNode(text="b", text_type=TextType.BOLD))
        self.assertEqual(split_nodes[2], TextNode(text="c", text_type=TextType.TEXT))
        self.assertEqual(split_nodes[3], TextNode(text="a", text_type=TextType.TEXT))
        self.assertEqual(split_nodes[4], TextNode(text="b", text_type=TextType.BOLD))
        self.assertEqual(split_nodes[5], TextNode(text="c", text_type=TextType.TEXT))

    def test_split_nodes_delimiter_invalid_syntax_raise(self):
        test_node = TextNode("this is broken **bold text", TextType.TEXT)

        with self.assertRaises(InvalidSyntaxException):
            split_nodes_delimiter([test_node], "**", TextType.BOLD)

    def test_split_nodes_delimiter_non_text(self):
        test_node = TextNode("this is a bold text", TextType.BOLD)

        split_nodes = split_nodes_delimiter([test_node], "**", TextType.BOLD)
        self.assertEqual(split_nodes[0], test_node)

    def test_split_nodes_delimiter_no_match(self):
        test_node = TextNode("this is a bold text", TextType.TEXT)

        split_nodes = split_nodes_delimiter([test_node], "**", TextType.BOLD)
        self.assertEqual(len(split_nodes), 1)
        self.assertEqual(split_nodes[0], test_node)

    def test_split_nodes_delimiter_bold(self):
        test_node = TextNode("a**b**c", TextType.TEXT)

        split_nodes = split_nodes_delimiter([test_node], "**", TextType.BOLD)
        self.assertEqual(split_nodes[0], TextNode(text="a", text_type=TextType.TEXT))
        self.assertEqual(split_nodes[1], TextNode(text="b", text_type=TextType.BOLD))
        self.assertEqual(split_nodes[2], TextNode(text="c", text_type=TextType.TEXT))

    def test_split_nodes_delimiter_italic(self):
        test_node = TextNode("a_b_c", TextType.TEXT)

        split_nodes = split_nodes_delimiter([test_node], "_", TextType.ITALIC)
        self.assertEqual(split_nodes[0], TextNode(text="a", text_type=TextType.TEXT))
        self.assertEqual(split_nodes[1], TextNode(text="b", text_type=TextType.ITALIC))
        self.assertEqual(split_nodes[2], TextNode(text="c", text_type=TextType.TEXT))

    def test_split_nodes_delimiter_code(self):
        test_node = TextNode("a`b`c", TextType.TEXT)

        split_nodes = split_nodes_delimiter([test_node], "`", TextType.CODE)
        self.assertEqual(split_nodes[0], TextNode(text="a", text_type=TextType.TEXT))
        self.assertEqual(split_nodes[1], TextNode(text="b", text_type=TextType.CODE))
        self.assertEqual(split_nodes[2], TextNode(text="c", text_type=TextType.TEXT))

    def test_extract_markdown_images_count(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        image_tuples = extract_markdown_images(text)

        self.assertEqual(len(image_tuples), 2)
        self.assertEqual(len(image_tuples[0]), 2)
        self.assertEqual(len(image_tuples[1]), 2)

    def test_extract_markdown_images_content(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        image_tuples = extract_markdown_images(text)

        self.assertEqual(image_tuples[0][0], "rick roll")
        self.assertEqual(image_tuples[0][1], "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(image_tuples[1][0], "obi wan")
        self.assertEqual(image_tuples[1][1], "https://i.imgur.com/fJRm4Vk.jpeg")

    def test_extract_markdown_links_count(self):
        text = "Here is a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        link_tuples = extract_markdown_links(text)

        self.assertEqual(len(link_tuples), 2)
        self.assertEqual(len(link_tuples[0]), 2)
        self.assertEqual(len(link_tuples[1]), 2)

    def test_extract_markdown_links_content(self):
        text = "Here is a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        link_tuples = extract_markdown_links(text)

        self.assertEqual(link_tuples[0][0], "to boot dev")
        self.assertEqual(link_tuples[0][1], "https://www.boot.dev")
        self.assertEqual(link_tuples[1][0], "to youtube")
        self.assertEqual(link_tuples[1][1], "https://www.youtube.com/@bootdotdev")

    def test_split_nodes_image_count(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        nodes = split_nodes_image([TextNode(text=text, text_type=TextType.TEXT)])

        self.assertEqual(len(nodes), 2)

    def test_split_nodes_image_no_image(self):
        text = "This is text without an image"
        nodes = split_nodes_image([TextNode(text=text, text_type=TextType.TEXT)])

        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0], TextNode(text=text, text_type=TextType.TEXT))

    def test_split_nodes_image_just_one_image(self):
        text = "![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        nodes = split_nodes_image([TextNode(text=text, text_type=TextType.TEXT)])

        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0], TextNode(text="rick roll", text_type=TextType.IMAGE, url="https://i.imgur.com/aKaOqIh.gif"))

    def test_split_nodes_image_one_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif). Cool!"
        nodes = split_nodes_image([TextNode(text=text, text_type=TextType.TEXT)])

        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0], TextNode(text="This is text with a ", text_type=TextType.TEXT))
        self.assertEqual(nodes[1], TextNode(text="rick roll", text_type=TextType.IMAGE, url="https://i.imgur.com/aKaOqIh.gif"))
        self.assertEqual(nodes[2], TextNode(text=". Cool!", text_type=TextType.TEXT))

    def test_split_nodes_image_just_two_images(self):
        text = "![rick roll](https://i.imgur.com/aKaOqIh.gif)![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        nodes = split_nodes_image([TextNode(text=text, text_type=TextType.TEXT)])

        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0], TextNode(text="rick roll", text_type=TextType.IMAGE, url="https://i.imgur.com/aKaOqIh.gif"))
        self.assertEqual(nodes[1], TextNode(text="obi wan", text_type=TextType.IMAGE, url="https://i.imgur.com/fJRm4Vk.jpeg"))

    def test_split_nodes_image_two_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg). Cool!"
        nodes = split_nodes_image([TextNode(text=text, text_type=TextType.TEXT)])

        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0], TextNode(text="This is text with a ", text_type=TextType.TEXT))
        self.assertEqual(nodes[1], TextNode(text="rick roll", text_type=TextType.IMAGE, url="https://i.imgur.com/aKaOqIh.gif"))
        self.assertEqual(nodes[2], TextNode(text=" and ", text_type=TextType.TEXT))
        self.assertEqual(nodes[3], TextNode(text="obi wan", text_type=TextType.IMAGE, url="https://i.imgur.com/fJRm4Vk.jpeg"))
        self.assertEqual(nodes[4], TextNode(text=". Cool!", text_type=TextType.TEXT))

    def test_split_nodes_link_count(self):
        text = "Here is a link [to boot dev](https://www.boot.dev)"
        nodes = split_nodes_link([TextNode(text=text, text_type=TextType.TEXT)])

        self.assertEqual(len(nodes), 2)

    def test_split_nodes_link_no_link(self):
        text = "This is text without a link"
        nodes = split_nodes_link([TextNode(text=text, text_type=TextType.TEXT)])
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0], TextNode(text=text, text_type=TextType.TEXT))

    def test_split_nodes_link_just_one_link(self):
        text = "[to boot dev](https://www.boot.dev)"
        nodes = split_nodes_link([TextNode(text=text, text_type=TextType.TEXT)])

        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0], TextNode(text="to boot dev", text_type=TextType.LINK, url="https://www.boot.dev"))


    def test_split_nodes_link_one_link(self):
        text = "Here is a link [to boot dev](https://www.boot.dev). Neat!"
        nodes = split_nodes_link([TextNode(text=text, text_type=TextType.TEXT)])

        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0], TextNode(text="Here is a link ", text_type=TextType.TEXT))
        self.assertEqual(nodes[1], TextNode(text="to boot dev", text_type=TextType.LINK, url="https://www.boot.dev"))
        self.assertEqual(nodes[2], TextNode(text=". Neat!", text_type=TextType.TEXT))


    def test_split_nodes_link_just_two_images(self):
        text = "[to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)"
        nodes = split_nodes_link([TextNode(text=text, text_type=TextType.TEXT)])

        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0], TextNode(text="to boot dev", text_type=TextType.LINK, url="https://www.boot.dev"))
        self.assertEqual(nodes[1], TextNode(text="to youtube", text_type=TextType.LINK, url="https://www.youtube.com/@bootdotdev"))

    def test_split_nodes_link_two_images(self):
        text = "Here is a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev). Neat!"
        nodes = split_nodes_link([TextNode(text=text, text_type=TextType.TEXT)])

        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0], TextNode(text="Here is a link ", text_type=TextType.TEXT))
        self.assertEqual(nodes[1], TextNode(text="to boot dev", text_type=TextType.LINK, url="https://www.boot.dev"))
        self.assertEqual(nodes[2], TextNode(text=" and ", text_type=TextType.TEXT))
        self.assertEqual(nodes[3], TextNode(text="to youtube", text_type=TextType.LINK, url="https://www.youtube.com/@bootdotdev"))
        self.assertEqual(nodes[4], TextNode(text=". Neat!", text_type=TextType.TEXT))

    def test_text_to_textnodes_nothing(self):
        text = "This is a simple text"
        nodes = text_to_textnodes(text)

        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0], TextNode(text=text, text_type=TextType.TEXT))

    def test_text_to_textnodes_bold_single(self):
        text = "text1 **bold** text2"
        nodes = text_to_textnodes(text)

        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0], TextNode(text="text1 ", text_type=TextType.TEXT))
        self.assertEqual(nodes[1], TextNode(text="bold", text_type=TextType.BOLD))
        self.assertEqual(nodes[2], TextNode(text=" text2", text_type=TextType.TEXT))

    def test_text_to_textnodes_bold_same_simple(self):
        text = "text1 **bold1** text2 **bold2** text3"
        nodes = text_to_textnodes(text)

        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0], TextNode(text="text1 ", text_type=TextType.TEXT))
        self.assertEqual(nodes[1], TextNode(text="bold1", text_type=TextType.BOLD))
        self.assertEqual(nodes[2], TextNode(text=" text2 ", text_type=TextType.TEXT))
        self.assertEqual(nodes[3], TextNode(text="bold2", text_type=TextType.BOLD))
        self.assertEqual(nodes[4], TextNode(text=" text3", text_type=TextType.TEXT))

    def test_text_to_textnodes_mixed_simple(self):
        text = "text1 **bold** text2 _italic_ text3 `code` text4"
        nodes = text_to_textnodes(text)

        self.assertEqual(len(nodes), 7)
        self.assertEqual(nodes[0], TextNode(text="text1 ", text_type=TextType.TEXT))
        self.assertEqual(nodes[1], TextNode(text="bold", text_type=TextType.BOLD))
        self.assertEqual(nodes[2], TextNode(text=" text2 ", text_type=TextType.TEXT))
        self.assertEqual(nodes[3], TextNode(text="italic", text_type=TextType.ITALIC))
        self.assertEqual(nodes[4], TextNode(text=" text3 ", text_type=TextType.TEXT))
        self.assertEqual(nodes[5], TextNode(text="code", text_type=TextType.CODE))
        self.assertEqual(nodes[6], TextNode(text=" text4", text_type=TextType.TEXT))

    def test_text_to_textnodes_single_image(self):
        text = "text1 ![alt](src) text2"
        nodes = text_to_textnodes(text)

        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0], TextNode(text="text1 ", text_type=TextType.TEXT))
        self.assertEqual(nodes[1], TextNode(text="alt", url="src", text_type=TextType.IMAGE))
        self.assertEqual(nodes[2], TextNode(text=" text2", text_type=TextType.TEXT))

    def test_text_to_textnodes_same_images(self):
        text = "text1 ![alt1](src1) text2 ![alt2](src2) text3"
        nodes = text_to_textnodes(text)

        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0], TextNode(text="text1 ", text_type=TextType.TEXT))
        self.assertEqual(nodes[1], TextNode(text="alt1", url="src1", text_type=TextType.IMAGE))
        self.assertEqual(nodes[2], TextNode(text=" text2 ", text_type=TextType.TEXT))
        self.assertEqual(nodes[3], TextNode(text="alt2", url="src2", text_type=TextType.IMAGE))
        self.assertEqual(nodes[4], TextNode(text=" text3", text_type=TextType.TEXT))

    def test_text_to_textnodes_mixed_images_links(self):
        text = "text1 ![alt1](src1) text2 [label1](url1) text3 ![alt2](src2) text4 [label2](url2) text5"
        nodes = text_to_textnodes(text)

        self.assertEqual(len(nodes), 9)
        self.assertEqual(nodes[0], TextNode(text="text1 ", text_type=TextType.TEXT))
        self.assertEqual(nodes[1], TextNode(text="alt1", url="src1", text_type=TextType.IMAGE))
        self.assertEqual(nodes[2], TextNode(text=" text2 ", text_type=TextType.TEXT))
        self.assertEqual(nodes[3], TextNode(text="label1", url="url1", text_type=TextType.LINK))
        self.assertEqual(nodes[4], TextNode(text=" text3 ", text_type=TextType.TEXT))
        self.assertEqual(nodes[5], TextNode(text="alt2", url="src2", text_type=TextType.IMAGE))
        self.assertEqual(nodes[6], TextNode(text=" text4 ", text_type=TextType.TEXT))
        self.assertEqual(nodes[7], TextNode(text="label2", url="url2", text_type=TextType.LINK))
        self.assertEqual(nodes[8], TextNode(text=" text5", text_type=TextType.TEXT))

    def test_text_to_textnodes_mixed(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)

        self.assertEqual(len(nodes), 10)
        self.assertEqual(nodes[0], TextNode(text="This is ", text_type=TextType.TEXT))
        self.assertEqual(nodes[1], TextNode(text="text", text_type=TextType.BOLD))
        self.assertEqual(nodes[2], TextNode(text=" with an ", text_type=TextType.TEXT))
        self.assertEqual(nodes[3], TextNode(text="italic", text_type=TextType.ITALIC))
        self.assertEqual(nodes[4], TextNode(text=" word and a ", text_type=TextType.TEXT))
        self.assertEqual(nodes[5], TextNode(text="code block", text_type=TextType.CODE))
        self.assertEqual(nodes[6], TextNode(text=" and an ", text_type=TextType.TEXT))
        self.assertEqual(nodes[7], TextNode(text="obi wan image", text_type=TextType.IMAGE, url="https://i.imgur.com/fJRm4Vk.jpeg"))
        self.assertEqual(nodes[8], TextNode(text=" and a ", text_type=TextType.TEXT))
        self.assertEqual(nodes[9], TextNode(text="link", text_type=TextType.LINK, url="https://boot.dev"))

    def test_markdown_to_blocks_example(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_one_block(self):
        text="""# This is a heading
        """

        blocks = markdown_to_blocks(text)

        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0], "# This is a heading")

    def test_markdown_to_blocks_one_block_many_lines(self):
        text="""# This is a heading
Still in the same block
Still there
        """

        blocks = markdown_to_blocks(text)

        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0], "# This is a heading\nStill in the same block\nStill there")

    def test_markdown_to_blocks_count(self):
        text="""# This is a heading

        This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

        - This is the first list item in a list block
        - This is a list item
        - This is another list item
        """

        blocks = markdown_to_blocks(text)

        self.assertEqual(len(blocks), 3)

    def test_block_to_block_type_paragraph(self):
        text="This is a simple text"

        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_block_to_block_type_heading(self):
        text="# This is a heading"

        self.assertEqual(block_to_block_type(text), BlockType.HEADING)

    def test_block_to_block_type_not_heading(self):
        text="not # This is not a heading"

        self.assertNotEqual(block_to_block_type(text), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        text="""
```
This is a block of code
```
"""
        self.assertEqual(block_to_block_type(text), BlockType.CODE)

    def test_block_to_block_type_not_code(self):
        text="""
``
This is a not a block of code
```
"""
        self.assertNotEqual(block_to_block_type(text), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        text="""
>Quote line 1
>Quote line 2
>Quote line 3
"""
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)

    def test_block_to_block_type_not_quote(self):
        text="""
>Quote line 1
Quote line 2
>Quote line 3
"""
        self.assertNotEqual(block_to_block_type(text), BlockType.QUOTE)

    def test_block_to_block_type_ul(self):
        text="""
- Unordered item
- Another one
- And another one
"""
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_not_ul(self):
        text="""
- Unordered item
-Another one - LIST BREAKING ITEM
- And another one
"""
        self.assertNotEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ol(self):
        text="""
1. First
2. Second
3. Third
"""
        self.assertEqual(block_to_block_type(text), BlockType.ORDERED_LIST)

    def test_block_to_block_type_not_ol(self):
        text="""
1. First
2. Second
3 Third - LIST BREAKING ITEM
"""
        self.assertNotEqual(block_to_block_type(text), BlockType.ORDERED_LIST)

if __name__ == "__main__":
    unittest.main()
