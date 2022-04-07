from content import Content
from admin_info import get_saramin_key

class Saramin(Content):
    def __init__(self, requires: dict):
        super().__init___(requires)
        self.service_key = get_saramin_key()
        self.service_url = 'https://oapi.saramin.co.kr/job-search'

    def get_content(self) -> dict:
        self.set_headers()
        self.set_params()

        return self.content

    def set_headers(self):
        self.headers['Accept'] = 'application/json'
    
    def set_params(self):
        requires = self.requires
        locations = requires['locations']
        jobs = requires['jobs']
        loc_dict = requires['code_map']['saramin_loc']
        job_dict = requires['code_map']['saramin_job']

        loc_list = self.map_locations(locations, loc_dict)
        job_list = self.map_jobs(jobs, job_dict)

        self.__params['access_key'] = self.service_key
        self.__params['loc_cd'] = ','.join(loc_list)
        self.__params['job_cd'] = ','.join(job_list)
        self.__params['fields'] = self.__fields
        self.__params['sr'] = 'directhire'
        self.__params['count'] = requires['count']
    
    def map_locations(self, locs: list, lmap: dict) -> list:
        loc_keys = lmap.keys()
        return[ lmap[loc] if loc in loc_keys else '' for loc in locs ]

    def map_jobs(self, jobs: list, jmap: dict) -> list:
        job_keys = jmap.keys()
        return[ jmap[job] if job in job_keys else '' for job in jobs ]
