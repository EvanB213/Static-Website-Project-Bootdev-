import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("h", "This is an HTML node", [], {"href": "https://www.google.com", "target": "_blank",})
        test_str = node.props_to_html()
        self.assertEqual(test_str, ' href=https://www.google.com target=_blank')

    def test_no_val(self):
        node = HTMLNode("h", None, [], {"href": "https://www.google.com", "target": "_blank",})
        test_str = node.props_to_html()
        self.assertEqual(test_str, ' href=https://www.google.com target=_blank')

    def test_no_child(self):
        node = HTMLNode("h", "This is an HTML node", None, {"href": "https://www.google.com", "target": "_blank",})
        test_str = node.props_to_html()
        self.assertEqual(test_str, ' href=https://www.google.com target=_blank')

    def test_no_props(self):
        node = HTMLNode("h", "This is an HTML node", [], None)
        test_str = node.props_to_html()
        self.assertEqual(test_str, '')

    def test_values(self):
        node = HTMLNode("div", "I wish I could read",)
        self.assertEqual(node.tag, "div",)
        self.assertEqual(node.value, "I wish I could read",)
        self.assertEqual(node.children, None,)
        self.assertEqual(node.props,None,)
    
    def test_repr(self):
        node = HTMLNode("div", "testing a thing", None, {"class": "primary"},)
        self.assertEqual(node.__repr__(), "HTMLNode - Tag: div, Value: testing a thing, Children: None, Props: {'class': 'primary'}")

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("h", "This is an HTML node", {"href": "https://www.google.com",})
        test_str = node.to_html()
        self.assertEqual(test_str, '<h href=https://www.google.com>This is an HTML node</h>')

    def test_no_link(self):
        node = LeafNode("h", "This is an HTML node",)
        test_str = node.to_html()
        self.assertEqual(test_str, '<h>This is an HTML node</h>')

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_repr(self):
        node = LeafNode("div", "testing a thing", {"class": "primary"},)
        self.assertEqual(node.__repr__(), "LeafNode - Tag: div, Value: testing a thing, Props: {'class': 'primary'}")

if __name__ == "__main__":
    unittest.main()