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
# exactly one capture group, it returns a list of strings
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
