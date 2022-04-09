from admin import get_admin_info
from client import Admin, Client


def collect_requires() -> dict:
    """
    클라이언트의 요구사항을 수집하는 함수
    실제 서비스에선 Bootstrap의 Form 템플릿을 활용하기 때문에 입력값 검증 불필요
    코드맵과 맵핑해야 하는 지역 및 직업은 selectbox로 입력 처리
    True/False 입력값을 기대하는 키값들은 checkbox로 입력 처리
    """

    requires = dict()

    requires['locations'] = input('희망하는 지역을 입력해주세요. ').split()
    requires['jobs'] = input('희망하는 직업을 입력해주세요. ').split()
    requires['assay'] = input('합격자소서 항목을 보시겠습니까? (Y/N) ')
    requires['skill'] = [input('기술역량 항목을 보시겠습니까? (Y/N) ')]
    # requires['skill'].append(input('기술역량 워드클라우드를 보시겠습니까? (Y/N)'))
    requires['salary_map'] = input('지역별 연봉 지도를 보시겠습니까? (Y/N) ')
    requires['count'] = input('검색할 채용공고 개수를 입력해주세요. (최대 110) ')
    requires['companies'] = list(input('희망하는 회사를 입력해주세요. (생략가능) '))

    return requires


def make_client() -> Client:
    """
    클라이언트의 요청을 토대로 클라이언트 객체를 생성하고 반환하는 함수
    실제 서비스에선 Bootstrap의 Form 템플릿을 활용하기 때문에 입력값 검증 불필요
    웹페이지에서 입력을 받게 된다면 collect_requires() 함수 불필요
    """

    name = input('이름을 입력해주세요. ')
    address = input('이메일 주소를 입력해주세요. ')
    requires = collect_requires()
    return Client(name, address, requires)


def main():
    """
    메인 함수
    관리자 및 클라이언트 객체를 생성하고 클라이언트에게 메일을 일괄적으로 전송
    admin_info는 개인정보 보호를 위해 숨김 처리, 필요 시 값 변경
    """

    admin_info = get_admin_info()
    admin = Admin(admin_info[0], admin_info[1], admin_info[2])

    # 클라이언트 요청이 있으면
    if True:
        client = make_client()
        client.request_contents()


    # 메일 발송 이벤트가 생기면 (관리자의 수동 조작 또는 자동 실행 봇 등)
    if True:
        admin.send_mail()


if __name__ == '__main__':
    main()


def debug_requires() -> dict:
    """
    디버그용 함수
    input()을 거치지 않고 미리 지정된 클라이언트 요구사항을 반환
    """

    requires = dict()

    requires['locations'] = ['서울']
    requires['jobs'] = ['인공지능']
    requires['assay'] = 'Y'
    requires['skill'] = 'N'
    requires['skill_map'] = 'N'
    requires['salary_map'] = 'N'
    requires['count'] = '10'
    requires['companies'] = ['그린웹서비스']

    return requires
