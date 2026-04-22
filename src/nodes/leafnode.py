from src.nodes.htmlnode import HTMLNode

VOID_TAGS: set[str] = {"img"}


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str | None] | None = None,
    ) -> None:
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if self.tag in VOID_TAGS:
            return f"<{self.tag}{self.props_to_html()}>"

        if not self.value:
            raise ValueError("LeafNode object must have a value")
        if not self.tag:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
