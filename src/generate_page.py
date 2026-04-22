from pathlib import Path

from src.nodes.utils.convert import markdown_to_html_node
from src.nodes.utils.extract import extract_title


def generate_page(
    from_path: Path, template_path: Path, dest_path: Path, basepath: str
) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with from_path.open("r") as f:
        markdown_content = f.read()

    with template_path.open("r") as f:
        template_content = f.read()

    html_string = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)

    template_content = (
        template_content
        .replace("{{ Content }}", html_string)
        .replace("{{ Title }}", title)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )

    dest_path.parent.mkdir(parents=True, exist_ok=True)

    with dest_path.open("w") as f:
        f.write(template_content)


def generate_pages_recursive(
    dir_path_content: Path, template_path: Path, dest_dir_path: Path, basepath: str
) -> None:
    for src_path in dir_path_content.iterdir():
        dest_path = dest_dir_path / src_path.name

        if src_path.is_file() and src_path.suffix == ".md":
            generate_page(
                src_path, template_path, dest_path.with_suffix(".html"), basepath
            )
        elif src_path.is_dir():
            generate_pages_recursive(src_path, template_path, dest_path, basepath)
