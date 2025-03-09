import unittest  # our unit testing lib :)
# CRITICAL: methods & filename must start with "test_" to be discoverable by "unittest"

from block_markdown import markdown_to_blocks  # import modules
from blocktype import (BlockType,
                       block_to_block_type)  # import modules


class TestBlockMarkdown(unittest.TestCase):
    # BLOCK SPLIT TESTING
    # simple test to see if it works
    def test_markdown_to_blocks(self):
        # our markdown input text
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)  # run the func on it
        self.assertEqual(  # output must be equal to this
            blocks,  # our blocks func must equal below output
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    # test with whitespace lines
    def test_markdown_to_blocks_with_whitespace_only_lines(self):
        # many white space lines
        md = """
                            
        This is a paragraph
                            
                            
        Another paragraph
                            
        """
        blocks = markdown_to_blocks(md)  # run the func on it
        self.assertEqual(  # output must be equal to this
            blocks,
            [
                "This is a paragraph",
                "Another paragraph",
            ],
        )

    # test with empty input
    def test_markdown_to_blocks_empty_input(self):
        md = ""  # empty string
        blocks = markdown_to_blocks(md)  # run the func on it
        self.assertEqual(blocks, [])  # assume empty list will return

    # test with no test only white space
    def test_markdown_to_blocks_only_whitespace(self):
        md = "   \n  \n  \t  "  # only white space and newlines
        blocks = markdown_to_blocks(md)  # run the func on it
        self.assertEqual(blocks, [])  # assume empty list will return


    # BLOCKTYPE TESTING
    # test with all blocktypes
    def test_block_to_block_type_all_types(self):
        # WHITESPACE (whitespace handled by markdown_to_blocks, but just for safety)
        self.assertEqual(block_to_block_type(" "), None)  # space
        self.assertEqual(block_to_block_type("            "), None)  # many spaces
        # PARAGRAPH
        self.assertEqual(block_to_block_type("This is a paragraph"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("123 123 123 123 123"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("                       Wow"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(""), None)  # empty isn't a paragraph
        # HEADING
        self.assertEqual(block_to_block_type("# Heading1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading3"), BlockType.HEADING)
        # CODE
        self.assertEqual(block_to_block_type("```This is code```"), BlockType.CODE)  # quote as code
        self.assertEqual(block_to_block_type("``````"), BlockType.CODE)  # empty code block
        self.assertEqual(block_to_block_type("```## Heading code```"), BlockType.CODE)  # "Heading" code block
        self.assertEqual(block_to_block_type("```<this is quote of code```"), BlockType.CODE)  # "Quote" code block
        # QUOTE
        self.assertEqual(block_to_block_type(">This is a quote"), BlockType.QUOTE)  # text as quote 
        self.assertEqual(block_to_block_type(">    This is an indented quote"), BlockType.QUOTE)  # text as indented quote
        self.assertEqual(block_to_block_type(">## Heading quote"), BlockType.QUOTE)  # "Heading" quote inside
        self.assertEqual(block_to_block_type(">```code block```"), BlockType.QUOTE)  # "Code" quote inside
        self.assertEqual(block_to_block_type("<wrong quote syntax"), BlockType.PARAGRAPH)  # wrong syntax is paragraph
        # UNORDERED LISTS
        self.assertEqual(block_to_block_type("- Single List"), BlockType.UNORDERED_LIST)  # text as unordered list
        self.assertEqual(block_to_block_type("- item1\n- item2\n- item3"), BlockType.UNORDERED_LIST)  # multiple lines
        self.assertEqual(block_to_block_type("--Single List"), BlockType.PARAGRAPH)  # wrong syntax is paragraph
        self.assertEqual(block_to_block_type("-- Single List"), BlockType.PARAGRAPH)  # wrong syntax is paragraph
        self.assertEqual(block_to_block_type("- item1\n-- item2\n-item3"), BlockType.PARAGRAPH)  # wrong syntax is paragraph
        # ORDERED LISTS
        self.assertEqual(block_to_block_type("1. Single List"), BlockType.ORDERED_LIST)  # text as ordered list
        self.assertEqual(block_to_block_type("1. item1\n2. item2\n3. item3"), BlockType.ORDERED_LIST)  # multiple lines
        self.assertEqual(block_to_block_type("1. item1\n3. item3\n5. item5"), BlockType.PARAGRAPH)  # not incr +1 is paragraph
        self.assertEqual(block_to_block_type("4. Single List"), BlockType.PARAGRAPH)  # not start at 1 is paragraph
        self.assertEqual(block_to_block_type("1.Single List"), BlockType.PARAGRAPH)  # wrong syntax is paragraph
        self.assertEqual(block_to_block_type("1 Single List"), BlockType.PARAGRAPH)  # wrong syntax is paragraph
        self.assertEqual(block_to_block_type("1. item1\n2 item2\n3.item3"), BlockType.PARAGRAPH)  # wrong syntax is paragraph

    # test markdown_to_blocks stripping block correct and getting expected type
    def test_block_to_block_type_with_markdown_to_blocks(self):
        # ORDERED LISTS - correct syntax
        md = "   1. item1 \n 2. item2 \n 3. item3     "  # whitespace riddled markdown, syntax is wrong
        blocks = markdown_to_blocks(md)  # strip and create blocks
        self.assertEqual(len(blocks), 1)  # 1 block with multiple items!
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.ORDERED_LIST)  # block should be ordered list

        # ORDERED LISTS - wrong syntax
        md = "   1. item1 \n\n 2. item2      \n\n\n 3. item3     "  # whitespace riddled markdown, syntax is wrong
        blocks = markdown_to_blocks(md)  # strip and create blocks
        self.assertEqual(len(blocks), 3)  # should be block of 3 lines (because of busted syntax)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.ORDERED_LIST)  # 1st is ordered list
        self.assertEqual(block_to_block_type(blocks[1]), BlockType.PARAGRAPH)  # 2nd is PARAGRAPH
        self.assertEqual(block_to_block_type(blocks[2]), BlockType.PARAGRAPH)  # 3rd is PARAGRAPH


if __name__ == "__main__":
    unittest.main()