from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from functions import split_node_delimiter

node = TextNode("This is `code` and more `code` and **bold** and nothing", TextType.TEXT)

nodes = split_node_delimiter([node], "`", TextType.CODE)
print(split_node_delimiter(nodes, "**", TextType.BOLD))