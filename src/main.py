from nodes.textnode import TextNode, TextType


def main():
    new = TextNode("some text here boi", TextType.PLAIN)
    print(new)


if __name__ == "__main__":
    main()
