from enum import Enum  # for BlockType enums
import re  # for spotting patterns


class BlockType(Enum):
    # Cover all types of text nodes
    PARAGRAPH = "normal block"
    HEADING = "heading block"
    CODE = "code block"
    QUOTE = "quote block"
    UNORDERED_LIST = "unordered list block"
    ORDERED_LIST = "ordered list block"

# It's a FUNCTION, not a method. define OUT of class
# convert markdown block text to blocktype
def block_to_block_type(block):  # note, no self, it's a FUNC, not METH!
    
    # if else to find types
    # first define our ReGex patterns
    is_heading = re.match(r"^#{1,6} ", block)  # HEADING TYPE - starts 1-6# + space + text
    # ^ -- anchors to start of line
    # #{1,6} " -- matches 1 to 6 # chars + space
    # .* is NOT needed as we don't care about content after, we just want to see #'s
    is_quote = re.match(r"^>.*", block)  # QUOTE TYPE - starts  >
    # ^ -- anchors to start of line
    # > -- matches > char
    # .* -- matches rest of line (not just start like header, need to consider all content after)

    # An empty block shouldn't even reach this function if markdown_to_blocks 
    # is filtering correctly, but just in case:
    if not block or block.isspace():  # if empty or a space
        return None  # return None ie not a Block
    elif is_heading:  # if this is TRUE
        return BlockType.HEADING  # return type
    elif block.startswith("```") and block.endswith("```"):  # if start/ends w ```
        return BlockType.CODE
    elif is_quote:  # if this is TRUE
        return BlockType.QUOTE
    elif is_unordered_list(block):  # etc
        return BlockType.UNORDERED_LIST  # if helper func is TRUE
    elif is_ordered_list(block):
        return BlockType.ORDERED_LIST  # if helper func is TRUE
    # Default case
    else:  # it's a normal paragraph
        return BlockType.PARAGRAPH

# helper func for unordered list block
# each line starts with "- "
def is_unordered_list(block):
    lines = block.splitlines()  # split block into lines
    for line in lines:  # loop thru each line
        if re.match(r"^- .*", line):  # if starts with "- "
            # ^ -- anchors to start of line
            # ^- " -- matches - + space
            # .* -- matches rest of line content (else excluded...)
            continue  # go to next line
        else:  # if line not with "- "
            return False  # early exit and return not an unordered_list
    return True  # if all loops continue, it is!

# helper func for ordered list block
# each line starts with "num. " where num is 1 and increments by 1 each line
def is_ordered_list(block):
    lines = block.splitlines()  # split block into lines
    counter = 1  # our first line counter
    for line in lines:  # loop thru each line
        if re.match(rf"^{counter}\. .*", line):  # if starts with "num." -- Dynamic regex (d if static) :)
            # ^ -- anchors to start of line
            # {counter} -- matches the incremented counter starting at 1
            # \. " -- matches a literal "." using \ (. is special char in ReGex) + space
            # .* -- matches rest of line content (else excluded...)
            counter += 1  # increment
            continue  # go to next line
        else:  # if line not match
            return False  # early exit and return not an ordered_list
    return True  # if all loops continue, it is!