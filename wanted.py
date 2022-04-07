from content import Content

class Wanted(Content):
    def __init__(self, requires: dict):
        super().__init___(requires)
        self.service_url = 'https://www.wanted.co.kr/search'

    def get_content(self) -> dict:
        return self.content