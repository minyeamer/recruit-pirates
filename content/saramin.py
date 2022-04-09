import requests
import json
from datetime import date
from content.content import Content
from content.api import get_saramin_key


class Saramin(Content):
    """
    사람인 API에 채용공고 정보를 요청하고 결과를 저장하는 사람인 객체
    사람인 API에서 받은 JSON 응답을 재해석해 딕셔너리로 변환
    사람인 API 키는 개인정보 보호를 위해 숨김 처리, 필요 시 값 변경
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

        self.params['access-key'] = get_saramin_key()
        self.params['loc_cd'] = ','.join(loc_list)
        self.params['job_cd'] = ','.join(job_list)
        self.params['fields'] = fields
        self.params['sr'] = 'directhire'
        self.params['count'] = requires['count']


    def reformat_contents(self):
        if not self.contents:
            raise Exception('서버로부터 응답을 받지 못했습니다.')

        recruits = self.contents['jobs']['job']
        self.contents = dict()

        for recruit in recruits:
            recruit_info = dict()
            company = recruit['company']['detail']
            position = recruit['position']

            company_id = company['href'].split('csn=')[1]
            company_id= company_id.split('&')[0]

            opening_date = int(recruit['opening-timestamp'])
            opening_date = date.fromtimestamp(opening_date)

            expiration_date = int(recruit['expiration-timestamp'])
            expiration_date = date.fromtimestamp(expiration_date)

            recruit_info['company_id'] = company_id
            recruit_info['position_id'] = recruit['id']
            recruit_info['title'] = position['title']
            recruit_info['industry'] = position['industry']['name']
            recruit_info['location'] = position['location']['name']
            recruit_info['job_type'] = position['job-type']['name']
            recruit_info['exp'] = position['experience-level']['name']
            recruit_info['edu'] = position['required-education-level']['name']
            recruit_info['keyword'] = recruit['keyword']
            recruit_info['salary'] = recruit['salary']['name']
            recruit_info['opening_date'] = opening_date
            recruit_info['expiration_date'] = expiration_date
            recruit_info['dday'] = (expiration_date - date.today()).days
            recruit_info['close-type'] = recruit['close-type']['name']

            self.contents[company['name'].replace('(주)', '')] = recruit_info
    

    def request_salary_map(self):
        pass


    def match_codemap(self, texts: list, codemap: dict) -> list:
        code_keys = codemap.keys()
        return [ str(codemap[text]) if text in code_keys else '' for text in texts ]
