import unittest
from htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html_none(self):
        node = HTMLNode()

        props_str = node.props_to_html()

        self.assertEqual("", props_str)

    def test_props_to_html_empty_dict(self):
        node = HTMLNode(props={})

        props_str = node.props_to_html()

        self.assertEqual("", props_str)

    def test_props_to_html_not_one_prop(self):
        node = HTMLNode(props={"a":1})

        props_str = node.props_to_html()

        self.assertEqual(' a="1"', props_str)

    def test_props_to_html_not_many_props(self):
        node = HTMLNode(props={"a":1, "b":2, "c":3})

        props_str = node.props_to_html()

        self.assertEqual(' a="1" b="2" c="3"', props_str)

if __name__ == "__main__":
    unittest.main()
