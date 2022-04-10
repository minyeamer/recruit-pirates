from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.service import Service 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from content.content import Content
import warnings
warnings.filterwarnings("ignore")


class Wanted(Content):
    """
    원티드에 회사별 채용공고에 대한 추가 정보를 요청하고 결과를 저장하는 원티드 객체
    회사 이름을 바탕으로 원티드 크롤링해서 기술역량 문자열 리스트를 반환
    """


    def request_contents(self) -> dict:
        self.service_url = 'https://www.wanted.co.kr/search'
        service = Service(executable_path=ChromeDriverManager().install()) 
        driver = webdriver.Chrome(service=service)

        for company in self.requires['companies']:
            self.contents[company] = dict()

            try:
                self.company = company
                self.company_url = self.service_url + f'?query={self.company}'
                position_count = self.get_position_count(driver)
                positions = self.request_positions(driver, position_count)
                self.contents[company] = positions
                
            except Exception as e:
                # 각각의 경고 메시지 로그에 기록하는 부분 생략
                print(e)
                pass
        
        driver.close()
        driver.quit()


    def get_position_count(self, driver: webdriver.Chrome) -> int:
        driver.get(self.company_url)
        self.wait_for_xpath(driver, '/html/body/div/div[4]')

        try:
            box_list = driver.find_element_by_xpath('/html/body/div/div[4]/div[2]')
            position_count = int(box_list.find_element_by_tag_name('span').text)

            if (not position_count) or (box_list.text.find('바로 지원할 곳이 없다면?') > -1):
                raise Exception(f'원티드에 {self.company}의 채용 중인 포지션이 없습니다.')
            
            return position_count
        except:
            raise Exception(f'원티드에 {self.company}의 회사 페이지가 존재하지 않습니다.')


    def request_positions(self, driver: webdriver.Chrome, position_count: int) -> dict:
        positions = dict()

        # 채용공고별 기술 역량 최대 표시 개수, 향후 해당 부분 입력 구문 구현 (기본값 5)
        position_count = min(position_count, 5)

        for i in range(position_count):
            if i > 0:
                driver.get(self.company_url)
                self.wait_for_xpath(driver, '/html/body/div/div[4]')

            try:
                driver.find_elements_by_class_name('job-card-position')[i].click()
                self.wait_for_xpath(driver, '/html/body/div/div[3]')
            except:
                continue

            position_id = driver.current_url.split('/wd/')[1]
            positions[position_id] = self.get_position_dict(driver)

        return positions


    def get_position_dict(self, driver: webdriver.Chrome) -> dict:
        position_dict = dict()

        content_xpath = '/html/body/div/div[3]/div[1]/div[1]/div'
        header_xpath = f'{content_xpath}/section[2]'
        description_xpath = f'{content_xpath}/div[2]/section'

        entire_text = driver.find_element_by_xpath(content_xpath).text
        # 클라이언트가 희망하는 직무와 관련된, 키워드 목록 생성 기능 개선 필요
        keywords = self.requires['jobs'] + ['AI', 'Data', '데이터', \
                        'ML', '머신러닝', '딥러닝', 'Deep Learning', 'Machine Learning']
        keywords_in = [ keyword in entire_text for keyword in keywords ]
        if True not in keywords_in:
            return position_dict

        title = driver.find_element_by_xpath(f'{header_xpath}/h2').text
        # description = driver.find_element_by_xpath(f'{description_xpath}/p[1]/span').text

        tasks = driver.find_element_by_xpath(f'{description_xpath}/p[2]/span').text
        tasks = tasks.replace('• ', '').split('\n')

        attributes = driver.find_element_by_xpath(f'{description_xpath}/p[3]/span').text
        attributes = attributes.replace('• ', '').split('\n')

        benefits = driver.find_element_by_xpath(f'{description_xpath}/p[4]/span').text
        benefits = benefits.replace('• ', '').split('\n')

        position_dict['직무'] = (title, driver.current_url)
        # position_dict[f'{self.company} 소개'] = description
        position_dict['주요업무'] = tasks
        position_dict['자격요건'] = attributes
        position_dict['우대사항'] = benefits

        return position_dict


    def wait_for_xpath(self, driver: webdriver.Chrome, xpath: str, delay=0.5):
        time.sleep(delay)
        accum_delay = delay

        while not driver.find_element_by_xpath(xpath).text:
            if accum_delay > 10:
                raise Exception('원티드에 페이지를 요청하는 과정에서 문제가 발생했습니다.')

            time.sleep(delay)

            accum_delay += delay
            delay += delay
