import smtplib
from email.mime.text import MIMEText
from saramin import Saramin
from jobkorea import Jobkorea
from wanted import Wanted
import pandas as pd


class Person(object):
    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address


"""
이름, 메일주소, 요구사항, 컨텐츠를 가지고 있는 클라이언트 객체
요구사항을 만족하는 채용공고 정보를 구직 사이트로부터 수집해 컨텐츠로 저장
사람인 채용공고 정보를 기반으로 잡코리아와 원티드에서 가져온 부가 정보를 추가
"""
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
    

    def get_html(self):
        pass


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


"""
이름, 메일주소, 메일비밀번호를 가지고 있는 서비스 관리자 객체
클라이언트 집합을 관리하며 단일 또는 전체 클라이언트에게 메일을 전송하는 역할
현재 버전에서 관리자는 Gmail 메일 서버만 사용 가능
"""
class Admin(Person):
    def __init__(self, name: str, address: str, password: str):
        super().__init__(name, address)
        self.password = password
        self.clients = set()
    

    def send_all(self):
        for client in self.clients:
            self.send_mail(client)


    def send_mail(self, clients=list()):
        clients =  list(self.clients) if not client else [client]

        SMTP_SERVER = 'smtp.gmail.com'
        SMTP_PORT = '465'

        smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        smtp.starttls()
        smtp.login(self.address, self.password)

        for client in clients:
            body = client.get_html()

            msg = MIMEText('내용')
            msg['Subject'] = '제목'

            smtp.sendmail(self.address, client.address, msg)

        smtp.quit()


    def add_client(self, client: Client):
        self.clients.add(client)


    def remove_client(self, client: Client):
        self.clients.discard(client)
