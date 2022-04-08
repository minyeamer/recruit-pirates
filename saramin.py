import requests
import json
from datetime import date
from content import Content
from admin import get_saramin_key


class Saramin(Content):
    def __init__(self, requires: dict):
        super().__init__(requires)
        self.service_key = get_saramin_key()
        self.service_url = 'https://oapi.saramin.co.kr/job-search'
        self.service_response = None


    def get_content(self) -> dict:
        self.set_headers()
        self.set_params()
        self.request_json()
        self.make_content()
        return self.content


    def set_headers(self):
        self.headers['Accept'] = 'application/json'


    def set_params(self):
        requires = self.requires
        locations = requires['locations']
        jobs = requires['jobs']
        loc_dict = requires['code_map']['saramin_loc']
        job_dict = requires['code_map']['saramin_job']

        loc_list = self.match_code_map(locations, loc_dict)
        job_list = self.match_code_map(jobs, job_dict)

        fields = {'posting-date', 'expiration-date', 'keyword-code', 'count'}

        self.params['access-key'] = self.service_key
        self.params['loc_cd'] = ','.join(loc_list)
        self.params['job_cd'] = ','.join(job_list)
        self.params['fields'] = fields
        self.params['sr'] = 'directhire'
        self.params['count'] = requires['count']


    def match_code_map(self, texts: list, codes: dict) -> list:
        code_keys = codes.keys()
        return [ str(codes[text]) if text in code_keys else '' for text in texts ]


    def request_json(self):
        response = requests.get(url=self.service_url, \
                                headers=self.headers, \
                                params=self.params)

        self.service_response = json.loads(response.content)


    def make_content(self):
        if not self.service_response:
            raise Exception('서버로부터 응답을 받지 못했습니다.')

        recruits = self.service_response['jobs']['job']

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

            self.content[company['name'].replace('(주)', '')] = recruit_info
