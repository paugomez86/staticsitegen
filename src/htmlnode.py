# HTMLNode objects represent nodes containing the required data to inject html elements in the DOM.
# As the DOM may have nested elements, nodes may have another children nodes.
# Props are values that will become attributes of the html element.

SELF_CLOSING_TAGS = ["img"]

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        if self.tag in SELF_CLOSING_TAGS:
            self.self_closing = True
        else:
            self.self_closing = False
        
    def to_html(self):
            raise NotImplementedError
        
    def props_to_html(self):
        result = ""
        if self.props is not None and len(self.props) != 0:
            for key, value in self.props.items():
                result += f' {key}="{value}"'
        return result
        
    def __repr__(self):
        if self.children is not None and len(self.children) != 0:
            children = f" {self.children} "
        else:
            children = ""
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

# LeafNode objects represent the nodes that don't have children. They are the innermost in the DOM.
# self.to_html() returns the html code to be injected into the DOM.
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value is None and self.self_closing == False:
            raise ValueError("value is None")
        if self.tag is None:
            return f"{self.value}"
        if self.self_closing == True:
            return f"<{self.tag}{self.props_to_html()}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

# ParentNode objects represent nodes with children.
# self.to_html() calls the same method of its children recursively to build and return a single html format string.
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is None")
        if self.children is None:
            raise ValueError("invalid children")
        html = f"<{self.tag}>"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html