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
    def props_to_html(self, props):
        if self.props == None:  # if default None
            return ""  # return empty str
        prop_str = ""  # init str
        for prop in self.props:  # loop through
            prop_str += " " + f'{prop}: "{self.props[prop]}"'  # leading space for HTML attributes
        return prop_str  # return st
    
    def __eq__(self, other):
        # checks if all properties of two TextNode objects are equal
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        return False
    
    # debugging printout of all 4 data members for debugging
    def __repr__(self, tag, value, children, props):
        print(f"Tag: {self.tag}\nValue: {self.value}\nChildren: {self.children}\nProps: {self.props}")
