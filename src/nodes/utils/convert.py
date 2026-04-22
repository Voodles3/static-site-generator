import re
from typing import Literal

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
            return LeafNode(tag="img", value=text, props={"src": text_node.url, "alt": text})

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


def markdown_to_html_node(markdown: str) -> ParentNode:

    blocks = markdown_to_blocks(markdown)
    block_nodes: list[HTMLNode] = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                block_node = _get_paragraph_blocknode(block)
            case BlockType.HEADING:
                block_node = _get_heading_blocknode(block)
            case BlockType.CODE:
                block_node = _get_code_blocknode(block)
            case BlockType.QUOTE:
                block_node = _get_quote_blocknode(block)
            case BlockType.UNORDERED_LIST:
                block_node = _get_list_blocknode(block, "ul")
            case BlockType.ORDERED_LIST:
                block_node = _get_list_blocknode(block, "ol")

        block_nodes.append(block_node)

    div_node = ParentNode(tag="div", children=block_nodes)
    return div_node


def _get_paragraph_blocknode(block: str) -> ParentNode:
    block = block.replace("\n", " ")
    return ParentNode(tag="p", children=text_to_children(block))


def _get_heading_blocknode(block: str) -> ParentNode:
    header_num = specify_block_header_type(block)
    block = block[header_num + 1 :]
    return ParentNode(tag=f"h{header_num}", children=text_to_children(block))


def _get_code_blocknode(block: str) -> ParentNode:
    block = block.removeprefix("```\n").removesuffix("```")
    text_node = TextNode(text=block, text_type=TextType.TEXT)
    code_node = text_node_to_html_node(text_node)
    parent_node = ParentNode(tag="code", children=[code_node])
    return ParentNode(tag="pre", children=[parent_node])


def _get_quote_blocknode(block: str) -> ParentNode:
    block = block.replace(">", "", 1)
    return ParentNode(tag="blockquote", children=text_to_children(block))


def _get_list_blocknode(block: str, tag: Literal["ul", "ol"]) -> ParentNode:
    block_node = ParentNode(tag=tag, children=[])
    block_node.children = []  # Without this, the .append() below errors due to possible nullness for some reason
    for line in block.split("\n"):
        if tag == "ul":
            line = line[2:]
        else:
            line = re.sub(r"^\d+\.\s+", "", line, count=1)

        block_node.children.append(
            ParentNode(tag="li", children=text_to_children(line))
        )
    return block_node


def text_to_children(text: str) -> list[HTMLNode]:

    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]
