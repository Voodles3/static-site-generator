import unittest

from src.nodes.textnode import TextNode, TextType
from src.nodes.utils.split_nodes import split_nodes_delimiter


class TestSplit(unittest.TestCase):
    def test_split_bold(self):
        res = split_nodes_delimiter(
            [TextNode("this is **bold** text", TextType.PLAIN)], "**", TextType.BOLD
        )
        self.assertEqual(
            res,
            [
                TextNode("this is ", TextType.PLAIN, None),
                TextNode("bold", TextType.BOLD, None),
                TextNode(" text", TextType.PLAIN, None),
            ],
        )

    def test_split_italic(self):
        res = split_nodes_delimiter(
            [TextNode("this is *italic* text", TextType.PLAIN)], "*", TextType.ITALIC
        )
        self.assertEqual(
            res,
            [
                TextNode("this is ", TextType.PLAIN, None),
                TextNode("italic", TextType.ITALIC, None),
                TextNode(" text", TextType.PLAIN, None),
            ],
        )

    def test_split_code(self):
        res = split_nodes_delimiter(
            [TextNode("this is `code` text", TextType.PLAIN)], "`", TextType.CODE
        )
        self.assertEqual(
            res,
            [
                TextNode("this is ", TextType.PLAIN, None),
                TextNode("code", TextType.CODE, None),
                TextNode(" text", TextType.PLAIN, None),
            ],
        )

    def test_split_plain(self):
        res = split_nodes_delimiter(
            [TextNode("this is **plain** text", TextType.PLAIN)], "**", TextType.PLAIN
        )
        self.assertEqual(
            res,
            [
                TextNode("this is ", TextType.PLAIN, None),
                TextNode("plain", TextType.PLAIN, None),
                TextNode(" text", TextType.PLAIN, None),
            ],
        )

    def test_split_link_unchanged(self):
        link_node = TextNode("link text", TextType.LINK, "https://example.com")
        res = split_nodes_delimiter([link_node], "**", TextType.BOLD)
        self.assertEqual(res, [link_node])

    def test_split_image_unchanged(self):
        image_node = TextNode("image text", TextType.IMAGE, "image.jpg")
        res = split_nodes_delimiter([image_node], "**", TextType.BOLD)
        self.assertEqual(res, [image_node])
