class Content:
    def __init__(self, requires: dict):
        self.requires = requires
        self.content = dict()
        self.headers = dict()
        self.params = dict()
    
    def get_content(self) -> dict:
        return self.content
