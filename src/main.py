from textnode import TextNode

def main():
    node = TextNode("dummy text", "bold")
    node2 = TextNode("This is a text node", "italic","https://www.boot.dev")
    print(node)
    print(node2)

main()