from copy_static import copy_static
from generate_page import generate_page

def main():
    # Delete last public and copy static files over to new public folder
    copy_static(source="static", destination="public")

    # Generate index.html page!
    # args: from_path, template_path, dest_path
    from_path = "content/index.md"  # our input md
    template_path = "template.html"  # our input template html
    dest_path = "public/index.html"  # our output html
    generate_page(from_path=from_path,
                  template_path=template_path,
                  dest_path=dest_path)


# Need this to run!
if __name__ == "__main__":
    main()