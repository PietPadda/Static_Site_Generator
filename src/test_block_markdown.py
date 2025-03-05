import unittest  # our unit testing lib :)
# CRITICAL: methods & filename must start with "test_" to be discoverable by "unittest"

from block_markdown import markdown_to_blocks  # import modules


class TestBlockNode(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()