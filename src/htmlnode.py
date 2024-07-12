class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self) -> str:
        if self.props == None:
            return ""
        print_string = ""
        for key, value in self.props.items():
            print_string = print_string + " " + key + "=" + value
        return print_string
    
    def __repr__(self) -> str:
        return f"HTMLNode - Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("Leaf node must have value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"LeafNode - Tag: {self.tag}, Value: {self.value}, Props: {self.props}"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent node must have tag")
        if self.children == None:
            raise ValueError("Parent node must have children")
        print_string = f"<{self.tag}{self.props_to_html()}>"
        for elem in self.children:
            print_string += elem.to_html()
        print_string += f"</{self.tag}>"
        return print_string
    
    def __repr__(self) -> str:
        return f"ParentNode - Tag: {self.tag}, Children: {self.children}, Props: {self.props}"
