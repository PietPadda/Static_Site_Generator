import re  # Regex import
import os  # for filemanagement

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
def generate_page(from_path, template_path, dest_path):
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

    # FULL PAGE CREATION
     # create distination folders including subfolders!
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)  # exist_ok is builtin flag to check if already existing
    # write the full htmlpage to  path
    with open(dest_path, "w") as file:  # "w" for write
        file.write(output_html)  # write html page to path!
