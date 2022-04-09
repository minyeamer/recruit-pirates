import pandas as pd


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

            # 실제 서비스 적용 시 'Y' 대신 True로 변환
            if 'Y' == requires['assay']:
                from content.jobkorea import Jobkorea
                jobkorea_client = Jobkorea(requires)
                jobkorea_client.request_contents()
                jobkorea_content = jobkorea_client.get_contents()
                for company, assay in jobkorea_content.items():
                    self.contents[company]['assay'] = assay

            # 실제 서비스 적용 시 'Y' 대신 True로 변환
            if 'Y' in requires['skill']:
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


    def get_html_body(self) -> dict:
        return self.contents


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
