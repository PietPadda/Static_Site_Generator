class HTMLNode:
    # make all default=None
    # no tag = raw text, no value has children, no children has value, no props has no attributes
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag   # str for HTML tag name (p, a, h1 etc)
        self.value = value  # str for HTML tag value (eg text in paragrph)
        self.children = children  # list of HTMLNode objs for children of this node
        self.props = props  # dict key:value pairs of attributes of HTML tag (eg <a> may have {"href": "https://www.google.com"})

    # just raises error --> children will override to render as HTML
    def to_html(self):
        raise NotImplementedError
    
    # returns str of HTML attributes for node
    def props_to_html(self):  # only self, no props!
        if self.props == None:  # if default None
            return ""  # return empty str
        prop_str = ""  # init str
        for prop in self.props:  # loop through
            prop_str += " " + f'{prop}="{self.props[prop]}"'  # leading space + atr name + eq + quoted value
        return prop_str  # return st
        
        # sample output: " href="https://www.google.com" target="_blank"
        # 1st iter: " " + f'{prop}="{self.props[prop]}' --> " href="https://www.google.com"
        # 2nd iter: " " + f'{prop}="{self.props[prop]}' --> " href="https://www.google.com" target="_blank"
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):  # if not same type
            return False  # return false
        # checks if all properties of two TextNode objects are equal
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        return False
    
    # debugging printout of all 4 data members for debugging
    def __repr__(self, tag, value, children, props):
        print(f"Tag: {self.tag}\nValue: {self.value}\nChildren: {self.children}\nProps: {self.props}")


# child class of HTMLNode
# represent single HTML tag with no children ie has a value
# no children, don't init children, set super=None
# props not required, set default=None
class LeafNode(HTMLNode):
    def __init__ (self, tag, value, props=None):  # we don't add children so don't include, props not "required" so def=None
        super().__init__(tag=tag, value=value, children=None, props=props)  # inherit from parent (set value=value to allow positional ordering)
    
    # renders leaf node as HTML str, returns str
    def to_html(self):  # no args here except self
        if self.value == None:  # if no value
            raise ValueError("All leaf nodes must have a value!")  # raise error
        if self.tag == None:  # if there's no tag
            return self.value  # return raw text str
        # otherwise, render HTML tag
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"  # func we made in HTMLNode
        
        # sample output: "<a href="https://www.google.com">Click me!</a>"
        # "<{self.tag} ~ "<a
        # {self.props_to_html()}>=  " href="https://www.google.com>
        # {self.value} = Click me!
        # </{self.tag}>" = </a>"



