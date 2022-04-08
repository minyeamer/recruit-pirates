from saramin import Saramin
from jobkorea import Jobkorea
from wanted import Wanted

# for debugging
import pandas as pd

class Person(object):
    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address


class Client(Person):
    def __init__(self, name: str, address: str, requires: dict):
        super().__init__(name, address)
        self.requires = requires
        self.contents = {'saramin': None, 'jobkorea': None, 'wanted': None}
        # 실제 서비스에 적용한다면 사용자의 요구사항을 DB에 저장해서 데이터 관리


    def request_contents(self):
        requires = self.requires

        saramin_client = Saramin(requires)
        self.contents = saramin_client.get_content()

        if not requires['companies']:
            requires['companies'] = list(self.contents.keys())

        if 'Y' == requires['assay']:
            jobkorea_client = Jobkorea(requires)
            jobkorea_content = jobkorea_client.get_content()
            for company, assay in jobkorea_content.items():
                self.contents[company]['assay'] = assay
        
        if 'Y' in requires['skill']:
            wanted_client = Wanted(requires)
            wanted_content = wanted_client.get_content()
            for company, skill in wanted_content.items():
                self.contents[company]['skill'] = skill


    def send_mail(self):
        # 메일 보내는 코드
        pass


    # for debugging
    def get_dataframe(self):
        contents = self.contents
        columns = list(list(contents.values())[0].keys())
        rows = list(contents.keys())
        df = pd.DataFrame(columns=columns, index=rows)
        for company, content in contents.items():
            df.loc[company] = content
        df.index.name = 'company_name'
        df = df.fillna('')
        return df
