import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_tag(self):
        node = HTMLNode(tag="a", value="link")
        node2 = HTMLNode(tag="div", children=[])
        node3 = HTMLNode(value="test", props={})
        self.assertEqual(node.tag, "a")
        self.assertNotEqual(node2.tag, "h1")
        self.assertIsNone(node3.children)
        
    def test_props(self):
        node = HTMLNode(props={"href": "www.google.es", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="www.google.es" target="_blank"')
        
    def test_repr(self):
        node = HTMLNode(tag="h1", value="title", children=[], props={'style': 'color:red;'})
        self.assertEqual(node.__repr__(), "HTMLNode(h1, title, [], {'style': 'color:red;'})")
        
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>") 
        
    def test_leaf_repr(self):
        node = LeafNode("h2", "subtitle", {"class": "bold"})
        self.assertEqual(node.__repr__(), "LeafNode(h2, subtitle, {'class': 'bold'})")
        
class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_multiple(self):
        gchild_node1 = LeafNode("h1", "title")
        gchild_node2 = LeafNode("i", "italic text")
        child_node1 = LeafNode("b", "Bold text")
        child_node2 = LeafNode(None, "Normal text")
        child_node3 =  ParentNode("div", [gchild_node1, gchild_node2], {"class": "container"})
        child_node4 = LeafNode(None, "Normal text")
        parent_node = ParentNode("p", [child_node1, child_node2, child_node3, child_node4])
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold text</b>Normal text<div><h1>title</h1><i>italic text</i></div>Normal text</p>"
        )

if __name__ == "__main__":
    unittest.main()