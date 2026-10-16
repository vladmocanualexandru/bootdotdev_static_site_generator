import unittest
from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
