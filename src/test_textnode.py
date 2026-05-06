import unittest

from textnode import TextNode, TextType
from functions import split_node_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)
        
    def test_url_none(self):
        node = TextNode("Text node without URL", TextType.TEXT)
        self.assertIsNone(node.url)
        
    def test_class(self):
        node = TextNode("Text node", TextType.TEXT)
        self.assertIsInstance(node, TextNode)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_type(self):
        node = TextNode("Testing type", TextType.IMAGE)
        self.assertEqual(node.text_type.value, "image")

    def test_delimiter(self):
        nodes = [TextNode("`code` with plain text and **bold**", TextType.TEXT), TextNode("plain text with __italic text__", TextType.TEXT)]
        nodes = split_node_delimiter(nodes, "`", TextType.CODE)
        nodes = split_node_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_node_delimiter(nodes, "__", TextType.ITALIC)
        self.assertEqual(len(nodes), 8)
    
    def test_no_delimiter(self):
        node = [TextNode("text without delimiters", TextType.TEXT)]
        new_node = split_node_delimiter(node, "**", TextType.BOLD)
        self.assertEqual(new_node, node)


if __name__ == "__main__":
    unittest.main()