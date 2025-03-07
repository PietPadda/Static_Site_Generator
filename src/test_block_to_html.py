import unittest  # our unit testing lib :)
# CRITICAL: methods & filename must start with "test_" to be discoverable by "unittest"

from block_to_html import markdown_to_html_node  # import moduels


class TestBlockNode(unittest.TestCase):
    # Paragraph
    def test_paragraphs(self):
            md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            )

    # Heading
    def test_headings(self):
        md = """
    # Heading 1

    ## Heading 2

    ### Heading 3 with **bold**

    ###### Heading 6
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3 with <b>bold</b></h3><h6>Heading 6</h6></div>",
        )


    # Code
    def test_codeblock(self):
            md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            )


    # Quote 
    def test_quotes(self):
        md = """
    > This is a quote
    > with multiple lines
    > and some **bold** text
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with multiple lines and some <b>bold</b> text</blockquote></div>",
        )


    # Unordered list
    def test_unordered_lists(self):
        md = """
    - Item 1
    - Item 2 with _italic_
    - Item 3 with `code`
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2 with <i>italic</i></li><li>Item 3 with <code>code</code></li></ul></div>",
        )


    # Ordered list
    def test_ordered_lists(self):
        md = """
    1. Item 1
    2. Item 2 with _italic_
    3. Item 3 with `code`
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1</li><li>Item 2 with <i>italic</i></li><li>Item 3 with <code>code</code></li></ol></div>",
        )


    # Invalid BlockType (default type is paragraph...)
    def test_invalid_blocktype(self):
        md = "^!* This is an invalid block *!^"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>^!* This is an invalid block *!^</p></div>",
        )


    # Empty markdown...
    def test_empty_input(self):
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")


if __name__ == "__main__":
    unittest.main()