

class MY_SVG_TAG_BUILDER():
    def __init__(self, name: str, attributes= {},  children= []) -> None:
        self.name = name
        self.attributes = attributes
        self.children = children

    def __str__(self) -> str:
        def attr_func (key: str):
            value = str(self.attributes[key]) 
            if not bool(value) or len(value) <= 0:
                return key
            else: return f'{key}="{value}"'

        if len(self.attributes) > 0:
            left_side = f"<{self.name} {' '.join(map(attr_func,self.attributes))}"
        else: left_side = f"<{self.name}"

        if len (self.children) == 0:
            return left_side + "/>"
        
        left_side += ">" # Close tag

        right_side = f"</{self.name}>"
           

        return left_side + "".join(map(str,self.children)) + right_side
    
