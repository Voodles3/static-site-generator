from collections.abc import Callable

from src.nodes.textnode import TextNode, TextType
from src.nodes.utils.extract import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    out = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            out.append(node)
            continue
        split_nodes = []
        sub_strs = node.text.split(delimiter)
        if len(sub_strs) % 2 == 0:
            raise ValueError("Invalid Markdown format")
        for i in range(len(sub_strs)):
            if sub_strs[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sub_strs[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sub_strs[i], text_type))
        out.extend(split_nodes)
    return out


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_link_or_image_nodes(
        old_nodes, TextType.IMAGE, extract_markdown_images, "![{text}]({url})"
    )


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_link_or_image_nodes(
        old_nodes, TextType.LINK, extract_markdown_links, "[{text}]({url})"
    )


def _split_link_or_image_nodes(
    old_nodes: list[TextNode],
    expected_type: TextType,
    extract_func: Callable[[str], list[tuple[str, str]]],
    split_format: str,
) -> list[TextNode]:
    out = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            out.append(node)
            continue
        text = node.text
        extracted = extract_func(text)
        if not extracted:
            out.append(node)
            continue
        for extracted_text, extracted_url in extracted:
            sections = text.split(
                split_format.format_map({"text": extracted_text, "url": extracted_url}),
                1,
            )
            if len(sections) != 2:
                raise ValueError("Invalid markdown; image/link section not closed")
            if sections[0] != "":
                out.append(TextNode(sections[0], TextType.TEXT))
            out.append(TextNode(extracted_text, expected_type, extracted_url))
            text = sections[1]
        if text:
            out.append(TextNode(text, TextType.TEXT))
    return out
