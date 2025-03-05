import re  # import ReGex module

# takes raw markdown string (representing full doc)
# returns list of "block" strings ie split into separate strings using blank space
# blank space: \n\n

# put simply, we just take text input and split it based on our newline 
# and return as a list of strings!
def markdown_to_blocks(markdown):
    # The below code DOESN'T handle more than two consecutive \n's...
    # raw_blocks = markdown.split("\n\n")  # we split the text
    # enter REGEX!
    raw_blocks = re.split(r"\n\s*\n", markdown)  # we ReGex split the text disregarding multiple \n's
    # r"...", raw text -- regex on text
    # \n --> match newline char
    # \s* --> matches zero or more WHITESPACE chars (space, tabs etc)
    # \n --> matches final \n
    # this way, we ignore all internal \n's, and only look for further two \n's!
    clean_blocks = []  # initiate our cleaned block list

    # now we want to strip out all whitespace left and right
     # loop through each split block of markdown
    for block in raw_blocks:
        block_lines = block.split("\n")  # we split each line inside each block
        clean_lines = []  # initiate our lines list to clean each line of each block

        # loop through our split block's lines
        for line in block_lines:
            strip_line = line.strip()  # strip whitespace from each individual lines
            if strip_line:  # if it's not an empty line
                # we want to remove any empty lines inside block...
                clean_lines.append(strip_line)  # add to clean lines through loop
        block_strip = "\n".join(clean_lines)  # we rejoin cleaned lines as cleaned individual block

        if block_strip:  # if it's not an empty block
            # we want to remove any empty blocks...
            clean_blocks.append(block_strip)  # we add to clean blocks

    return clean_blocks  # we return the cleaned blocks