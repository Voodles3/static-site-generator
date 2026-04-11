from src.nodes.leafnode import LeafNode
from src.nodes.textnode import TextNode, TextType
from src.nodes.utils.split_nodes import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if not isinstance(text_node.text_type, TextType):
        raise TypeError("text_node text type must be a TextType")

    text = text_node.text
    match text_node.text_type:
        case TextType.TEXT:
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


def text_to_textnodes(text: str) -> list[TextNode]:
    original = [TextNode(text, TextType.TEXT)]
    bold = split_nodes_delimiter(original, "**", TextType.BOLD)
    italic = split_nodes_delimiter(bold, "_", TextType.ITALIC)
    code = split_nodes_delimiter(italic, "`", TextType.CODE)
    image = split_nodes_image(code)
    link = split_nodes_link(image)
    return link
