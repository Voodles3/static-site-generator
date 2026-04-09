import unittest

from src.nodes.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode(
            "a",
            "Click here",
            {"href": "example.com", "target": "_blank"},
        )
        self.assertEqual(
            node.to_html(), '<a href="example.com" target="_blank">Click here</a>'
        )

    def test_repr(self):
        node = LeafNode("<a>", "Click here", {"href": "example.com"})
        node_repr = str(node)
        self.assertEqual(
            node_repr, "LeafNode(<a>, Click here, {'href': 'example.com'})"
        )
