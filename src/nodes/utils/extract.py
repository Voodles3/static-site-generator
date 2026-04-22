import re


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_title(markdown: str) -> str:
    match = re.search(r"^# (.*)", markdown, re.MULTILINE)
    if match:
        return match.group(1).strip()
    raise ValueError("h1 header not found")
