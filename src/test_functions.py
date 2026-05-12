import unittest

from textnode import TextNode
from functions import split_node_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_text_nodes, markdown_to_blocks, block_to_block_type, markdown_to_html_node
from type_enums import TextType, BlockType

class TestFunctionsDelimiters(unittest.TestCase):
    def test_delimiter(self):
        nodes = [TextNode("`code` with plain text and **bold**", TextType.TEXT), TextNode("plain text with _italic text_", TextType.TEXT)]
        nodes = split_node_delimiter(nodes, "`", TextType.CODE)
        nodes = split_node_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_node_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(len(nodes), 5)
    
    def test_no_delimiter(self):
        node = [TextNode("text without delimiters", TextType.TEXT)]
        new_node = split_node_delimiter(node, "**", TextType.BOLD)
        self.assertEqual(new_node, node)


class TestFunctionsImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)\n" + 
            "This is text with ![another image](https://i.imgur.com/zjjcJKZ.png)\n" +
            "This is text with ![random characters...---](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([
            ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ("another image", "https://i.imgur.com/zjjcJKZ.png"),
            ("random characters...---", "https://i.imgur.com/zjjcJKZ.png")
        ], matches)
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
class TestFunctionsLinks(unittest.TestCase):        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an anchor: [Download here](https://i.imgur.com/zjjcJKZ.png)\n" +
            "Another anchor: [Download here](https://i.imgur.com/zjjcJKZ.png)\n" +
            "[Download here](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([
            ("Download here", "https://i.imgur.com/zjjcJKZ.png"),
            ("Download here", "https://i.imgur.com/zjjcJKZ.png"),
            ("Download here", "https://i.imgur.com/zjjcJKZ.png")
        ], matches)

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link!!](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link!!", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

class TestFunctionsTextToNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = ("Long text with all kinds of characters!! Does it work? It has **bold** and _italic_. " +
        "There is some `code blocks here` and `there`. More **bold text**, a [link](boot.dev) and an ![image](/images/image.png)" +
        "![Another image alt text](/images/image.png) with more _italic text_. And some `extra code`")
        
        nodes = text_to_text_nodes(text)
        
        self.assertListEqual(
            [
                TextNode("Long text with all kinds of characters!! Does it work? It has ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(". There is some ", TextType.TEXT),
                TextNode("code blocks here", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("there", TextType.CODE),
                TextNode(". More ", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
                TextNode(", a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "boot.dev"),
                TextNode(" and an ", TextType.TEXT) ,
                TextNode("image", TextType.IMAGE, "/images/image.png"),
                TextNode("Another image alt text", TextType.IMAGE, "/images/image.png"),
                TextNode(" with more ", TextType.TEXT),
                TextNode("italic text", TextType.ITALIC),
                TextNode(". And some ", TextType.TEXT),
                TextNode("extra code", TextType.CODE),
            ],
            nodes
        )
        
        
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph\n\n

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
        
    
    def test_block_to_type(self):
        h = "### This is a heading"
        p = "This is a paragraph of text. It has some **bold** and _italic_ words inside of it."
        ul = "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        ol = "1. ordered item\n2. another item\n3. another"
        quote = ">Quote"
        code = "```\ncode block```"
        quote2 = "> Another quote"

        tests = {
            h: BlockType.H,
            p: BlockType.P,
            ul: BlockType.UL,
            ol: BlockType.OL,
            quote: BlockType.BLOCKQUOTE,
            code: BlockType.CODE,
            quote2: BlockType.BLOCKQUOTE
        }
        
        for test, result in tests.items():
            self.assertEqual(block_to_block_type(test), result)

class TestFunctionsMarkdownToNodes(unittest.TestCase):
    def test_paragraphs(self):
        md = """This is **bolded** paragraph\ntext in a p\ntag here\n\nThis is another paragraph with _italic_ text and `code` here"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
        
    def test_links(self):
        md = "Text with [link](www.url.com) and ![image](image.png)"
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>Text with <a href="www.url.com">link</a> and <img src="image.png" alt="image"></p></div>',
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_ul(self):
        md = '''
This is a UL:

- Element
- Element with **bold**
- _Italic element_
- Element with [link](www.url.com)    
'''

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This is a UL:</p><ul><li>Element</li><li>Element with <b>bold</b></li><li><i>Italic element</i></li><li>Element with <a href="www.url.com">link</a></li></ul></div>',
        )
        
    def test_ol(self):
        md = '''
This is a OL:

1. Element
2. Element with **bold**
3. _Italic element_
4. Element with [link](www.url.com)
'''

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This is a OL:</p><ol><li>Element</li><li>Element with <b>bold</b></li><li><i>Italic element</i></li><li>Element with <a href="www.url.com">link</a></li></ol></div>',
        )
        
if __name__ == "__main__":
    unittest.main()