import unittest

from src.nodes.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("Text", TextType.PLAIN, url="Test URL")
        node2 = TextNode("Text", TextType.PLAIN, url="Test URL")
        self.assertEqual(node, node2)

    def test_url_none_eq(self):
        node = TextNode("Text", TextType.PLAIN, url=None)
        node2 = TextNode("Text", TextType.PLAIN)
        self.assertEqual(node, node2)

    def test_text_different(self):
        node = TextNode("Text", TextType.PLAIN)
        node2 = TextNode("Different text", TextType.PLAIN)
        self.assertNotEqual(node, node2)

    def test_type_different(self):
        node = TextNode("Text", TextType.PLAIN)
        node2 = TextNode("Text", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_url_different(self):
        node = TextNode("Text", TextType.PLAIN, url="Test URL")
        node2 = TextNode("Text", TextType.PLAIN, url="Different test URL")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
