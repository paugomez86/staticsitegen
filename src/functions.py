import re, os
from enum import Enum

from textnode import TextNode
from htmlnode import ParentNode
from type_enums import TextType, BlockType


# Gets a list of TextNode and splits them into the appropriate types of TextNode depending on the given delimiter and text_type (see TextType enum).
# Returns a list of TextNode having handled the Markdown format delimiters for inline text.   
def split_node_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # This function only process TEXT nodes. If other type, means it has already been processed and converted to the appropriate type
        if node.text_type == TextType.TEXT:
            # Splitting string using delimiters
            strings = node.text.split(delimiter)
            # If the result after .split() is even, it means the delimiters are unmatched
            if len(strings) % 2 == 0:
                raise Exception("incorrect Markdown format, unmatched delimiters")
            # If the result is 1, it means there are no delimiters so it has to be passed as TEXT
            if len(strings) == 1:
                # Before creating the TextNode, line breaks are replaced for spaces.
                text_value = strings[0].replace("\n", " ")
                new_nodes.append(TextNode(text_value, TextType.TEXT))
            else:
                for i in range(len(strings)):
                    # Even strings are the ones outside delimiters
                    if i % 2 == 0:
                        if strings[i] != "":
                            new_nodes.append(TextNode(strings[i], TextType.TEXT))
                    # Odd strings are the ones delimited
                    else:
                        new_nodes.append(TextNode(strings[i], text_type))            
        else:
            # Node is not TEXT
            new_nodes.append(node)
    return new_nodes


# Gets a string in Markdown format and looks for image matches using regex. Pattern is ![alt text](url).
# Returns a list of tuples (alt text, url), one tuple for each image in the given text string.
def extract_markdown_images(text):
    data = []
    # Regex pattern to find image links ![alt_text](url)
    matches = re.findall(r"!\[[^\]]+\]\([\w.:/]+\)", text)
    for match in matches:
        # For each match, separate the alt_text and the url parts. Strip the leading and trailing [] and ()
        alt = re.search(r"\[.*\]", match).group().lstrip("[").rstrip("]")
        url = re.search(r"\(.*\)", match).group().lstrip("(").rstrip(")")
        # Append to the list as a tuple
        data.append((alt, url))
    return data
    

# Gets a string in Markdown format and looks for link matches using regex. Pattern is [anchor text](url).
# Returns a list of tuples (anchor_text, url), one tuple for each link in the given text string.
def extract_markdown_links(text):
    data = []
    # Regex pattern to find image links [anchor_text](url)
    matches = re.findall(r"(?<!\!)\[[^\]]+\]\([\w.:/]+\)", text)
    for match in matches:
        # For each match, separate the anchor_text and the url parts. Strip the leading and trailing [] and ()
        anchor_text = re.search(r"\[.*\]", match).group().lstrip("[").rstrip("]")
        url = re.search(r"\(.*\)", match).group().lstrip("(").rstrip(")")
        # Append to the list as a tuple
        data.append((anchor_text, url))
    return data


# Gets a list of TextNode. Calls extract_markdown_images() for each node and, if there are matches, breaks the node content
# in several TextNode [TEXT, IMAGE, TEXT, TEXT, IMAGE...] and returns the list of the new nodes having handled the existing Markdown images.
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # Id node is not TEXT, it means it has already been handled
        if node.text_type == TextType.TEXT:
            # Getting image data tuples from Markdown matches
            image_tuples = extract_markdown_images(node.text)
            # remaining_text starts being the whole text of the current node.
            # For each image tuple iteration, the text is split using the strings from tuple. 
            # From the .split() result, the first string is the next TEXT node. The second is the IMAGE node
            # The remaining text gets stored for the next tuple iteration.
            remaining_text = node.text
            for alt, url in image_tuples:
                delimiter = f"![{alt}]({url})"
                strings = remaining_text.split(delimiter, 1)
                if strings[0] != "":
                    new_nodes.append(TextNode(strings[0], TextType.TEXT))
                new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                remaining_text = strings[1]
            # When there're no more tuples, the remaining text is the trailing characters after the last image node
            # It's appended as TEXT node if it's not empty
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))    
        else:
            # If node is not TEXT
            new_nodes.append(node)
    return new_nodes


# Gets a list of TextNode. Calls extract_markdown_links() for each node and, if there are matches, breaks the node content
# in several TextNode [TEXT, LINK, TEXT, TEXT, LINK...] and returns the list of the new nodes having handled the existing Markdown links.
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            link_tuples = extract_markdown_links(node.text)
            # See split_nodes_image() for info
            remaining_text = node.text
            for anchor, url in link_tuples:
                delimiter = f"[{anchor}]({url})"
                strings = remaining_text.split(delimiter, 1)
                if strings[0] != "":
                    new_nodes.append(TextNode(strings[0], TextType.TEXT))
                new_nodes.append(TextNode(anchor, TextType.LINK, url))
                remaining_text = strings[1]
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))    
        else:
            # Node is not TEXT
            new_nodes.append(node)
    return new_nodes


# Gets a text in Markdown format and converts it to a list of TextNode, each of the corresponding TextType.
# It calls functions split_node_delimiter() with the appropriate delimiters and types, split_nodes_image() and split_nodes_link().
# Returns a list of TextNode with the appropriate types without Markdown delimiters.
def text_to_text_nodes(text):
    # Creates an initial TextNode with the whole given text string. Then it calls the functions to handle the different types of existing text.
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_node_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_node_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_node_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

# Gets a code block (text between ```) and returns a TextNode.
# Similar to text_to_text_nodes() but in this case it ignores Markdown delimiters.
def text_to_codeblock_node(text):
    return TextNode(text, TextType.TEXT)


# Gets a long string in Markdown format and breaks it in blocks using double line break.
def markdown_to_blocks(markdown):
    blocks_f = []
    block_delimiter = "\n\n"
    blocks = markdown.split(block_delimiter)
    # Stripping extra line breaks and spaces.
    for block in blocks:
        block = block.strip()
        if block != "":
            blocks_f.append(block)
    return blocks_f


# Gets a text block in Markdown format and, using regex, checks the type of the block (see BlockType enum).
# Returns a BlockType enum object.
def block_to_block_type(block):
    # Starts with 1 to 6 #
    heading_regex = r"^#{1,6} .+"
    # Starts and ends with ``` 
    code_regex = r"```\n.+```"
    # Starts with > followed by 1 or none spaces
    quote_regex = r"^> {0,1}.+"
    # Starts with - and space
    # TODO Could be improved breaking down the block in lines and checking every line
    ul_regex = r"^- .+"
    # Starts with 1. and space
    # TODO Could be improved breaking down the block in lines and checking every line starts with consecutive numbers
    ol_regex = r"^1\. .+"
    
    if re.search(heading_regex, block) is not None:
        return BlockType.H
    
    if re.search(code_regex, block, re.DOTALL) is not None:
        return BlockType.CODE
    
    if re.search(quote_regex, block) is not None:
        return BlockType.BLOCKQUOTE
    
    if re.search(ul_regex, block) is not None:
        return BlockType.UL
    
    if re.search(ol_regex, block) is not None:
        return BlockType.OL
    
    return BlockType.P


# Gets a string of Markdown content, calls markdown_to_blocks() to split it in blocks.
# Then calls block_to_html_nodes() to convert each block in a string of HTML code representing the block.
# Returns a single DIV node with the html nodes as children.
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        html_nodes.append(block_to_html_nodes(block))
    return ParentNode("div", html_nodes)


# Gets a block of Markdown content (a string representing a block element). 
# Checks the type of the block (see type_enums.py) and, depending of the type, calls the corresponding
# function to break the block in HTMLNode.
# Returns a single ParentNode of the corresponding tag containing the LeafNode
def block_to_html_nodes(block):
    block_type = block_to_block_type(block)
    
    match block_type:
        case block_type.P:
            return block_p_to_html_node(block)
        
        case block_type.H:
            return block_h_to_html_node(block)
        
        case block_type.CODE:
            return block_code_to_html_node(block)
        
        case block_type.BLOCKQUOTE:
            return block_blockquote_to_html_node(block)
        
        case block_type.UL:
            return block_ul_to_html_node(block)
        
        case block_type.OL:
            return block_ol_to_html_node(block)
                
        case _:
            raise Exception("invalid block type")
        
        
# Gets a list of (or a single) TextNode and calls their self.text_node_to_html_node()
# in a loop to get them converted to HTMLNode. Returns a list. 
def text_nodes_to_html_node(nodes):
    html_nodes = []
    if len(nodes) == 0:
        return None
    for node in nodes:
        html_nodes.append(node.text_node_to_html_node())
    return html_nodes


# The following bunch of functions handle, each one, the corresponding type of block.
# The operations performed on the block and the node handling differ depending on the type.
# Returns a single ParentNode, with the appropriate tag, containing the children LeafNode.
def block_p_to_html_node(block):
    text_nodes = text_to_text_nodes(block)
    html_nodes = text_nodes_to_html_node(text_nodes)
    return ParentNode("p", html_nodes)

def block_h_to_html_node(block):
    match = re.search("^#+ ", block)
    header = block[match.end():]
    header_level = match.end() - 1
    text_nodes = text_to_text_nodes(header)
    html_nodes = text_nodes_to_html_node(text_nodes)
    return ParentNode(f"h{header_level}", html_nodes)

def block_code_to_html_node(block):
    block = block.strip("`").lstrip()
    text_node = text_to_codeblock_node(block)
    html_code_node = ParentNode("code", [text_node.text_node_to_html_node()])
    return ParentNode("pre", [html_code_node])

def block_blockquote_to_html_node(block):
    block = block.lstrip(">").strip()
    text_nodes = text_to_text_nodes(block)
    html_nodes = []
    html_nodes = text_nodes_to_html_node(text_nodes)
    return ParentNode(f"blockquote", html_nodes)

def block_ul_to_html_node(block):
    list_items = block.split("\n")
    html_nodes = []
    for item in list_items:
        item = item[2:].strip()
        text_nodes = text_to_text_nodes(item)
        item_html_nodes = text_nodes_to_html_node(text_nodes)
        html_nodes.append(ParentNode("li", item_html_nodes))
    return ParentNode("ul", html_nodes)

def block_ol_to_html_node(block):
    list_items = block.split("\n")
    html_nodes = []
    for item in list_items:
        item = item[2:].strip()
        text_nodes = text_to_text_nodes(item)
        item_html_nodes = text_nodes_to_html_node(text_nodes)
        html_nodes.append(ParentNode("li", item_html_nodes))
    return ParentNode("ol", html_nodes)
# =====================================================================

# Checks if the given string is a valid H1 Markdown string and returns it stripped.
# Used to generate the title of the page in the head section.
def extract_title(markdown):
    if re.search(r"^# .+", markdown) is None:
        raise Exception("invalid title Markdown")
    return markdown.lstrip("#").strip()


# Gets the path of the content, an html template, and the destination path for the html document.
# Generates the document file combining content with template and stores it in dest_path.
# Creates any necessary subdir.
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    
    with open(template_path, "r") as f:
        template = f.read()
    
    title = extract_title(markdown.split("\n\n", 1)[0])
    document = template.replace("{{ Title }}", title).replace("{{ Content }}", markdown_to_html_node(markdown).to_html())
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True) 
    with open(dest_path, "w") as f:
        f.write(document)
    