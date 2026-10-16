from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, value:str, tag:str|None = None, props:dict|None=None):
        super().__init__(value=value, tag=tag, props=props)
