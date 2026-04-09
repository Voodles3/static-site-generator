from src.nodes.htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: dict[str, str | None] | None = None,
    ):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode object must have a tag")
        if not self.children:
            raise ValueError("ParentNode object must have children")

        out_lines = []

        for child in self.children:
            out_lines.append(child.to_html())

        return f"<{self.tag}{self.props_to_html()}>{''.join(out_lines)}</{self.tag}>"
