import unittest

from src.nodes.blocknode import BlockType
from src.nodes.textnode import TextNode, TextType
from src.nodes.utils.convert import (
    block_to_block_type,
    markdown_to_blocks,
    text_node_to_html_node,
    text_to_textnodes,
)


class TestConvert(unittest.TestCase):
    def test_convert_plain(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "This is a text node")

    def test_convert_bold(self):
        node = TextNode("Bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold node")

    def test_convert_italic(self):
        node = TextNode("Italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic node")

    def test_convert_code(self):
        node = TextNode("Code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code node")

    def test_convert_link(self):
        node = TextNode("Link node", TextType.LINK, url="test.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Link node")
        self.assertEqual(html_node.props, {"href": "test.com"})

    def test_convert_image(self):
        node = TextNode("Image node", TextType.IMAGE, url="image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "Image node")
        self.assertEqual(html_node.props, {"src": "image.jpg", "alt": "Image node"})
        self.assertEqual(html_node.to_html(), '<img src="image.jpg" alt="Image node">')

    def test_convert_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_with_gap(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading(self):
        expected = {
            "# Heading": BlockType.HEADING,
            "## Heading": BlockType.HEADING,
            "### Heading": BlockType.HEADING,
            "#### Heading": BlockType.HEADING,
            "##### Heading": BlockType.HEADING,
            "###### Heading": BlockType.HEADING,
            "## ## Heading": BlockType.HEADING,
            "####### NOT Heading": BlockType.PARAGRAPH,
            "#NOT Heading": BlockType.PARAGRAPH,
            "NOT Heading": BlockType.PARAGRAPH,
        }
        actual = {case: block_to_block_type(case) for case in expected}

        self.assertEqual(expected, actual)

    def test_block_to_block_type_code(self):
        expected = {
            "```\nCode```": BlockType.CODE,
            "```\nCode\n```": BlockType.CODE,
            "```\nCode\n\n```": BlockType.CODE,
            "```\n\nCode\n```": BlockType.CODE,
            "```\nCode\nMore Code\nStill Code\n\n\n```": BlockType.CODE,
            "```\n```": BlockType.CODE,
            "NOT Code": BlockType.PARAGRAPH,
            "\n```NOT Code```": BlockType.PARAGRAPH,
            "`NOT Code`": BlockType.PARAGRAPH,
            "``````": BlockType.PARAGRAPH,
        }
        actual = {case: block_to_block_type(case) for case in expected}

        self.assertEqual(expected, actual)

    def test_block_to_block_type_quote(self):
        expected = {
            "> Quote": BlockType.QUOTE,
            "> Quote\n> More Quote": BlockType.QUOTE,
            "> Quote\nMore Quote": BlockType.QUOTE,
            "NOT Quote": BlockType.PARAGRAPH,
            " > NOT Quote": BlockType.PARAGRAPH,
        }
        actual = {case: block_to_block_type(case) for case in expected}

        self.assertEqual(expected, actual)

    def test_block_to_block_type_unordered_list(self):
        expected = {
            "- List Item": BlockType.UNORDERED_LIST,
            "- List Item\n- More List Item": BlockType.UNORDERED_LIST,
            "- List Item\n- More List Item\n- Last List Item": BlockType.UNORDERED_LIST,
            "NOT List Item": BlockType.PARAGRAPH,
            "-NOT List Item": BlockType.PARAGRAPH,
            "- List Item\nNOT List Item": BlockType.PARAGRAPH,
        }
        actual = {case: block_to_block_type(case) for case in expected}

        self.assertEqual(expected, actual)

    def test_block_to_block_type_ordered_list(self):
        expected = {
            "1. List Item": BlockType.ORDERED_LIST,
            "1. List Item\n2. More List Item": BlockType.ORDERED_LIST,
            "1. List Item\n2. More List Item\n3. Last List Item": BlockType.ORDERED_LIST,
            "NOT List Item": BlockType.PARAGRAPH,
            "1.NOT List Item": BlockType.PARAGRAPH,
            "2. NOT List Item": BlockType.PARAGRAPH,
            "1. List Item\n3. NOT List Item": BlockType.PARAGRAPH,
            "1. List Item\nNOT List Item": BlockType.PARAGRAPH,
        }
        actual = {case: block_to_block_type(case) for case in expected}

        self.assertEqual(expected, actual)

    def test_block_to_block_type_paragraph(self):
        expected = {
            "Paragraph": BlockType.PARAGRAPH,
            "Paragraph\nMore Paragraph": BlockType.PARAGRAPH,
            "This is **bold** text": BlockType.PARAGRAPH,
            "This is _italic_ text": BlockType.PARAGRAPH,
            "This is `code` text": BlockType.PARAGRAPH,
        }
        actual = {case: block_to_block_type(case) for case in expected}

        self.assertEqual(expected, actual)
