import unittest

from src.nodes.textnode import TextNode, TextType
from src.nodes.utils.split_nodes import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)


class TestSplit(unittest.TestCase):
    def test_split_bold(self):
        res = split_nodes_delimiter(
            [TextNode("this is **bold** text **andmore**", TextType.TEXT)],
            "**",
            TextType.BOLD,
        )
        self.assertEqual(
            res,
            [
                TextNode("this is ", TextType.TEXT, None),
                TextNode("bold", TextType.BOLD, None),
                TextNode(" text ", TextType.TEXT, None),
                TextNode("andmore", TextType.BOLD, None),
            ],
        )

    def test_split_italic(self):
        res = split_nodes_delimiter(
            [TextNode("this is *italic* text", TextType.TEXT)], "*", TextType.ITALIC
        )
        self.assertEqual(
            res,
            [
                TextNode("this is ", TextType.TEXT, None),
                TextNode("italic", TextType.ITALIC, None),
                TextNode(" text", TextType.TEXT, None),
            ],
        )

    def test_split_code(self):
        res = split_nodes_delimiter(
            [TextNode("this is `code` text", TextType.TEXT)], "`", TextType.CODE
        )
        self.assertEqual(
            res,
            [
                TextNode("this is ", TextType.TEXT, None),
                TextNode("code", TextType.CODE, None),
                TextNode(" text", TextType.TEXT, None),
            ],
        )

    def test_split_plain(self):
        res = split_nodes_delimiter(
            [TextNode("this is **plain** text", TextType.TEXT)], "**", TextType.TEXT
        )
        self.assertEqual(
            res,
            [
                TextNode("this is ", TextType.TEXT, None),
                TextNode("plain", TextType.TEXT, None),
                TextNode(" text", TextType.TEXT, None),
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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and text after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and text after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://vaughnchristman.com) and another [second link](example.com) and text after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://vaughnchristman.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "example.com"),
                TextNode(" and text after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_repeated_identical_links(self):
        node = TextNode(
            "[link](example.com) and again [link](example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "example.com"),
                TextNode(" and again ", TextType.TEXT),
                TextNode("link", TextType.LINK, "example.com"),
            ],
            new_nodes,
        )

    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode("First ![one](one.png) after", TextType.TEXT),
            TextNode("Second ![two](two.png) after", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("First ", TextType.TEXT),
                TextNode("one", TextType.IMAGE, "one.png"),
                TextNode(" after", TextType.TEXT),
                TextNode("Second ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "two.png"),
                TextNode(" after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_preserves_non_text_nodes(self):
        link_node = TextNode("already split", TextType.LINK, "example.com")
        image_node = TextNode("image alt", TextType.IMAGE, "image.png")
        new_nodes = split_nodes_link([
            link_node,
            TextNode("Text with [link](new.com)", TextType.TEXT),
            image_node,
        ])
        self.assertListEqual(
            [
                link_node,
                TextNode("Text with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "new.com"),
                image_node,
            ],
            new_nodes,
        )
