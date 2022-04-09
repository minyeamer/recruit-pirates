import pandas as pd
from datetime import date


class Content:
    """
    구직 사이트들로부터 받은 컨텐츠들을 종합하고 반환하는 컨텐츠 객체
    필요에 따라 HTML, DataFrame 형태로도 컨텐츠 반환
    """

    def __init__(self, requires: dict):
        self.requires = requires
        self.headers = dict()
        self.params = dict()
        self.contents = dict()


    def request_contents(self):
        requires = self.requires

        try:
            from content.saramin import Saramin
            saramin_client = Saramin(requires)
            saramin_client.request_contents()
            self.contents = saramin_client.get_contents()

            if not requires['companies']:
                requires['companies'] = list(self.contents.keys())

            if requires['assay']:
                from content.jobkorea import Jobkorea
                jobkorea_client = Jobkorea(requires)
                jobkorea_client.request_contents()
                jobkorea_content = jobkorea_client.get_contents()
                for company, assay in jobkorea_content.items():
                    self.contents[company]['assay'] = assay

            if requires['skill']:
                from content.wanted import Wanted
                wanted_client = Wanted(requires)
                wanted_client.request_contents()
                wanted_content = wanted_client.get_content()
                for company, skill in wanted_content.items():
                    self.contents[company]['skill'] = skill

        except Exception as e:
            print('채용공고 정보를 받아오지 못했습니다.')
            print(e)


    def set_headers(self):
        pass


    def set_params(self):
        pass


    def get_contents(self) -> dict:
        return self.contents


    # HTML 디자인 개선 필요 :(
    def get_html(self, contents=None, body=list(), head=2) -> list:
        head = min(head, 6)

        if not contents:
            contents = self.contents

        for key, values in contents.items():
            if not values:
                continue

            body.append(f'<div id="{key}">')
            body.append(f'<h{head}>{key.capitalize()}</h{head}>')

            if key == 'assay':
                return self.get_assay_html(values, body, head)

            if type(values) is not dict:
                if type(values) in {int, date}:
                    body.append(f'<ul><li>{values}</li></ul>')
                if type(values) is str:
                    text = values.replace('. ', '.<br>')
                    body.append(f'<ul><li>{text}</li></ul>')
                elif type(values) in {list, tuple}:
                    body.append('<ul>')
                    for value in values:
                        text = value.replace('. ', '.<br>')
                        body.append(f'<li>{text}</li>')
                    body.append('</ul>')
                else:
                    pass # 미구현
            else:
                for key, value in values.items():
                    self.get_html({key: value}, body, head+1)
            body.append('</div>')

            if head < 3:
                body.append('<hr>')

        return body


    def get_assay_html(self, assay: dict, body: list, head: int):
        for title, details in assay.items():
            # Gmail에서 <details> 태그 미지원
            # 다른 방안을 찾을 때까지 blockquote 태그로 대체
            # body.append('<details>')
            # body.append(f'<summary>{title}</summary>')
            body.append('<blockquote>')
            body.append(f'<h{head}>{title}</h{head}>')
            for key, value in details.items():
                self.get_html({key: value}, body, head+1)
            # body.append('</details>')
            body.append('</blockquote>')


    def get_dataframe(self, index_name='index'):
        contents = self.contents
        columns = list(list(contents.values())[0].keys())
        rows = list(contents.keys())
        df = pd.DataFrame(columns=columns, index=rows)
        for index, content in contents.items():
            df.loc[index] = content
        df.index.name = index_name
        df = df.fillna('')
        return df
