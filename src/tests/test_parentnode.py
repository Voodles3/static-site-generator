import unittest

from src.nodes.leafnode import LeafNode
from src.nodes.parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        res = node.to_html()
        self.assertEqual(
            res, "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_to_html_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchild(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_many_children(self):
        child1 = LeafNode("p", "child 1 text")
        child2 = LeafNode("p", "child 2 text")
        child3 = LeafNode("p", "child 3 text")
        child4 = LeafNode("p", "child 4 text")
        child5 = LeafNode("p", "child 5 text")
        parent_node = ParentNode("div", [child1, child2, child3, child4, child5])
        res = parent_node.to_html()
        self.assertEqual(
            res,
            "<div><p>child 1 text</p><p>child 2 text</p><p>child 3 text</p><p>child 4 text</p><p>child 5 text</p></div>",
        )

    def test_to_html_with_deep_nesting(self):
        level4 = LeafNode("p", "BOTTOM LEVEL TEXT")
        level3 = ParentNode("span", [level4])
        level2 = ParentNode("article", [level3])
        level1 = ParentNode("div", [level2])
        res = level1.to_html()
        self.assertEqual(
            res, "<div><article><span><p>BOTTOM LEVEL TEXT</p></span></article></div>"
        )

    def test_to_html_with_children_nesting_and_props(self):
        level4_0 = LeafNode("p", "BOTTOM LEVEL TEXT")
        level4_1 = LeafNode(
            "a", "BOTTOM LEVEL LINK", {"href": "hello.com", "target": "_blank"}
        )
        level4_2 = LeafNode("b", "BOTTOM LEVEL BOLD", {"boldness": "high"})

        level3_0 = ParentNode("aside", [level4_0, level4_1], {"test_prop": "value"})
        level3_1 = ParentNode("span", [level4_2])

        level2 = ParentNode("div", [level3_0])

        level1 = ParentNode("body", [level3_1, level2], {"bodyprop": "yessir"})

        res = level1.to_html()
        self.assertEqual(
            res,
            "".join(
                [
                    '<body bodyprop="yessir">',
                    "<span>",
                    '<b boldness="high">BOTTOM LEVEL BOLD</b>',
                    "</span>",
                    "<div>",
                    '<aside test_prop="value">',
                    "<p>BOTTOM LEVEL TEXT</p>",
                    '<a href="hello.com" target="_blank">BOTTOM LEVEL LINK</a>',
                    "</aside>",
                    "</div>",
                    "</body>",
                ]
            ),
        )
