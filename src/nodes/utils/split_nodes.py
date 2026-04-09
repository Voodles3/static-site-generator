from src.nodes.textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    out = []
    for node in old_nodes:
        if node.text_type is not TextType.PLAIN:
            out.append(node)
            continue
        sub_strs = node.text.split(delimiter)
        if len(sub_strs) != 3:
            raise ValueError("Invalid Markdown format")
        out.extend(
            [
                TextNode(sub_strs[0], TextType.PLAIN),
                TextNode(sub_strs[1], text_type),
                TextNode(sub_strs[2], TextType.PLAIN),
            ]
        )
    return out
