import unittest  # our unit testing lib :)
# CRITICAL: methods & filename must start with "test_" to be discoverable by "unittest"

from htmlnode import HTMLNode, LeafNode  # import modules


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

    # to_html test: with a given tag and value, Leafnodes with to_html should print correctly!
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")  # tag & value input
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")  # returns string

    # to_html: LeafNode children test (no Value)
    def test_leaf_children(self):
        node = LeafNode("a", None)  # value = None
        # Using context manager to check exception ("with")
        with self.assertRaises(ValueError):  # ValueError!
            node.to_html()  # when called on cnode
        
    # to_html: no tag returns raw value
    def test_leaf_no_tag(self):
        node = LeafNode(None, "Hello, world!")  # tag = None
        self.assertEqual(node.to_html(), "Hello, world!")  # raw value string


if __name__ == "__main__":
    unittest.main()