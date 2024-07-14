import unittest

from textnode import TextNode, text_node_to_html_node, text_type_enum
from split_delimiter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_url1(self):
        node = TextNode("This is a text node", "italic", "https://boot.dev")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    def test_url2(self):
        node = TextNode("This is a text node", "italic", "https://boot.dev")
        node2 = TextNode("This is a text node", "italic", "https://boot.dev")
        self.assertEqual(node, node2)

    def test_text1(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is not a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_text2(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("THIS IS A TEXT NODE", "bold")
        self.assertNotEqual(node, node2)

    def test_style(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

class TestTextNodeToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", text_type_enum.type_text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", text_type_enum.type_image, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", text_type_enum.type_bold)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

class TestSplitDelimiter(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_enum.type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_enum.type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_enum.type_text),
                TextNode("bolded", text_type_enum.type_bold),
                TextNode(" word", text_type_enum.type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_type_enum.type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_enum.type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_enum.type_text),
                TextNode("bolded", text_type_enum.type_bold),
                TextNode(" word and ", text_type_enum.type_text),
                TextNode("another", text_type_enum.type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_type_enum.type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_enum.type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_enum.type_text),
                TextNode("bolded word", text_type_enum.type_bold),
                TextNode(" and ", text_type_enum.type_text),
                TextNode("another", text_type_enum.type_bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", text_type_enum.type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_enum.type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_enum.type_text),
                TextNode("italic", text_type_enum.type_italic),
                TextNode(" word", text_type_enum.type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", text_type_enum.type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_enum.type_bold)
        new_nodes = split_nodes_delimiter(new_nodes, "*", text_type_enum.type_italic)
        self.assertListEqual(
            [
                TextNode("bold", text_type_enum.type_bold),
                TextNode(" and ", text_type_enum.type_text),
                TextNode("italic", text_type_enum.type_italic),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", text_type_enum.type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_enum.type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_enum.type_text),
                TextNode("code block", text_type_enum.type_code),
                TextNode(" word", text_type_enum.type_text),
            ],
            new_nodes,
        )

class TestRegexFunctions(unittest.TestCase):
    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        temp = extract_markdown_images(text)
        self.assertEqual(temp, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        temp = extract_markdown_links(text)
        self.assertEqual(temp, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

class TestSplitNodeFunctions(unittest.TestCase):
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            text_type_enum.type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_enum.type_text),
                TextNode("image", text_type_enum.type_image, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            text_type_enum.type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", text_type_enum.type_image, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_enum.type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_enum.type_text),
                TextNode("image", text_type_enum.type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_enum.type_text),
                TextNode(
                    "second image", text_type_enum.type_image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            text_type_enum.type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_enum.type_text),
                TextNode("link", text_type_enum.type_link, "https://boot.dev"),
                TextNode(" and ", text_type_enum.type_text),
                TextNode("another link", text_type_enum.type_link, "https://blog.boot.dev"),
                TextNode(" with text that follows", text_type_enum.type_text),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()