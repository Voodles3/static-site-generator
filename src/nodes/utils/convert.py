import re

from src.nodes.blocknode import BlockType
from src.nodes.htmlnode import HTMLNode
from src.nodes.leafnode import LeafNode
from src.nodes.parentnode import ParentNode
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


def markdown_to_blocks(markdown: str) -> list[str]:
    return [s.strip() for s in markdown.split("\n\n") if s.strip()]


def block_to_block_type(block: str) -> BlockType:
    if re.match(r"#{1,6} ", block):
        return BlockType.HEADING
    elif re.match(r"```\n.*```", block, re.S):
        return BlockType.CODE
    elif re.match(r">", block):
        return BlockType.QUOTE
    elif all(re.match(r"- ", line) for line in block.splitlines()):
        return BlockType.UNORDERED_LIST
    elif _is_ordered_list_block(block):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def specify_block_header_type(block: str) -> int:
    """Returns the header type (1 for h1, 2 for h2, etc.) for a heading block"""
    if block_to_block_type(block) != BlockType.HEADING:
        raise ValueError("Cannot determine header type for non-heading block")
    idx = 0
    while idx < 6 and block[idx] == "#":
        idx += 1
    return idx


def _is_ordered_list_block(block):
    lines = block.splitlines()

    for expected_number, line in enumerate(lines, start=1):
        match = re.match(r"^(\d+)\.\s+", line)

        if match is None:
            return False

        actual_number = int(match.group(1))

        if actual_number != expected_number:
            return False

    return True


def markdown_to_html_node(markdown) -> ParentNode:

    blocks = markdown_to_blocks(markdown)
    block_nodes: list[HTMLNode] = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                block = block.replace("\n", " ")
                block_node = ParentNode(tag="p", children=[])
            case BlockType.HEADING:
                header_num = specify_block_header_type(block)
                block_node = ParentNode(tag=f"h{header_num}", children=[])
            case BlockType.CODE:
                code_text_node = TextNode(text=block, text_type=TextType.CODE)
                code_node = text_node_to_html_node(code_text_node)
                parent_node = ParentNode(tag="code", children=[code_node])
                block_node = ParentNode(tag="pre", children=[parent_node])
                continue
            case BlockType.QUOTE:
                block_node = ParentNode(tag="blockquote", children=[])
            case BlockType.UNORDERED_LIST:
                block_node = ParentNode(tag="ul", children=[])
            case BlockType.ORDERED_LIST:
                block_node = ParentNode(tag="ol", children=[])
        assert isinstance(block_node.children, list)  # children will always be a list
        block_node.children.extend(text_to_children(block))
        block_nodes.append(block_node)

    div_node = ParentNode(tag="div", children=block_nodes)
    return div_node


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]
