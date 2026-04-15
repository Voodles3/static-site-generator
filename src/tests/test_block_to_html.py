import unittest

from src.nodes.utils.convert import markdown_to_html_node


class TestBlockToHTML(unittest.TestCase):
    def test_paragraph(self):
        md = "This is **bolded** paragraph\ntext in a p\ntag here\n\nThis is another paragraph with _italic_ text and `code` here"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_unordered_list(self):
        md = "This is a paragraph.\nBelow is an unordered list.\n\n- Item 1\n- Item 2\n- Item 3\n\nThis is another paragraph"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a paragraph. Below is an unordered list.</p><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul><p>This is another paragraph</p></div>",
        )

    def test_ordered_list(self):
        md = "This is a paragraph.\nBelow is an ordered list.\n\n1. Item 1\n2. Item 2\n3. Item 3\n\nThis is another paragraph"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a paragraph. Below is an ordered list.</p><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol><p>This is another paragraph</p></div>",
        )

    def test_header(self):
        md = "# This is an h1 element\n\n## This is an h2 element\n\n#This should be a paragraph"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is an h1 element</h1><h2>This is an h2 element</h2><p>#This should be a paragraph</p></div>",
        )

    def test_blockquote(self):
        md = "> This is a blockquote\n\n>This is another one\n\n>>This is also"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote> This is a blockquote</blockquote><blockquote>This is another one</blockquote><blockquote>>This is also</blockquote></div>",
        )
