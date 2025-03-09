import re  # Regex import
import os  # for filemanagement
import shutil  # for file copying

from block_to_html import markdown_to_html_node  # import module
from htmlnode import (LeafNode,
                      ParentNode)  # import htmlnode classes
# Note: don't need to directly access the class to get access to the methods


# pull h1 header from markdown
# remove single # and all whitespace L&R
def extract_title(markdown):
    title_match = re.search(r'^\s*# (.+)$', markdown, re.MULTILINE)
    # ^ - start of a line (with MULTILINE flag)
    # \s* - zero or more whitespace characters
    # "# " - symbol followed by a space
    # (.+) - one or more characters (this is captured)
    # $ - end of line
    if title_match:  # if this is found
        # Return the captured group (everything after "# "), stripped of whitespace
        return title_match.group(1).strip()
        # group(0) would be entire string...
    raise Exception("No h1 header!")  # if not returned!

# print message busy generating
# read md from path and store in var
# read template and store in var
# use markdown_to_html_node and .to_html() meth to conv md to html str
# use extract_tilte to grab the page title
# replace {{ Title }} and {{ Content }} w HTML and title generated
# write FULL HTML page to dest_path -- new folders required to be made
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")  # our busy message

    # GETTING TITLE & CONTENT
    # read and store md file from path
    with open(from_path, "r") as file:  # "r" for read
        md = file.read()  # store in md
    # read and store templ file from path
    with open(template_path, "r") as file:
        template = file.read()  # store in template

    # CREATING OUTPUT HTML PAGE FROM TEMPLATE
    md_node = markdown_to_html_node(md)  # convert md to HTMLNode
    content = md_node.to_html()  # conv HTMLNode to html string (content)
    title = extract_title(md)  # grab the title (title)
    output_html = template.replace("{{ Title }}", title)  # insert our title to template
    output_html = output_html.replace("{{ Content }}", content)  # insert our content to template

    # BASEPATH REPLACE:
    output_html = output_html.replace('href="/', f'href="{basepath}/')  # url navigation link (Hypertext REFerence)
    output_html = output_html.replace('src="/', f'src="{basepath}/')  # elements to load (SouRCe)
    # "/" just means to start at root of website... that's our default
    # BASEPATH is var to store roof of website ("/" good for local, Github prefers "/repo-name/")


    # FULL PAGE CREATION
     # create distination folders including subfolders!
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)  # exist_ok is builtin flag to check if already existing
    # write the full htmlpage to  path
    with open(dest_path, "w") as file:  # "w" for write
        file.write(output_html)  # write html page to path!

# crawl every entry in content dir
# for each md, make new .html usin template.html
# all pages written to DOCS dir using same dir structure
# EXACT structure as copy_static, but need to process different filetypes in for loop's else!
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    static_items = os.listdir(dir_path_content)  # list of file paths in content folder

    # loop each file AND subfolder in "static"
    for item in static_items:
        source_path = os.path.join(dir_path_content, item)  # static content item path
        destination_path = os.path.join(dest_dir_path, item)  # DOCS html item path
        # if a folder (not a file)
        if os.path.isdir(source_path):
            print(f"Debug: {destination_path} is a folder, recurse")
            # use makedirs (to include subfolders) with exist_ok=True to only make folder if not existing
            os.makedirs(destination_path, exist_ok=True)  # create folder & subfolders in DOCS
            generate_pages_recursive(source_path, template_path, destination_path, basepath)  # recurse folder UNTIL we reach files
        # otherwise it's a file AND ONLY IF IT'S MARKDOWN!
        else:
            if item == "index.md":  # if it's markdown index file eg index.md
                print(f"Debug: {source_path} is an index.md, generate HTML page")
                # take destination path and add on index.html
                # this renames it to the correct filetype!
                html_destination = os.path.join(os.path.dirname(destination_path), "index.html")
                generate_page(source_path, template_path, html_destination, basepath)  # generate the page
            else:  # if it's not index.md
                print(f"Debug: {source_path} is not an index.md, skipping")