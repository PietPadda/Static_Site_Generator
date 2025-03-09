import sys  # for CLI handling

from copy_static import copy_static
from generate_page import generate_pages_recursive

def main():
    # get basepath from CLI
    # [1] is command, [0] is script itself (len is 1 with just the script, so >1!)
    # if not there, make it "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    # Delete last DOCS and copy static files over to new DOCS folder
    copy_static(source="static", destination="docs")

    # Generate index.html pages!
    # args: dir_path_content, template_path, dest_dir_path
    content_dir = "content"  # our content folder with mds
    template_path = "template.html"  # our input template html
    output_dir = "docs"  # our output folder with htmls
    generate_pages_recursive(dir_path_content=content_dir,
                  template_path=template_path,
                  dest_dir_path=output_dir, basepath=basepath)


# Need this to run!
if __name__ == "__main__":
    main()