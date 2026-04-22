import os
import shutil
import sys
from pathlib import Path

from src.generate_page import generate_pages_recursive


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_dir(Path("static/"), Path("docs/"))
    generate_pages_recursive(
        Path("content/"), Path("template.html"), Path("docs/"), basepath
    )


def copy_dir(src: Path, dest: Path) -> None:
    if not os.path.exists(src):
        raise FileNotFoundError("Source directory not found")

    if not os.path.exists(dest):
        os.mkdir(dest)
    else:
        dir_contents = os.listdir(dest)
        for name in dir_contents:
            path = os.path.join(dest, name)
            if os.path.isfile(path):
                os.remove(path)
            else:
                shutil.rmtree(path)

    contents = os.listdir(src)
    for name in contents:
        path = os.path.join(src, name)

        if os.path.isfile(path):
            print(f"COPYING FILE {path} TO {dest}")
            shutil.copy(path, dest)
        else:
            dir_name = os.path.join(dest, name)
            print(f"COPYING DIR {path} TO {dir_name}")
            copy_dir(Path(path), Path(dir_name))


if __name__ == "__main__":
    main()
