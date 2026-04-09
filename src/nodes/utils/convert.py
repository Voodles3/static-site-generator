from src.nodes.leafnode import LeafNode
from src.nodes.textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if not isinstance(text_node.text_type, TextType):
        raise TypeError("text_node text type must be a TextType")

    text = text_node.text
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(tag=None, value=text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value=text, props={"href": text_node.url})

    raise RuntimeError("Unreachable code position")
