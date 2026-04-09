import unittest

from src.nodes.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("<a>", "Click here", None, {"href": "example.com"})
        node_repr = str(node)
        self.assertEqual(
            node_repr, "HTMLNode(<a>, Click here, None, {'href': 'example.com'})"
        )

    def test_props_to_html(self):
        node = HTMLNode(
            "<a>",
            "Click here",
            None,
            {"href": "example.com", "target": "_blank"},
        )

        res = node.props_to_html()
        self.assertEqual(res, ' href="example.com" target="_blank"')

    def test_props_to_html_none(self):
        node = HTMLNode(
            "<p>",
            "Sample text",
        )
        res = node.props_to_html()
        self.assertEqual(res, "")

    def test_to_html_not_implemented(self):
        node = HTMLNode(
            "<p>",
            "Sample text",
        )
        self.assertRaises(NotImplementedError, node.to_html)
