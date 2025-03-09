import unittest  # our unit testing lib :)
# CRITICAL: methods & filename must start with "test_" to be discoverable by "unittest"

from generate_page import extract_title  # import modules


class TestGeneratePage(unittest.TestCase):
    # GENERATE PAGE Testing
    # simple test to see if header works
    def test_extract_header(self):
        # our markdown input text
        md = """# Header 1"""
        title = extract_title(md)  # run the func on it
        self.assertEqual("Header 1", title)

    # white space added
    def test_extract_header_whitespace(self):
        # our markdown input text
        md = """  #  Header 1    """
        title = extract_title(md)  # run the func on it
        self.assertEqual("Header 1", title)

    # wrong format expect error
    def test_extract_header_not_h1(self):
        # our markdown input text
        md = """  ###  Header 3    """
        # Using context manager to check exception ("with")
        with self.assertRaises(Exception):
            extract_title(md)  # when called on markdown


if __name__ == "__main__":
    unittest.main()