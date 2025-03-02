import unittest  # our unit testing lib :)
# CRITICAL: methods & filename must start with "test_" to be discoverable by "unittest"

from textnode import (TextNode, 
                      TextType)  # import modules
from inline_markdown import (split_nodes_delimiter,
                             extract_markdown_images,
                             extract_markdown_links)  # import modules


class TestTextNode(unittest.TestCase):
    # Old TextNode Splitter Unit Tests -- simple inline markdown (bold, italic etc)
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

    # Regex Inline Markdown IMAGE & LINK
    # IMAGE markdown extractor
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)  # for this input
        self.assertListEqual(  # match input shall be
        [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    # LINK markdown extractor
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)  # for this input
        self.assertListEqual(  # match input shall be
        [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    # LINK & IMAGE markdown extractor
    def test_extract_markdown_links_images(self):
        text = "Link [to boot dev](https://www.boot.dev) and image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches_images = extract_markdown_images(text)  # for this input
        matches_links = extract_markdown_links(text)  # for this input
        self.assertListEqual([("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches_images)# match input shall be
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches_links) # match input shall be

    # LINK & IMAGE EMPTY markdown extractor
    def test_extract_markdown_empty_links_images(self):
        text = "Link []() and image ![]()"
        matches_images = extract_markdown_images(text)  # for this input
        matches_links = extract_markdown_links(text)  # for this input
        self.assertListEqual([("", "")], matches_images)# match input shall be
        self.assertListEqual([("", "")], matches_links) # match input shall be

    # LINK & IMAGE NESTED BRACKETS markdown extractor
    def test_extract_markdown_nested_brackets_links_images(self):
        text = "Link [to boot dev[1]](https://www.boot.dev(2)) and image ![obi wan[A]](https://i.imgur.com/fJRm4Vk.jpeg(B)"
        matches_images = extract_markdown_images(text)  # for this input
        matches_links = extract_markdown_links(text)  # for this input
        self.assertListEqual([], matches_images)# match input shall be
        self.assertListEqual([], matches_links) # match input shall be

    # LINK MALFORMED SYNTAX markdown extractor
    def test_extract_markdown_links_with_malformed_syntax(self):
        text = "Incomplete [syntax and [text](https://example.com)"  # ignore "[syntax and " as next match "[text]" works!
        links = extract_markdown_links(text)   # for this input
        self.assertListEqual([("text", "https://example.com")], links)  # Should only match the complete one


if __name__ == "__main__":
    unittest.main()