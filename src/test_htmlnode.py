import unittest  # our unit testing lib :)
# CRITICAL: methods & filename must start with "test_" to be discoverable by "unittest"

from htmlnode import HTMLNode, LeafNode, ParentNode  # import modules


class TestHTMLNode(unittest.TestCase):
    #HTMLNode Unit Tests:
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

    # check if has value (thus no children)
    def test_has_no_children(self):
        node = HTMLNode("a", "paragraph text", None, {"href": "https://www.google.com"})
        self.assertEqual(node.children, None)  # check if children=None ie has value


    #LeafNode Unit Tests:
    # to_html test: with a given tag and value, Leafnodes with to_html should print correctly!
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")  # tag & value input
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")  # returns string

    # to_html: LeafNode children test (no Value)
    def test_leaf_children(self):
        node = LeafNode("a", None)  # value = None
        # Using context manager to check exception ("with")
        with self.assertRaises(ValueError):  # ValueError!
            node.to_html()  # when called on node
        
    # to_html: no tag returns raw value
    def test_leaf_no_tag(self):
        node = LeafNode(None, "Hello, world!")  # tag = None
        self.assertEqual(node.to_html(), "Hello, world!")  # raw value string


    #ParentNode Unit Tests:
    #to_html: with children test - 2 level nest
    def test_to_html_parent_with_children(self):
        child_node = LeafNode("span", "child")  # define sample child
        parent_node = ParentNode("div", [child_node])  # define sample parent
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")  # must print this

    #to_html: with grandchildren test - 3 level nest
    def test_to_html_parent_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")  # define sample grandchild
        child_node = ParentNode("span", [grandchild_node])  # define sample child
        parent_node = ParentNode("div", [child_node])  # define sample parent
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    #to_html: with great_grandchildren test - 4 level nest
    def test_to_html_parent_with_great_grandchildren(self):
        great_grandchild_node = LeafNode("i", "great_grandchild")  # define sample great_grandchild
        grandchild_node = ParentNode("b", [great_grandchild_node])  # define sample grandchild
        child_node = ParentNode("span", [grandchild_node])  # define sample child
        parent_node = ParentNode("div", [child_node])  # define sample parent
        self.assertEqual(parent_node.to_html(), "<div><span><b><i>great_grandchild</i></b></span></div>")
        self.assertEqual(child_node.to_html(), "<span><b><i>great_grandchild</i></b></span>")
        self.assertEqual(grandchild_node.to_html(), "<b><i>great_grandchild</i></b>")
        self.assertEqual(great_grandchild_node.to_html(), "<i>great_grandchild</i>")

    #to_html: with children that have children test - 3 level nest
    def test_to_html_parent_with_parentchildren(self):
        grandchild_node = LeafNode("b", "grandchild")  # define sample grandchild
        child_node_with_children = ParentNode("span", [grandchild_node])  # define sample child that's also a parent
        simple_child_node = LeafNode("p", "direct child")  # define sample child that's NOT a parent
        parent_node = ParentNode("div", [child_node_with_children, simple_child_node])  # define sample parent, ch is parent, other ch isnt
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span><p>direct child</p></div>")
        self.assertEqual(child_node_with_children.to_html(), "<span><b>grandchild</b></span>")
        self.assertEqual(grandchild_node.to_html(), "<b>grandchild</b>")
        self.assertEqual(simple_child_node.to_html(), "<p>direct child</p>")

    #to_html: with child that have multiple children test - 3 level nest
    def test_to_html_parent_with_multiple_parentchildren(self):
        grandchild1_node = LeafNode("b", "grandchild1")  # define sample grandchild
        grandchild2_node = LeafNode("q", "grandchild2")  # define sample grandchild
        child_node_with_children = ParentNode("span", [grandchild1_node, grandchild2_node])  # define sample child that's also a parent
        parent_node = ParentNode("div", [child_node_with_children])  # define sample parent, ch is parent, other ch isnt
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild1</b><q>grandchild2</q></span></div>")
        self.assertEqual(child_node_with_children.to_html(), "<span><b>grandchild1</b><q>grandchild2</q></span>")
        self.assertEqual(grandchild1_node.to_html(), "<b>grandchild1</b>")
        self.assertEqual(grandchild2_node.to_html(), "<q>grandchild2</q>")

    #to_html: no children test - no nesting
    def test_to_html_parent_with_no_children(self):
        parent_node = ParentNode("p", None)  # define None children
        # Using context manager to check exception ("with")
        with self.assertRaises(ValueError):  # ValueError!
            parent_node.to_html()  # when called on parent node

    #to_html: no tag test - no nesting
    def test_to_html_parent_with_no_tag(self):
        child_node = ParentNode("span", "child")  # define sample child
        parent_node = ParentNode(None, [child_node])  # define None tag
        # Using context manager to check exception ("with")
        with self.assertRaises(ValueError):  # ValueError!
            parent_node.to_html()  # when called on parent node


if __name__ == "__main__":
    unittest.main()