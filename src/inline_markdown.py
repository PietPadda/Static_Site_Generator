import re  # RegEx module
from textnode import TextType, TextNode

# takes 3:
# List of "old nodes", # a delimeter, # and a text type (OF DELIMITER, not OLD NODE!)
# Returns a new list of nodes
# Any text typenodes are (possibly) split 
# into multiple nodes based on syntax
# Doesn't allow nested syntax ie bold inside an italic section etc
# ie ONLY TYPE OF OF DELIMITER PER FUNC CALL!

# Markdown delimeters:
# TEXT = none
# BOLD = **
# ITALIC = _ or single *
# CODE = `
# LINK = [text](url), [ & ] for text, ( & ) for url
# IMAGE = ![alt text](url), ![ & ] for alt text, ( & ) for url
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []  # init empty list

    for node in old_nodes:  # loop through old list
        # Handle unavailable node types
        if not isinstance(node.text_type, TextType):  # check invalid TextType (not in enum list)
            raise ValueError("Invalid Markdown Syntax! TextType Not Handled!")  # raise exception
        # Handle modes of non-TEXT that aren't delimited (no nesting allowed)
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)  # add straight as a node
            continue  # skip following if/else etc as it is TEXT and do next loop

        # Handle TEXT node types
        else:
            if delimiter in ("[", "!["):  # If delimiter is compound ([ or ![)
                # Use parse_compound_delimiter for parsing compound parts
                try:
                    before, delimited_text, after = parse_compound_delimiter(node.text, delimiter)
                except ValueError as e:  # Catch parsing errors
                    raise ValueError(f"Error parsing compound delimiter '{delimiter}': {e}")
                
                # Add 'before', 'delimited_text', and 'after' as nodes
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))
                if delimited_text:
                    new_nodes.append(TextNode(delimited_text, text_type))
                if after:
                    new_nodes.append(TextNode(after, TextType.TEXT))
            # For other delimiters, fall back on the current `str_splitter` logic
            else:
                # split the string into text [0] + delimited [1] + text parts [2]
                text_split = str_splitter(node.text, delimiter)
                if len(text_split) % 2 == 0:  # No matching closing delimiter (if only index 0 & 1, we can assume no closing)
                    raise ValueError(f"No closing '{delimiter}' present in '{node.text}'")  # raises exception
                index_counter = 0  # init text_split counter

                for text in text_split:  # loop through list of split text
                    if text:  # check to avoid adding empty strings!
                        # Normal Text Type (index 0 & 2)
                        if index_counter % 2 == 0:  # if even ie NOT delimited ie TEXT type
                            new_nodes.append(TextNode(text, TextType.TEXT))  # add straight as a node as normal text
                        # Delimted Text Type (index 1)
                        else:
                            new_nodes.append(TextNode(text, text_type))  # add delimted text with relevant type
                        index_counter += 1  # increment counter
    # after finishing looping through all old nodes, we return our processed and delimited "new nodes"
    return new_nodes


# helper func to strip text based on a delimter
def str_splitter(text, delimiter):
    # Splits the text into sections based on the delimiter
    return text.split(delimiter)  # split based on delimiter

# helper func to help LINK & IMAGE with 2 sets of delimimters
def parse_compound_delimiter(text, delimiter):
    # Splits the text into sections based on the delimiter
    if delimiter == "[":
        # LINK = [text](url)
        start = text.find("[")  # link start
        return parse_compound_part(text, start)
    elif delimiter == "![":
        # IMAGE = ![alt text](url)
        start = text.find("![")
        return parse_compound_part(text, start)
    raise ValueError("Unsupported delimiter type!")  # If parsing fails

# helper func to shorten parsing code
def parse_compound_part(text, start):

        if start == -1:
            raise ValueError("Starting delimiter not found in text.")
        end = text.find("](", start)   # Find the closing square bracket and opening parenthesis
        if end == -1:
            raise ValueError("Missing '](...' structure in text.")
        url_end = text.find(")", end)    # Find the closing parenthesis
        if url_end == -1:
            raise ValueError("Missing closing parenthesis in text.")
        # If all components are found, extract the parts
        before = text[:start]  # Text before the compound delimiter
        delimited_text = text[start:url_end + 1]  # Text from the start to the end of the compound part
        after = text[url_end + 1:]  # Text after the compound part
        return before, delimited_text, after


# ReGex Notes:
# If no capture groups, returns a list of strings.
# exactly one capture group, it returns a list of strings (even if only one matches, if text has multiple, you get a list of tuples!)
# multiple capture groups, it returns a list of tuples

# ReGex Image handling
def extract_markdown_images(text):  # input text, output tuples each (alt text, img url)
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches  # tuples of alt text, img url
# r" ", text -- regex on text
# !\[ \] -- alt text escapes, ! is literal (! to differentiate from links!)
# \( \)  -- url link escapes
# ( ) -- capture group
# .*? -- all chars between --> works, but doesn't handled nested [] or ()! replace with...
# [^\[\]]* -- da bomb! breakdown below
# [ --  character class, let's you specify which chars can appear
# ^ -- means NOT, so this class will match any EXCEPT the ones listed after
# \[ -- an escape for the literal [, without \ it's a char class!
# \] -- an escape for the literal ]
# ] -- closes char class definition
# * -- zero or more, in this case, match zero or more that are NOT [ or ]
# [^\(\)]* -- same, just ()s!


# ReGex Links handling
def extract_markdown_links(text):  # input text, output tuples each (anchor text, url link)
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches  # tuples of anchor text, url link
# (?<!...) -- negative look behind, only match if the ... char is not there!
# ... = ! --- the 2nd ! is the char, so if ![ is there, it's NOT a link but an IMAGE!

# Split nodes for IMAGES
def split_nodes_image(old_nodes):
    new_nodes = []  # init empty list

    for node in old_nodes:  # loop through old list
        # Handle unavailable node types
        if not isinstance(node.text_type, TextType):  # check invalid TextType (not in enum list)
            raise ValueError("Invalid Markdown Syntax! TextType Not Handled!")  # raise exception

        # Handle modes of non-TEXT that aren't delimited (no nesting allowed)
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)  # add straight as a node
            continue  # skip following if/else etc as it is TEXT and do next loop

        images = extract_markdown_images(node.text)  # get images extracted from the node
        if not images:  # if it's an empty list ie no images
            new_nodes.append(node)  # add straight as a node
        else:
            current_text = node.text  # init our text to use in loop
            for alt_text, img_url in images:  # loop through images list
                # Split our text by the image, maxsplit 1 to get the first text
                image_split = f"![{alt_text}]({img_url})"  # we set our image text to split
                text_parts = current_text.split(image_split, 1)  # we split the text using above text, maxsplit = 1

                # If there is a text_part 1... set as text, else it's immediately image!
                if text_parts[0]:  # if text before image
                    new_nodes.append(TextNode(text_parts[0], TextType.TEXT))  # we add as text

                # Textnode Syntax: def __init__(self, text, text_type, url=None):
                # We know that first text bit is there now, so we can safely add the image text as node
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, img_url))  # we add our image node extracted

                # There may be remaining text AFTER
                if len(text_parts) >= 2:  # if there definitely is (not just first text and image)
                    current_text = text_parts[1]  # we use the text after... and will check for more images again in loop!
                else:
                    current_text = ""  # otherwise we just return empty for current and break the loop!
                    break  # No more text to process, so exit the loop

            # let's add any remaining text now that loop is broken and no more images are left
            if current_text:  # if there is text left and not images
                new_nodes.append(TextNode(current_text, TextType.TEXT))  # we add as text node!
    return new_nodes  # return our nodes split as TEXT, IMAGE, TEXT, IMAGE etc.


# Split nodes for LINKS
def split_nodes_link(old_nodes):
    new_nodes = []  # init empty list

    for node in old_nodes:  # loop through old list
        # Handle unavailable node types
        if not isinstance(node.text_type, TextType):  # check invalid TextType (not in enum list)
            raise ValueError("Invalid Markdown Syntax! TextType Not Handled!")  # raise exception

        # Handle modes of non-TEXT that aren't delimited (no nesting allowed)
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)  # add straight as a node
            continue  # skip following if/else etc as it is TEXT and do next loop

        links = extract_markdown_links(node.text)  # get LINKS extracted from the node
        if not links:  # if it's an empty list ie no links
            new_nodes.append(node)  # add straight as a node
        else:
            current_text = node.text  # init our text to use in loop
            for anchor_text, link_url in links:  # loop through LINKS list
                # Split our text by the link, maxsplit 1 to get the first text
                link_split = f"[{anchor_text}]({link_url})"  # we set our LINK text to split
                text_parts = current_text.split(link_split, 1)  # we split the text using above text, maxsplit = 1

                # If there is a text_part 1... set as text, else it's immediately LINK!
                if text_parts[0]:  # if text before LINK
                    new_nodes.append(TextNode(text_parts[0], TextType.TEXT))  # we add as text

                # Textnode Syntax: def __init__(self, text, text_type, url=None):
                # We know that first text bit is there now, so we can safely add the LINK text as node
                new_nodes.append(TextNode(anchor_text, TextType.LINK, link_url))  # we add our LINK node extracted

                # There may be remaining text AFTER
                if len(text_parts) >= 2:  # if there definitely is (not just first text and LINK)
                    current_text = text_parts[1]  # we use the text after... and will check for more LINKS again in loop!
                else:
                    current_text = ""  # otherwise we just return empty for current and break the loop!
                    break  # No more text to process, so exit the loop

            # let's add any remaining text now that loop is broken and no more LINKS are left
            if current_text:  # if there is text left and not images
                new_nodes.append(TextNode(current_text, TextType.TEXT))  # we add as text node!
    return new_nodes  # return our nodes split as TEXT, LINK, TEXT, LINK etc.


# Combining all our splitting funcs, the inline markdown "beast"!
# just conv text to "nodes" then run it successively on the same to continue processed it!
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]  # first create our LIST node

    # Now let's apply each type of simple inline markdown
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)  # simple inline bold
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)  # then simple inline italic
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)  # finally simple inline code

    # Now let's apply more complex img & link inline markdown
    nodes = split_nodes_image(nodes)  # image inline splitter
    nodes = split_nodes_link(nodes)  # finally link inline splitter
    return nodes


sample_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
print(text_to_textnodes(sample_text))