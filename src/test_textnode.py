import unittest  # our unit testing lib :)
# CRITICAL: methods & filename must start with "test_" to be discoverable by "unittest"

from textnode import (TextNode, 
                      TextType, 
                      text_node_to_html_node)  # import modules
from node_splitter import split_nodes_delimiter  # import modules



class TestTextNode(unittest.TestCase):
    # TextNode Unit Tests:
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


    # TextNode to LeafNode Unit Tests
    # TEXT TextNode to LeafNode
    def test_text_to_leaf_text_type(self):
        node = TextNode("This is a text textnode", TextType.TEXT)  # define normal text node
        html_node = text_node_to_html_node(node)  # convert to LeafNode
        self.assertEqual(html_node.tag, None)  # tag MUST be none
        self.assertEqual(html_node.value, "This is a text textnode")  # value MUST be raw str

    # BOLD TextNode to LeafNode
    def test_text_to_leaf_bold_type(self):
        node = TextNode("This is a bold textnode", TextType.BOLD)  # define bold text node
        html_node = text_node_to_html_node(node)  # convert to LeafNode
        self.assertEqual(html_node.tag, "b")  # tag MUST be b
        self.assertEqual(html_node.value, "This is a bold textnode")  # value MUST be raw str

    # ITALIC TextNode to LeafNode
    def test_text_to_leaf_italic_type(self):
        node = TextNode("This is an italic textnode", TextType.ITALIC)  # define italic text node
        html_node = text_node_to_html_node(node)  # convert to LeafNode
        self.assertEqual(html_node.tag, "i")  # tag MUST be i
        self.assertEqual(html_node.value, "This is an italic textnode")  # value MUST be raw str

    # CODE TextNode to LeafNode
    def test_text_to_leaf_code_type(self):
        node = TextNode("This is a code textnode", TextType.CODE)  # define code text node
        html_node = text_node_to_html_node(node)  # convert to LeafNode
        self.assertEqual(html_node.tag, "code")  # tag MUST be code
        self.assertEqual(html_node.value, "This is a code textnode")  # value MUST be raw str

    # LINK TextNode to LeafNode
    def test_text_to_leaf_link_type(self):
        node = TextNode("This is a link textnode", TextType.LINK, "https://www.google.com")  # define link text node
        html_node = text_node_to_html_node(node)  # convert to LeafNode
        self.assertEqual(html_node.tag, "a")  # tag MUST be a
        self.assertEqual(html_node.value, "This is a link textnode")  # value MUST be raw str
        self.assertEqual(html_node.props["href"], "https://www.google.com")  # href dict value MUST be url

    # IMAGE TextNode to LeafNode
    def test_text_to_leaf_image_type(self):
        node = TextNode("Alt text for image", TextType.IMAGE, "https://www.google.com/img.jpg")  # define img link text node
        html_node = text_node_to_html_node(node)  # convert to LeafNode
        self.assertEqual(html_node.tag, "img")  # tag MUST be img
        self.assertEqual(html_node.value, "")  # value MUST be empty str
        self.assertEqual(html_node.props["src"], "https://www.google.com/img.jpg")  # src dict value MUST be url
        self.assertEqual(html_node.props["alt"], "Alt text for image")  # alt dict value MUST be text


    # Old TextNode Splitter Unit Tests
    # OldNode with Bold delimeter, TEXT Type
    def test_node_splitter_text_with_code(self):
        old_node = TextNode("This is text with a `code block` word", TextType.TEXT)  # define normal text node
        new_node = split_nodes_delimiter([old_node], "`", TextType.CODE)  # run func on node, CODE for "`" delimiter
        self.assertEqual(new_node[0], TextNode("This is text with a ", TextType.TEXT))  # index 0 (plain text, even)
        self.assertEqual(new_node[1], TextNode("code block", TextType.CODE))  # index 1 (delimited, uneven)
        self.assertEqual(new_node[2], TextNode(" word", TextType.TEXT))  # index 2 (plain text, even)

    # OldNode with Markdown IMAGE delimiter
    def test_node_splitter_text_with_image(self):
        old_node = TextNode("This is text with an ![alt text](image-url) in it", TextType.TEXT)  # define the text
        new_node = split_nodes_delimiter([old_node], "![", TextType.IMAGE)  # Use ![ as the starting delimiter
        self.assertEqual(new_node[0], TextNode("This is text with an ", TextType.TEXT))  # index 0 (plain text, even)
        self.assertEqual(new_node[1], TextNode("![alt text](image-url)", TextType.IMAGE))  # index 1 (delimited, uneven)
        self.assertEqual(new_node[2], TextNode(" in it", TextType.TEXT))  # index 2 (plain text, even)

    # OldNode with Markdown LINK delimiter
    def test_node_splitter_text_with_link(self):
        old_node = TextNode("This is text with a [link text](url-link) in it", TextType.TEXT)  # define the text
        new_node = split_nodes_delimiter([old_node], "[", TextType.LINK)  # Use [ as the starting delimiter
        self.assertEqual(new_node[0], TextNode("This is text with a ", TextType.TEXT))  # index 0 (plain text, even)
        self.assertEqual(new_node[1], TextNode("[link text](url-link)", TextType.LINK))  # index 1 (delimited, uneven)
        self.assertEqual(new_node[2], TextNode(" in it", TextType.TEXT))  # index 2 (plain text, even)


    # OldNode with non-TEXT Type
    def test_node_splitter_bold_already(self):
        old_node = TextNode("This is a bold textnode", TextType.BOLD)  # define bold text node
        new_node = split_nodes_delimiter([old_node], "**", TextType.BOLD)  # run func on node, BOLD for "**" delimiter
        self.assertEqual(new_node, [TextNode("This is a bold textnode", TextType.BOLD)])  # no change, the same!
    def test_node_splitter_italic_already(self):
        old_node = TextNode("This is an italic textnode", TextType.ITALIC)  # define italic text node
        new_node = split_nodes_delimiter([old_node], "*", TextType.ITALIC)  # run func on node, ITALIC for "*" delimiter
        self.assertEqual(new_node, [TextNode("This is an italic textnode", TextType.ITALIC)])  # no change, the same!

    # OldNode with INVALID Type
    def test_node_splitter_invalid_type(self):
        invalid_type_placeholder = "CHUNKY"  # else it bombs out... doesn't reach code check
        old_node = TextNode("This is an invalid textnode", invalid_type_placeholder)  # define invalid text node
        # Using context manager to check exception ("with")
        with self.assertRaises(ValueError):  # ValueError!
            split_nodes_delimiter([old_node], "!!", invalid_type_placeholder)  # Trigger the split function
    def test_node_splitter_none_type(self):
        old_node = TextNode("This is a null textnode", None)  # define null text node
        # Using context manager to check exception ("with")
        with self.assertRaises(ValueError):  # ValueError!
            split_nodes_delimiter([old_node], "**", None)  # Trigger the split function

    # OldNode with non-CLOSING delimiter
    def test_node_splitter_nonclosing_delimiter(self):
        old_node = TextNode("This is text with a `code block word", TextType.TEXT)  # define normal text node
        # Using context manager to check exception ("with")
        with self.assertRaises(ValueError):  # ValueError!
            split_nodes_delimiter([old_node], "`", TextType.TEXT)  # Trigger the split function





if __name__ == "__main__":
    unittest.main()