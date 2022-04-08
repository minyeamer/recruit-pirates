from content import Content

class Jobkorea(Content):
    def __init__(self, requires: dict):
        super().__init___(requires)
        self.service_url = 'https://www.jobkorea.co.kr/Search'

    def get_content(self) -> dict:
        return self.content
    
    def set_params(self):
        pass