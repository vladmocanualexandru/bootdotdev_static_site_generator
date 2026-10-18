from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag:str, children:list, props:dict|None=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):

        children_str=""

        for child in self.children:
            children_str+=child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_str}</{self.tag}>"

    
    def __repr__(self):
        return f"""
        TAG={self.tag}
        CHILDREN={len(self.children) if self.children!=None else 'None'}
        PROPS={self.props_to_html()}
        """

    
