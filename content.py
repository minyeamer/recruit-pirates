class Content:
    def __init__(self, requires: dict):
        self.requires = requires
        self.headers = dict()
        self.params = dict()
        self.content = dict()
    
    def get_content(self) -> dict:
        return self.content
