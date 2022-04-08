from client import Client
from saramin import *
# from jobkorea import *
# from wanted import *
from code_map.get import *


def collect_requires() -> dict:
    requires = dict()

    requires['locations'] = input('희망하는 지역을 입력해주세요. ').split()
    requires['jobs'] = input('희망하는 직업을 입력해주세요. ').split()
    requires['assay'] = input('합격자소서 항목을 보시겠습니까? (Y/N) ')
    requires['skill'] = [input('기술역량 항목을 보시겠습니까? (Y/N) ')]
    # requires['skill'].append(input('기술역량 워드클라우드를 보시겠습니까? (Y/N)'))
    requires['count'] = input('검색할 채용공고 개수를 입력해주세요. (최대 110) ')
    requires['companies'] = input('희망하는 회사를 입력해주세요. (생략가능) ').split()
    requires['code_map'] = dict()
    requires['code_map'].update(get_saramin_loc('code_map/'))
    requires['code_map'].update(get_saramin_job('code_map/'))

    return requires


def main():
    name = input('이름을 입력해주세요. ')
    address = input('이메일 주소를 입력해주세요. ')
    requires = collect_requires()
    client = Client(name, address, requires)
    print(client.contents())


if __name__ == '__main__':
    main()


# for debugging
def debug_requires() -> dict:
    requires = dict()

    requires['locations'] = ['서울']
    requires['jobs'] = ['인공지능']
    requires['assay'] = 'N'
    requires['skill'] = 'N'
    requires['skill_map'] = 'N'
    requires['count'] = '10'
    requires['companies'] = ''
    requires['code_map'] = dict()
    requires['code_map'].update(get_saramin_loc('code_map/'))
    requires['code_map'].update(get_saramin_job('code_map/'))

    return requires

