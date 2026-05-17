import os, shutil, sys

from functions import copy_dir_r, generate_pages_recursive


def main():
    if len(sys.argv) == 1:
        basepath = "/"
    elif len(sys.argv) == 2:
        basepath = sys.argv[1]
    else:
        raise Exception("invalid argument count")
    
    # Setting default static content and Markdown content folders, and default template in project root.
    static_origin = "static"
    content_origin = "content"
    html_template = "template.html"
    
    # Default public folder. Where the page is gonna be created.
    public_destination = "docs" 

    
    # Removing existing public folder if already exists.
    if os.path.exists(public_destination):
        shutil.rmtree(public_destination)
        
    # Copying contents of static folder to public
    print(f"Copying static content from {static_origin} folder:")
    copy_dir_r(static_origin, public_destination)
    
    # Generating page
    print(f"\nGenerating pages using {html_template} in {public_destination} folder:")
    generate_pages_recursive(content_origin, html_template, public_destination, basepath)
    print("")

if __name__ == "__main__":
    main()