import requests
import json
import locale
from datetime import date
from content.content import Content
from content.api import get_saramin_key

class Saramin(Content):
    """
    사람인 API에 채용공고 정보를 요청하고 결과를 저장하는 사람인 객체
    사람인 API에서 받은 JSON 응답을 재해석해 딕셔너리로 변환
    """

    def request_contents(self):
        service_url = 'https://oapi.saramin.co.kr/job-search'
        self.set_headers()
        self.set_params()

        response = requests.get(url=service_url,      \
                                headers=self.headers, \
                                params=self.params)

        self.contents = json.loads(response.content)
        self.reformat_contents()

        # 실제 서비스 적용 시 'Y' 대신 True로 변환
        if 'Y' == self.requires['salary_map']:
            self.request_salary_map()


    def set_headers(self):
        self.headers['Accept'] = 'application/json'


    def set_params(self):
        requires = self.requires

        locations = requires['locations']
        jobs = requires['jobs']
        loc_dict = requires['codemap']['saramin_loc']
        job_dict = requires['codemap']['saramin_job']

        loc_list = self.match_codemap(locations, loc_dict)
        job_list = self.match_codemap(jobs, job_dict)

        fields = {'posting-date', 'expiration-date', 'keyword-code', 'count'}

        # content.api.get_saramin_key()는 개인정보 문제로 숨김 처리
        # 해당 부분에 본인의 사람인 API키 입력
        self.params['access-key'] = get_saramin_key()

        if requires['companies']:
            self.params['keywords'] = requires['companies'][0]

        self.params['loc_cd'] = ','.join(loc_list)
        self.params['job_cd'] = ','.join(job_list)
        self.params['fields'] = fields
        self.params['sr'] = 'directhire'
        self.params['count'] = requires['count']


    def reformat_contents(self):
        recruits = self.contents['jobs']['job']
        self.contents = dict()

        if not recruits:
            raise Exception('사람인에 조건에 맞는 채용공고가 없습니다.')

        for recruit in recruits:
            recruit_info = dict()
            locale.setlocale(locale.LC_ALL, 'ko_KR.UTF-8')

            position = recruit['position']
            position_url = recruit['url'].split('&')[0]

            company = recruit['company']['detail']
            company_id = company['href'].split('csn=')[1]
            company_id= company_id.split('&')[0]
            company_url = company['href'].split('&')[0]

            opening_date = int(recruit['opening-timestamp'])
            opening_date = date.fromtimestamp(opening_date)

            expiration_date = int(recruit['expiration-timestamp'])
            expiration_date = date.fromtimestamp(expiration_date)

            # recruit_info['회사 번호'] = company_id
            recruit_info['회사 주소'] = (f'사람인 회사 페이지 바로가기', company_url)
            # recruit_info['채용공고 글번호'] = recruit['id']
            recruit_info['채용공고 제목'] = (position['title'], position_url)
            recruit_info['업종'] = position['industry']['name']
            recruit_info['지역'] = position['location']['name']
            recruit_info['근무형태'] = position['job-type']['name']
            recruit_info['경력'] = position['experience-level']['name']
            recruit_info['학력'] = position['required-education-level']['name']
            recruit_info['직무 키워드'] = recruit['keyword']
            recruit_info['연봉'] = recruit['salary']['name']
            recruit_info['접수 시작일'] = opening_date.strftime('%Y년 %m월 %d일')
            recruit_info['접수 마감일'] = expiration_date.strftime('%Y년 %m월 %d일')
            recruit_info['D-Day'] = str((expiration_date - date.today()).days) + '일'
            recruit_info['마감일 형식'] = recruit['close-type']['name']

            self.contents[company['name'].replace('(주)', '')] = recruit_info


    def request_salary_map(self):
        pass


    def match_codemap(self, texts: list, codemap: dict) -> list:
        code_keys = codemap.keys()
        return [ str(codemap[text]) if text in code_keys else '' for text in texts ]
