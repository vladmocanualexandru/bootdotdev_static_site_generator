import unittest
from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_instance_creation(self):
        node = ParentNode(tag="test", children=[])

    def test_to_html_no_children_no_props(self):
        node = ParentNode(tag="div", children=[])

        self.assertEqual('<div></div>', node.to_html())

    def test_to_html_no_children(self):
        node = ParentNode(tag="div", children=[], props={"style":"cursor:pointer"})

        self.assertEqual('<div style="cursor:pointer"></div>', node.to_html())

    def test_to_html_one_leaf(self):
        node = ParentNode(tag="div", children=[
            LeafNode(value="test")
        ], props={"style":"cursor:pointer"})

        self.assertEqual('<div style="cursor:pointer">test</div>', node.to_html())

    def test_to_html_mixed_leafs(self):
        node = ParentNode(tag="div", children=[
            LeafNode(value="test1"),
            LeafNode(value="test2", tag="b"),
            LeafNode(value="test3", tag="span", props={"style":"color:red"})
        ], props={"style":"cursor:pointer"})

        self.assertEqual('<div style="cursor:pointer">test1<b>test2</b><span style="color:red">test3</span></div>', node.to_html())
    
    def test_to_html_one_parent(self):
        node = ParentNode(tag="outer", children=[
            ParentNode(tag="inner", props={"style":"color:red"}, children=[
                LeafNode(value="test")
            ])
        ], props={"style":"cursor:pointer"})

        self.assertEqual('<outer style="cursor:pointer"><inner style="color:red">test</inner></outer>', node.to_html())
    
    def test_to_html_two_parents(self):
        node = ParentNode(tag="outer", children=[
            ParentNode(tag="inner1", props={"style":"color:red"}, children=[
                LeafNode(value="test1")
            ]),
            ParentNode(tag="inner2", props={"style":"color:blue"}, children=[
                LeafNode(value="test2")
            ])
        ], props={"style":"cursor:pointer"})

        self.assertEqual('<outer style="cursor:pointer"><inner1 style="color:red">test1</inner1><inner2 style="color:blue">test2</inner2></outer>', node.to_html())
    
    def test_to_html_mixed_parents(self):
        node = ParentNode(tag="outer", children=[
            ParentNode(tag="inner1", props={"style":"color:red"}, children=[
                LeafNode(value="test1")
            ]),
            LeafNode(value="test2", tag="span", props={"style":"color:blue"})
        ], props={"style":"cursor:pointer"})

        self.assertEqual('<outer style="cursor:pointer"><inner1 style="color:red">test1</inner1><span style="color:blue">test2</span></outer>', node.to_html())
    
    def test_to_html_two_levels(self):
        node = ParentNode(tag="outer", children=[
            ParentNode(tag="center", children=[
                ParentNode(tag="inner", children=[
                    LeafNode(value="test")
                ], props={"style":"color:blue"}, )
            ], props={"style":"color:green"}, )
        ], props={"style":"color:red"})

        self.assertEqual('<outer style="color:red"><center style="color:green"><inner style="color:blue">test</inner></center></outer>', node.to_html())

    def test_to_html_with_children(self):
        child_node = LeafNode(tag="span", value="child")
        parent_node = ParentNode(tag="div", children=[child_node])

        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode(tag="b", value="grandchild")
        child_node = ParentNode(tag="span", children=[grandchild_node])
        parent_node = ParentNode(tag="div", children=[child_node])
        
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()
