from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, value:str="", tag:str|None = None, props:dict|None=None):
        super().__init__(value=value, tag=tag, props=props)

    def to_html(self):
        if not self.tag:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"""
            TAG={self.tag}
            VALUE={self.value}
            PROPS={self.props_to_html()}
        """

    
