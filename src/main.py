from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from functions import split_node_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, text_to_text_nodes, markdown_to_blocks, block_to_block_type, markdown_to_html_node, block_to_html_nodes
from type_enums import TextType

md = '''
### This is a heading\n\n
This is a paragraph of text. It has some **bold** and _italic_ words inside of it. And `a code block`\n\n
- This is the first list item in a list block
- This is a list item
- This is another list item

1. ordered item
2. another item
3. another

>Quote

```
code block```

> Another quote
'''
md2 = '''
- This is the first list **bold** in a list block
- This is a list item
'''
md3 = '''
Text with ![image](image.png) 
'''



nodes = markdown_to_html_node(md2)
print(nodes)
#print(node.to_html())
""" print(blocks)
for item in blocks:
    print(block_to_block_type(item)) """

