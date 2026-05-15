import os, shutil, argparse

from functions import extract_title, generate_page

# Copies the contents or origin to destination recursively.
# Used to copy the contents from static to public folder.
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
    static_origin = "static"
    static_destination = "public"
    
    # Removing existing public folder if exists
    if os.path.exists(static_destination):
        shutil.rmtree(static_destination)
        
    # Copying contents of static folder to public
    copy_dir_r(static_origin, static_destination)
    
    # Generating page
    generate_page("content/index.md", "template.html", "public/index.html")
    

if __name__ == "__main__":
    main()