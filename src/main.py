import os, shutil, argparse

from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from functions import split_node_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, text_to_text_nodes, markdown_to_blocks, block_to_block_type, markdown_to_html_node, block_to_html_nodes
from type_enums import TextType



def copy_dir_r(origin, destination):
    if not os.path.exists(origin):
        raise NotADirectoryError("invalid origin or destination folders")
    if not os.path.exists(destination):
        os.mkdir(destination)
        if args.verbose:
            print(f"{origin}")
    
    for item in os.listdir(origin):
        item_path = os.path.join(origin, item)
        dest_path = os.path.join(destination, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, dest_path)
            if args.verbose:
                print(f"{item_path}")
        else:
            copy_dir_r(item_path, dest_path)


def main():
    # Setting argument parser
    arg_parser = argparse.ArgumentParser(description="Static site generator")
    arg_parser.add_argument("-V", "--verbose", action="store_true", help="prints static folder copy process")
    
    # Catching CLI arguments (see main.sh)
    global args
    args = arg_parser.parse_args()
    
    # Setting default static and public folders in project root
    origin = "static"
    destination = "public"
    
    # Removing existing public folder if exists
    if os.path.exists(destination):
        shutil.rmtree(destination)
        
    # Copying contents of static folder to public
    copy_dir_r(origin, destination)
    

if __name__ == "__main__":
    main()