from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText
from datetime import date
from content.content import Content
from codemap.get import get_codemap


class Person(object):
    """
    개인정보를 가지고 있는 사람 객체
    """

    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address


class Admin(Person):
    """
    개인정보와 서비스 데이터를 가지고 있고 클라이언트 객체들을 관리하는 서비스 관리자 객체
    일부 또는 전체 클라이언트에게 메일을 전송하는 역할 수행
    현재 버전에서 관리자는 Gmail 메일 서버만 사용 가능
    """

    def __init__(self, name: str, address: str, password: str):
        super().__init__(name, address)
        self.password = password
        self.clients = set()
        self.codemap = get_codemap('codemap/')


    def send_mail(self, clients=list()):
        clients =  list(self.clients) if not clients else clients

        SMTP_SERVER = 'smtp.gmail.com'
        SMTP_PORT = '465'

        smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        smtp.starttls()
        smtp.login(self.address, self.password)

        for client in clients:
            print(f'Sending Mail To {client.address}')

            msg = MIMEMultipart('alternative')
            msg['Subject'] = f'[Recruits Pirates] {date.today()}'
            msg['From'] = self.address
            msg['To'] = client.address

            body = client.get_html()
            msg.attach(MIMEText(body, 'html'))

            smtp.send_message(msg)

        print('Successfully Completed :)')
        smtp.quit()


    def add_client(self, client):
        self.clients.add(client)


    def remove_client(self, client):
        self.clients.discard(client)


class Client(Person, Content):
    """
    개인정보와 요구사항을 가지고 있고 컨텐츠를 요청해서 받아오는 클라이언트 객체
    """

    def __init__(self, name: str, address: str, requires: dict, admin: Admin):
        Person.__init__(self, name, address)
        Content.__init__(self, requires)
        self.synchronize(admin)
        # 실제 서비스에 적용한다면 사용자의 요구사항을 DB에 저장해서 데이터 관리


    def synchronize(self, admin: Admin):
        admin.add_client(self)
        self.requires['codemap'] = admin.codemap
