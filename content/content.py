import pandas as pd
import content.html


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
        try:
            self.request_saramin_contents()

            if not self.requires['companies']:
                self.requires['companies'] = list(self.contents.keys())

            if self.requires['assay']:
                self.request_jobkorea_contents()

            if self.requires['skill']:
                self.request_wanted_contents()

        except Exception as e:
            print('채용공고 정보를 받아오지 못했습니다.')
            print(e)


    def request_saramin_contents(self):
        from content.saramin import Saramin
        saramin_client = Saramin(self.requires)
        saramin_client.request_contents()
        self.contents = saramin_client.get_contents()


    def request_jobkorea_contents(self):
        from content.jobkorea import Jobkorea
        jobkorea_client = Jobkorea(self.requires)
        jobkorea_client.request_contents()
        jobkorea_content = jobkorea_client.get_contents()
        for company, assay in jobkorea_content.items():
            self.contents[company]['잡코리아 제공 합격자소서'] = assay


    def request_wanted_contents(self):
        from content.wanted import Wanted
        wanted_client = Wanted(self.requires)
        wanted_client.request_contents()
        wanted_content = wanted_client.get_contents()
        for company, skill in wanted_content.items():
            self.contents[company]['원티드 제공 기술역량'] = skill


    def set_headers(self):
        pass


    def set_params(self):
        pass


    def get_contents(self) -> dict:
        return self.contents


    def get_html(self) -> list:
        html = content.html.get_html(self.contents)

        if not html:
            return ['<hr><div><h2>현재 조건에 맞는 채용공고가 없습니다.</h2></div>']
        else:
            return html


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
