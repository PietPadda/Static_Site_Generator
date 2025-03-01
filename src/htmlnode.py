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


# child class of HTMLNode, "leaf"
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


# child class of HTMLNode, "parent"
# handles nesting of HTML nodes inside one another ie has children, has NO value
# has children, ag and children are not optional
# doesn't take a value, props are optional
# exact OPPOSITE of LeafNode
class ParentNode(HTMLNode):
    def __init__ (self, tag, children, props=None):  # we don't add value so don't include, props not "required" so def=None
        super().__init__(tag=tag, value=None, children=children, props=props)  # inherit from parent (set value=value to allow positional ordering)
    
    # recursion to print html tag of node & children, returns str
    def to_html(self):  # no args here except self
        if self.tag == None:  # if no tag
            raise ValueError("All parent nodes must have a tag!")  # raise error
        if self.children == None:  # if there's no child
            raise ValueError("All parent nodes must have a child!")  # raise error
        # otherwise, render HTML tag of node and children
        # recursive, each time called on a nested child node
        # use for loop to get the children (recursion happens in calling the func on each child)
        children_html = ""  # init our starting string
        for child in self.children:  # our children loop... to get each child
            children_html += child.to_html()  # RECURSIVE STEP! 
        # this adds the str to ALL parents, only leaf nodes are not recursed


        # Return parent tag wrapped around children's HTML
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"  # func we made in HTMLNode
        
        # sample output: 
# <p>
#   <b>Bold text</b>
#   Normal text
#   <i>italic text</i>
#   Normal text
# </p>
        # f"<{self.tag}{self.props_to_html()}> == <p> --> parent tag + props (optional, sample is None)
        # {children_html} == <b>Bold text</b>Normal text<i>italic text</i>Normal text --> all child HTML content, recursively generated
        # </{self.tag}>" == </p> --> final parent tag (no props here... props only appear at start of tag, not end)



