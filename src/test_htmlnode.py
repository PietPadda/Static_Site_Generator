import unittest  # our unit testing lib :)
# CRITICAL: methods & filename must start with "test_" to be discoverable by "unittest"

from htmlnode import HTMLNode  # import modules


class TestHTMLNode(unittest.TestCase):
    # check if both are equal
    def test_eq(self):
        node = HTMLNode("a", "paragraph text", None, {"href": "https://www.google.com"})
        node2 = HTMLNode("a", "paragraph text", None, {"href": "https://www.google.com"})
        self.assertEqual(node, node2)  # state (assert) that these must be equal to pass!

    # check if both are unequal
    def test_uneq(self):
        node = HTMLNode("a", None, ["Bob"], {"href": "https://www.google.com"})
        node2 = HTMLNode("h", None, ["John"], {"target": "_blank"})
        self.assertNotEqual(node, node2)  # check they are not equal!

    # check if has children (thus no value)
    def test_has_children(self):
        node = HTMLNode("a", None, ["Bob"], {"href": "https://www.google.com"})
        self.assertEqual(node.value, None)  # check if value=None ie has children

    # check if has children (thus no value)
    def test_has_no_children(self):
        node = HTMLNode("a", "paragraph text", None, {"href": "https://www.google.com"})
        self.assertNotEqual(node.value, None)  # check if value=None ie has children


if __name__ == "__main__":
    unittest.main()