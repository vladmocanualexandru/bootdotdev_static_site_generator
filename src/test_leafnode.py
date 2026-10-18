import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_instance_creation(self):
        node = LeafNode("test")

    def test_to_html_no_tag(self):
        node = LeafNode("test")

        self.assertEqual("test", node.to_html())

    def test_to_html_tag_no_props(self):
        node = LeafNode(tag="span", value="test")

        self.assertEqual("<span>test</span>", node.to_html())

    def test_to_html_tag_with_props(self):
        node = LeafNode(tag="span", value="test", props={"style":"color:red"})

        self.assertEqual('<span style="color:red">test</span>', node.to_html())


if __name__ == "__main__":
    unittest.main()
