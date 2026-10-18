import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq_nourl(self):
        node = TextNode("Text", TextType.BOLD)
        node2 = TextNode("Text", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("Text", TextType.IMAGE, "same image source url")
        node2 = TextNode("Text", TextType.IMAGE, "same image source url")
        self.assertEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("Text", TextType.BOLD)
        node2 = TextNode("DIFFERENT Text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_type(self):
        node = TextNode("Text", TextType.CODE)
        node2 = TextNode("Text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_url(self):
        node = TextNode("Text", TextType.LINK, "url1")
        node2 = TextNode("Text", TextType.LINK, "url2")
        self.assertNotEqual(node, node2)

    def test_to_html_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_to_html_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>This is a bold text node</b>")
    
    def test_to_html_italic(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<i>This is a italic text node</i>")

    def test_to_html_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<code>This is a code text node</code>")

    def test_to_html_link(self):
        node = TextNode("This is a link text node", TextType.LINK, url="www.test.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<a href="www.test.com">This is a link text node</a>')

    def test_to_html_code(self):
        node = TextNode("This is an image text node", TextType.IMAGE, url="www.test.com/img.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<img alt="This is an image text node" src="www.test.com/img.png"></img>')

if __name__ == "__main__":
    unittest.main()
