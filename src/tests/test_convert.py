import unittest

from src.nodes.textnode import TextNode, TextType
from src.nodes.utils.convert import text_node_to_html_node


class TestConvert(unittest.TestCase):
    def test_convert_plain(self):
        node = TextNode("This is a text node", TextType.PLAIN)
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
        self.assertEqual(html_node.props, {"href": "image.jpg"})
