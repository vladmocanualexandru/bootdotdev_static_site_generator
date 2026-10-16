class HTMLNode:
    def __init__(self, tag:str|None = None, value:str|None = None, children:list|None = None, props:dict|None=None):
        self.tag=tag
        self.value=value
        self.children=children
        self.props=props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if not self.props:
            return ""

        return "".join([f' {key}="{value}"' for key, value in self.props.items()])

    def __repr__(self):
        return f"""
        TAG={self.tag}
        VALUE={self.value}
        CHILDREN={len(self.children) if self.children!=None else 'None'}
        PROPS={self.props_to_html()}
        """
