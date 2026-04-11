import unittest

from src.nodes.utils.extract import extract_markdown_images, extract_markdown_links


class TestExtract(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](linktoimage.png)"
        )
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("second image", "linktoimage.png"),
            ],
            matches,
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://vaughnchristman.com)"
        )
        self.assertListEqual([("link", "https://vaughnchristman.com")], matches)

    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://vaughnchristman.com) and another [second link](example.co.usa)"
        )
        self.assertListEqual(
            [
                ("link", "https://vaughnchristman.com"),
                ("second link", "example.co.usa"),
            ],
            matches,
        )
