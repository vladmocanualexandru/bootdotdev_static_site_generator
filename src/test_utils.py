import unittest
from utils import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

class TestUtils(unittest.TestCase):
    def test_split_nodes_delimiter_split_count(self):
        test_node = TextNode("this is **bold** text", TextType.TEXT)

        split_nodes = split_nodes_delimiter([test_node], "**", TextType.BOLD)
        self.assertEqual(len(split_nodes), 3)

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

        with self.assertRaises(Exception):
            split_nodes = split_nodes_delimiter([test_node], "**", TextType.BOLD)

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

    def test_split_nodes_delimiter_bold(self):
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

    # IMPLEMENT MORE TESTS
    
    def test_extract_markdown_links_count(self):        
        text = "Here is a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        image_tuples = extract_markdown_links(text)

        self.assertEqual(len(image_tuples), 2)
        self.assertEqual(len(image_tuples[0]), 2)
        self.assertEqual(len(image_tuples[1]), 2)

    # IMPLEMENT MORE TESTS
    

if __name__ == "__main__":
    unittest.main()
