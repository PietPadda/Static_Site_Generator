import re  # import ReGex module

from blocktype import (BlockType,
                       block_to_block_type)  # import blocktypes

from htmlnode import (HTMLNode,
                      LeafNode,
                      ParentNode)  # import modules

from textnode import (text_node_to_html_node)  # import modules (NB for Code)

from inline_markdown import (text_to_textnodes)  # import modules

from block_markdown import markdown_to_blocks  # import modules


# Block to HTML
# markdown doc to single parent HTMLNode
# contains many child HTMLNodes for nested elements
def markdown_to_html_node(markdown):
    # ParentNode
    # tag = "<div>", value=None, children=children, props=props
    parent = ParentNode("div", [])  # init empty parent node
    blocks = markdown_to_blocks(markdown)  # split md intod blocks

    # now we make the children blocks for this parent HTMLNode
    for block in blocks:  # loop each block
        block_type = block_to_block_type(block)  # get BlockType
        match block_type:  # match w below cases
            # PARAGRAPH
            case BlockType.PARAGRAPH:
                paragraph_node = create_paragraph_node(block)  # create a node
                parent.children.append(paragraph_node)  # add to parent as child
            # HEADING type case
            case BlockType.HEADING:
                heading_node = create_heading_node(block)  # create a node
                parent.children.append(heading_node)  # add to parent as child
            # CODE
            case BlockType.CODE:
                code_node = create_code_node(block)  # create a node
                parent.children.append(code_node)  # add to parent as child
            # QUOTE
            case BlockType.QUOTE:
                quote_node = create_quote_node(block)  # create a node
                parent.children.append(quote_node)  # add to parent as child
            # UNORDERED_LIST
            case BlockType.UNORDERED_LIST:
                unordered_list_node = create_unordered_list_node(block)  # create a node
                parent.children.append(unordered_list_node)  # add to parent as child
            # ORDERED_LIST
            case BlockType.ORDERED_LIST:
                ordered_list_node = create_ordered_list_node(block)  # create a node
                parent.children.append(ordered_list_node)  # add to parent as child

            
    return parent

# Block to HTMLNode Helper Functions
# PARAGRAPH ParentNode
def create_paragraph_node(block):
    # Note: block is only text! can pass block DIRECTLY text_to_children
    # ie no special markers to remove... EXCEPT NEWLINES!
    # Replace newlines with spaces in paragraph text
    # HTML rendering doesn't have \n... so this must be done!
    block = block.replace("\n", " ")
    children = text_to_children(block)  # list of LeafNodes from HTMLNode
    # Parent - p tag, no val, HAS child
    parent = ParentNode("p", children)  # create ParentNode from LeafNodes
    return parent  # our Paragraph ParentNode :)

# HEADING ParentNode
# need no of #s as tag (1-6)
def create_heading_node(block):
    # First get #'s & text
    split_block = block.split(maxsplit=1)  # list of #chars + text
    heading_tag = len(split_block[0])  # get no of #chars for parent
    heading_text = split_block[1]  # get text for children
    # Now create ParentNode!
    children = text_to_children(heading_text)  # list of LeafNodes from HTMLNode
    # Parent - h1-6 tag, no val, HAS child
    parent = ParentNode(f"h{heading_tag}", children)  # create ParentNode from LeafNodes
    return parent  # our Heading ParentNode :)

def create_code_node(block):
    # First need to strip backticks away from START & END... regex is king!
    clean_text = re.sub(r"^```\n?|```$", "", block, flags=re.MULTILINE)
    # sub is replace method for regex
    # ^ is start of line only
    # ``` is opening backticks
    # \n? is for optional newline (some people add a \n after first ```...)
    # | means OR (catches opening, closing and opening&closing for each line)
    # ``` is closing backticks
    # $ is end of line (vs ^ start of line)
    # "" is sub result
    # block is our input
    # re.MULTILINE - regex flag to implement this on EACH line!
    # Now create ParentNode!
    # children w nested "code" tag
    children = text_to_children(clean_text, "code")  # list of LeafNodes from HTMLNode
    # Parent - pre tag, no val, HAS child w nested code tag
    parent = ParentNode("pre", children)  # create ParentNode from LeafNodes
    return parent  # our Code ParentNode :)

# Quote ParentNode
def create_quote_node(block):
    # First need to strip "> " away from EACH start of line... regex is king!
    clean_text = re.sub(r"^> ", "", block, flags=re.MULTILINE)
    clean_text = clean_text.replace("\n", " ")  # replace newlines with spaces (similar to paragraph)
    # sub is replace method for regex
    # ^ is start of line only
    # "> " is txt to "sub"
    # "" is sub result
    # block is our input
    # re.MULTILINE - regex flag to implement this on EACH line!
    # Now create ParentNode!
    children = text_to_children(clean_text)  # list of LeafNodes from HTMLNode
    # Parent - blockquote tag, no val, HAS child
    parent = ParentNode("blockquote", children)  # create ParentNode from LeafNodes
    return parent  # our Quote ParentNode :)

# Unordered List ParentNode
def create_unordered_list_node(block):
    # First need to strip "- " away from EACH start of line... regex is king!
    clean_text = re.sub(r"^- ", "", block, flags=re.MULTILINE)
    # replace "- " w "" on each line!
    # Now create ParentNode!
    children = list_item_children(clean_text)  # list of LeafNodes from HTMLNode)
    # Parent - ul tag, no val, HAS child w nested li tag
    parent = ParentNode("ul", children)  # create ParentNode from LeafNodes
    return parent  # our Unordered List ParentNode :)

# Ordered List ParentNode
def create_ordered_list_node(block):
    # First need to strip "NUM. " away from EACH start of line... regex is king!
    clean_text = re.sub(r"^\d+\. ", "", block, flags=re.MULTILINE)
    # \d+ is for any digit
    # "\. " is for literal . and a space!
    # Now create ParentNode!
    children = list_item_children(clean_text)  # list of LeafNodes from HTMLNode)
    # Parent - ol tag, no val, HAS child w nested li tag
    parent = ParentNode("ol", children)  # create ParentNode from LeafNodes
    return parent  # our Ordered List ParentNode :)

# Shared func
# str txt & returns list of HTMLNodes
# inline markdown ie TextNode-->HTMLNode
# allows adding a nested tag if required!
def text_to_children(text, nested_tag=None):
    # our little CODE block exception
    if nested_tag:  # if it's added
        # If we have a nested tag, create a single leaf node with that tag
        # This path is used for CODE blocks where we don't process markdown
        return [LeafNode(nested_tag, text)]  # early return for CODE block :)

    html_list = []  # init empty list
    text_nodes = text_to_textnodes(text)  # create list of TextNodes from text
    for node in text_nodes:  # loop each node
        html_node = text_node_to_html_node(node)  # create HTMLNode from TextNode
        html_list.append(html_node)  # add HTMLNode to list
    return html_list  # return list

# List children func (DRY!)
# takes text and creates a list of ParentNodes that contain LeafNodes (possibly)!
def list_item_children(clean_text):
    # children are list items with nested "li" tags
    # they are made parents because list items CAN have markdown formatting
    # we wrap the "li" as a ParentNode w/o value, LeafNode is inside!
    list_items = clean_text.split("\n")  # list of list items
    children = []  # init empty list
    for list_item in list_items:  # loop each list item
        children.append(ParentNode("li", text_to_children(list_item)))  # add list item as LeafNode to ParentNode!
    return children