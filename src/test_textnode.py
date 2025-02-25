import unittest  # our unit testing lib :)
# CRITICAL: methods & filename must start with "test_" to be discoverable by "unittest"

from textnode import TextNode, TextType  # import modules


class TestTextNode(unittest.TestCase):
    # check if both are equal
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)  # missing url!
        node2 = TextNode("This is a text node", TextType.BOLD)  # should be None by def :)
        self.assertEqual(node, node2)  # state (assert) that these must be equal to pass!

    # check texttype are different
    def test_texttype_uneq(self):
        node = TextNode("This is a text node", TextType.BOLD)  # missing url!
        node2 = TextNode("This is a different text node", TextType.ITALIC)  # should be None by def :)
        self.assertNotEqual(node.text_type, node2.text_type)  # check they are not equal!

    # check url is None
    def test_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node.url, None)  # check if url=None

if __name__ == "__main__":
    unittest.main()