import unittest  # our unit testing lib :)
# CRITICAL: methods & filename must start with "test_" to be discoverable by "unittest"

from textnode import (TextNode, 
                      TextType)  # import modules
from inline_markdown import (split_nodes_delimiter,
                             extract_markdown_images,
                             extract_markdown_links,
                             split_nodes_image,
                             split_nodes_link,
                             text_to_textnodes)  # import modules


class TestInlineMarkdown(unittest.TestCase):
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
        new_node = split_nodes_delimiter([old_node], "_", TextType.ITALIC)  # run func on node, ITALIC for "_" delimiter
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


    # Split Inline Textnodes IMAGE & LINK
    # Test Image Split
    def test_split_images(self):
        node = TextNode(  # sample text node with images in it
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])  # use our split func
        self.assertListEqual(  # verify they're equal
            [
                TextNode("This is text with an ", TextType.TEXT),  # text before image
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),  # first image
                TextNode(" and another ", TextType.TEXT),  # text after first image
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"  # second and final image
                ),
            ],
            new_nodes,  # our input to compare (see if split is equal to this assertion)
        )

    # Test Link Split
    def test_split_links(self):
        node = TextNode(  # sample text node with links in it
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])  # use our split func
        self.assertListEqual(  # verify they're equal
            [
                TextNode("This is text with a link ", TextType.TEXT),  # text before link
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),  # first link
                TextNode(" and ", TextType.TEXT),  # text after first link
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"  # second and final link
                ),
            ],
            new_nodes,  # our input to compare (see if split is equal to this assertion)
        )

   # Test Image & Link Split
    def test_split_images_and_links(self):
        node = TextNode(  # sample text node with image & link in it
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes1 = split_nodes_image([node])  # use our split func for images first (NOTE: NODE AS LIST)
        new_nodes2 = split_nodes_link(new_nodes1)  # use our split func for links second (NOTE: Already list... just pass it directly)
        self.assertListEqual(  # verify they're equal
            [
                TextNode("This is text with an ", TextType.TEXT),  # text before image
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),  # first image
                TextNode(" and a link ", TextType.TEXT),  # text after first image
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"  # first and final link
                ),
            ],
            new_nodes2,  # our input to compare (see if split is equal to this assertion)
        )

   # Test Image & Link Split -- multiple nodes
    def test_plit_images_and_links_multiple_nodes(self):
        node1 = TextNode("Text with ![image](https://example.com/img.png)", TextType.TEXT)  # image node
        node2 = TextNode("More text with [link](https://example.com)", TextType.TEXT)  # link node
        
        # Test image splitting on multiple nodes
        result_images = split_nodes_image([node1, node2])  # input both
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),  # split text bore
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),  # get image
                node2  # just return directly
            ],
            result_images  # func call on nodes
        )
        
        # Test link splitting on multiple nodes
        result_links = split_nodes_link([node1, node2])
        self.assertListEqual(
            [
                node1,  # This node should be unchanged since it doesn't contain links
                TextNode("More text with ", TextType.TEXT),  # split text bore
                TextNode("link", TextType.LINK, "https://example.com")  # get link
            ],
            result_links  # func call on nodes
        )
        
        # Test both in sequence (first images, then links)
        intermediate_result = split_nodes_image([node1, node2])  # split image first
        final_result = split_nodes_link(intermediate_result)  # then split link on it
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),  # get text before img
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),  # get img
                TextNode("More text with ", TextType.TEXT),  # get text after img (incl link... call link will process this to split)
                TextNode("link", TextType.LINK, "https://example.com")  # get link
            ],
            final_result  # img func call on nodes then link func call
        )

   # Test Image & Link Split with invalid type
    def test_split_images_and_links_with_invalid_type(self):
        node = TextNode(  # sample text node with image & link in it... invalid type
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link [to youtube](https://www.youtube.com/@bootdotdev)",
            "Chunky",  # "CHUNKY" ie invalid
        )
        # Using context manager to check exception ("with")
        with self.assertRaises(ValueError):  # ValueError!
            split_nodes_image([node])  # This should raise ValueError due to invalid type
        with self.assertRaises(ValueError):  # ValueError!
            split_nodes_link([node])  # This should raise ValueError due to invalid type

    # Test Image & Link Split with empty node
    def test_split_images_and_links_empty_text_nodes(self):
        node = TextNode("", TextType.TEXT)  # empty text
        self.assertListEqual([node], split_nodes_image([node]))  # just return directly
        self.assertListEqual([node], split_nodes_link([node]))  # just return directly

    # Test Image & Link Split with text only
    def test_split_images_and_links_no_matches(self):
        node = TextNode("This is just plain text with no images or links", TextType.TEXT)  # simple text
        self.assertListEqual([node], split_nodes_image([node]))  # just return directly
        self.assertListEqual([node], split_nodes_link([node]))  # just return directly

    # Test Image & Link Split with incorrect syntax
    def test_split_images_and_links_malformed_markdown(self):
        # Incomplete image markdown
        node1 = TextNode("This has a ![broken image](", TextType.TEXT)  # broken image sytnax
        self.assertListEqual([node1], split_nodes_image([node1]))  # just return directly
        
        # Incomplete link markdown
        node2 = TextNode("This has a [broken link](", TextType.TEXT)  # broken link sytnax
        self.assertListEqual([node2], split_nodes_link([node2]))  # just return directly

    # Our "beast" combined splitter, all 3 at once!
    # Combined text splitter -- normal use
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        old_nodes = text_to_textnodes(text)  # we call the beast!

        # we expect the result to be
        new_nodes = [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        # Assert that the actual result matches the expected result
        self.assertListEqual(new_nodes, old_nodes)

    # Combined text splitter -- text only
    def test_text_to_textnodes_text_only(self):
        text = "This is text with an italic word and a code block and an obi wan image https://i.imgur.com/fJRm4Vk.jpeg and a link https://boot.dev"
        old_nodes = text_to_textnodes(text)  # we call the beast!

        # we expect the result to be
        new_nodes = [
        TextNode("This is text with an italic word and a code block and an obi wan image https://i.imgur.com/fJRm4Vk.jpeg and a link https://boot.dev", TextType.TEXT),
        ]

        # Assert that the actual result matches the expected result
        self.assertListEqual(new_nodes, old_nodes)

    # Combined text splitter -- empty
    def test_text_to_textnodes_text_only(self):
        text = ""
        old_nodes = text_to_textnodes(text)  # we call the beast!

        # we expect the result to be
        new_nodes = []

        # Assert that the actual result matches the expected result
        self.assertListEqual(new_nodes, old_nodes)



if __name__ == "__main__":
    unittest.main()