import requests
from bs4 import BeautifulSoup
import time
from content.content import Content

class Jobkorea(Content):
    """
    잡코리아에 회사에 대한 합격자소서 정보를 요청하고 결과를 저장하는 잡코리아 객체
    회사 이름을 바탕으로 잡코리아를 크롤링해서 합격자소서 문자열 리스트를 반환
    """

    def request_contents(self):
        self.service_url = 'https://www.jobkorea.co.kr'

        for company in self.requires['companies']:
            self.contents[company] = dict()
            
            try:
                self.company = company
                company_id = self.get_company_id()
                self.assay_url = self.service_url + \
                                 f'/company/{company_id}/PassAssay'
                self.contents[company] = self.request_assay()
            except Exception as e:
                # 각각의 경고 메시지 로그에 기록하는 부분 생략
                print(e)
                pass


    def get_company_id(self) -> str:
        search_url = self.service_url + '/Search/'
        self.params['stext'] = self.company
        self.params['tabType'] = 'corp'

        response = requests.get(url=search_url,    \
                                params=self.params)
        source = BeautifulSoup(response.content, 'html.parser')
        time.sleep(0.5)

        try:
            corp_info = source.find('div', {'class': 'corp-info'})
            corp_list = corp_info.find('li', {'class': 'list-post'})
            corp_name = corp_list.find('a', {'class': 'name'})
        except AttributeError:
            raise Exception(f'잡코리아에서 {self.company}의 회사 페이지가 존재하지 않습니다.')

        return corp_name.get('href').replace('/company/', '')


    def request_assay(self) -> dict:
        assay_section = self.request_assay_section()

        # 회사별 합격자소서 최대 표시 개수, 향후 해당 부분 입력 구문 구현
        assay_count = self.get_assay_count(assay_section, 3)
        if assay_count <= 10:
            assay_numbers = self.get_assay_numbers(assay_section, assay_count)
        else:
            assay_numbers = self.get_assay_numbers_multipages(assay_count)

        return self.get_assay_dict(assay_numbers)


    def request_assay_section(self, page_number=1) -> BeautifulSoup:
        assay_url = self.assay_url + f'?Page={str(page_number)}'
        response = requests.get(assay_url)
        source = BeautifulSoup(response.content, 'html.parser')
        assay_section = source.find('section', {'class': 'assayCont'})
        time.sleep(0.5)

        if not assay_section:
            raise Exception(f'{self.company}의 합격자소서가 존재하지 않습니다.')

        return assay_section


    def get_assay_count(self, assay_section: BeautifulSoup, assay_count: int) -> int:
        view_tabs = assay_section.find('div', {'class': 'viewTabs'})
        passassay_max_count = view_tabs.find('span').get_text()
        passassay_max_count = passassay_max_count.replace('(', '')
        passassay_max_count = passassay_max_count.replace(')', '')

        return min([assay_count, int(passassay_max_count)])


    def get_assay_numbers(self, assay_section: BeautifulSoup, assay_count=0) -> list:
        assay_numbers = list()

        assay_div = assay_section.find('div', {'class': 'passassayCont'})
        assay_list = assay_div.find_all('li', {'class': 'assay'})

        for assay in assay_list:
            assay_url = assay.find('a').get('href').split('&Part_Code=')[0]
            assay_number = assay_url.split('Job_Epil_No=')[1]
            assay_numbers.append(assay_number)

        return assay_numbers[:assay_count] if assay_count else assay_numbers


    def get_assay_numbers_multipages(self, assay_count: int) -> list:
        start_page = 1
        max_page = (assay_count//10)+1
        assay_numbers = list()

        for current_page in range(start_page, max_page+1):
            assay_section = self.request_assay_section(current_page)
            assay_numbers += self.get_assay_numbers(assay_section)

        return assay_numbers[:assay_count]


    def get_assay_dict(self, assay_numbers: list) -> dict:
        assay_dict = dict()        

        for assay_number in assay_numbers:
            assay_detail_url = self.assay_url + \
                               f'/View?Job_Epil_No={assay_number}'
            
            response = requests.get(assay_detail_url)
            source = BeautifulSoup(response.content, 'html.parser')
            detail_view = source.find('article', {'class': 'detailView'})
            time.sleep(0.5)

            assay_detail_dict = dict()
            assay_detail_dict['number'] = assay_number
            assay_detail_dict['advice'] = self.get_assay_advice(detail_view)
            assay_detail_dict.update(self.get_assay_qna(detail_view))

            title = detail_view.find('h2').get_text()
            assay_dict[title] = assay_detail_dict
        
        return assay_dict


    def get_assay_advice(self, detail_view: BeautifulSoup) -> str:
        advice_div = detail_view.find('div', {'class': 'adviceTotal'})

        if not advice_div:
            return ''

        advice_lines = advice_div.find('p', {'class': 'tx'}).get_text().strip()
        advice_lines = advice_lines.replace('\r\n\r\n', ' ')
        advice_lines = advice_lines.replace('.  ', '. ')

        advice_grade = advice_div.find('span', {'class': 'grade'}).get_text().strip()
        advice_lines = f'{advice_grade}점: ' + advice_lines
        
        return advice_lines


    def get_assay_qna(self, detail_view: BeautifulSoup) -> dict:
        qna_dict = {'index': list()}
        qna_div = detail_view.find('dl',{'class':'qnaLists'})

        indexes = qna_div.find_all('span',{'class':'num'})
        questions = qna_div.find_all('span',{'class':'tx'})
        answers = qna_div.find_all('div',{'class':'tx'})
        qna_zip = zip(indexes, questions, answers)

        for index, question, answer in qna_zip:
            index = index.get_text()
            question = question.get_text()
            answer = answer.get_text().replace('\r\n\r\n', ' ')
            answer = answer.replace('\r', '')
            answer = answer.replace('\n', '')
            answer = answer.split('글자수')[0].strip()
            answer = answer.split('아쉬운점')[0].strip()
            answer = answer.split('좋은점')[0].strip()

            qna_dict['index'].append(index)
            qna_dict[index] = (question, answer)
        
        return qna_dict
