import requests
import json
from client import *
from ..admin.info import get_saramin_key
from ..admin.info import get_saramin_url


class SaraminAdmin(Admin):
    __key = get_saramin_key()
    __url = get_saramin_url()
    __loc_dict = dict()
    __job_dict = dict()

    def set_loc_dict(self):
        # 사람인 API 문서 크롤링을 통해 지역코드 딕셔너리 생성
        self.__loc_dict['test'] = 123

    def set_job_dict(self):
        # 사람인 API 문서 크롤링을 통해 직업코드 딕셔너리 생성
        self.__job_dict['test'] = 123
    
    def get_loc_dict(self) -> dict:
        return self.__loc_dict
    
    def get_job_dict(self) -> dict:
        return self.__job_dict


class SaraminClient(Client):
    __headers = dict()
    __fields = set()
    __params = dict()
    __response = None
    
    def set_fields(self):
        self.__fields.add('posting-date')
        self.__fields.add('expiration-date')
        self.__fields.add('keyword-code')
        self.__fields.add('count')

    def set_params(self, locs: list, jobs: list, count: str):
        service_key = self.__server.get_service_key()
        loc_dict = self.__server.get_loc_dict()
        job_dict = self.__server.get_job_dict()

        loc_list = locs # text to code 전처리 함수
        job_list = jobs # text to code 전처리 함수

        self.__params['access_key'] = service_key
        self.__params['loc_cd'] = ','.join(loc_list)
        self.__params['job_cd'] = ','.join(job_list)
        self.__params['fields'] = self.__fields
        self.__params['sr'] = 'directhire'
        self.__params['count'] = count

    def request(self, type=''):
        url = self.__server.get_url()

        if type:
            self.__headers['Accept'] = f'application/{type}'

        response = requests.get(url, \
                                headers=self.__headers, \
                                params=self.__params)
        self.__response = response

    def get_json_response(self):
        if self.__response:
            return json.loads(self.__response.content)
    