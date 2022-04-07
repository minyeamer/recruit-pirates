from saramin import *
from jobkorea import *
from wanted import *

class Person(object):
    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address


class Admin(Person):
    def __init__(self, name: str, address: str, service_info: dict):
        super().__init__(name, address)
        self.service_key = service_info['key']
        self.service_url = service_info['url']


class Client(Person):
    def __init__(self, name: str, address: str, requires: dict):
        super().__init__(name, address)
        self.requires = requires
        self.contents = {'saramin': None, 'jobkorea': None, 'wanted': None}
    
    def request_contents(self):
        requires = self.requires

        saramin_client = Saramin(requires)
        self.contents['saramin'] = saramin_client.get_content()

        if not requires['companies']:
            requires['companies'] = self.contents['saramin'].keys()

        if requires['assay']:
            jobkorea_client = Jobkorea(requires)
            self.contents['jobkorea'] = jobkorea_client.get_content()
        
        if requires['skill'] or requires['skill_map']:
            wanted_client = Wanted(requires)
            self.contents['wanted'] = Wanted(wanted_client)

    def send_mail(self):
        # 메일 보내는 코드
        pass


"""
[참고사항]

클라이언트 요청 사항을 종합한 딕셔너리
requires {
    'locations': 희망 지역 리스트
    'jobs': 희망 직업 리스트
    'assay': 자기소개서 포함 여부 (True/False) -> 잡코리아 연결
    'skill': 기술 역량 포함 여부 (True/False) -> 원티드 연결
    'skill_map': 조건에 맞는 전체 기술 역량의 워드 클라우드 포함 여부 (True/False) -> 원티드 연결
    'count': 보여줄 채용공고 개수 (기본값: 5, 최대값: 110)
    'code_map': 지역, 직업 파라미터 코드 딕셔너리
    ('companies': 클라이언트가 지정한 특정 회사 목록,
                  없을 경우 사람인 API에서 가져온 회사명 목록으로 대체,
                  잡코리아 및 원티드에서 사용)
}

사람인 API 반환값 json을 정리한 딕셔너리
saramin_client {
    'company': 회사 이름 {
        'href': 회사 페이지 주소
        'id': 채용 공고 id (파라미터로 사용해 채용공고 페이지 이동 가능)
        'title': 채용 공고 제목
        'industry': 채용 공고의 서비스 분야 (SI, 게임 등)
        'location': 직장 위치
        'job_type': 정규직 등
        'exp': 요구 경력
        'edu': 요구 학력
        'keyword': 채용 공고 키워드
        'salary': 연봉 구간
        'opening_date': 채용 공고가 올라온 날짜
        'expiration_date': 채용이 끝나는 날짜
        'dday': 채용 종료까지 남은 일자
        'close-type': 마감일 형식 (접수 마감일, 상시 등)
        'jobkorea': 자소서
    }
}

"""
