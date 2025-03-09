from copy_static import copy_static
from generate_page import generate_pages_recursive

def main():
    # Delete last public and copy static files over to new public folder
    copy_static(source="static", destination="public")

    # Generate index.html pages!
    # args: dir_path_content, template_path, dest_dir_path
    content_dir = "content"  # our content folder with mds
    template_path = "template.html"  # our input template html
    public_dir = "public"  # our output folder with htmls
    generate_pages_recursive(dir_path_content=content_dir,
                  template_path=template_path,
                  dest_dir_path=public_dir)


# Need this to run!
if __name__ == "__main__":
    main()