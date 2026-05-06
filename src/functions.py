from textnode import TextType, TextNode

def split_node_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # This function only process TEXT nodes. If other type, means it has already been processed and converted to the appropriate type
        if node.text_type.TEXT:
            # Applying delimiter
            strings = node.text.split(delimiter)
            # If the result after .split() is even, it means the delimiters are unmatched
            if len(strings) % 2 == 0:
                raise Exception("incorrect Markdown format, unmatched delimiters")
            # If the result is 1, it means there are no delimiters so it has to be passed as TEXT
            if len(strings) == 1:
                new_nodes.append(TextNode(strings[0], TextType.TEXT))
            else:
                for i in range(len(strings)):
                    # Even strings are the ones outside delimiters
                    if i % 2 == 0:
                        new_nodes.append(TextNode(strings[i], TextType.TEXT))
                    # Odd strings are the ones delimited
                    else:
                        new_nodes.append(TextNode(strings[i], text_type))            
        else:
            # Node is not type_text
            new_nodes.append(node)
    return new_nodes