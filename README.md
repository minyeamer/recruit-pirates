# Recruit Pirates
- 사람인, 잡코리아, 원티드로부터 채용 정보를 받아오는 서비스
- 클라이언트 별로 종합한 정보들을 HTML 형식으로 변환해 메일로 전송

---

## Index
  1.  [How to Use](#1-how-to-use)
  2.  [Team Members](#2-team-members)
  3.  [Implementation](#3-implementation)
  4.  [Main Classes](#4-main-classes)
  5.  [Main Functions](#5-main-functions)
  6.  [Client Request](#6-client-request)
  7.  [Contents](#7-contents)
  8.  [Saramin Contents](#8-saramin-contents)
  9.  [Jobkorea Contents](#9-jobkorea-contents)
  10. [Wanted Contents](#10-wanted-contents)

---

## 1. How to Use
- 실제 서비스를 위해선 웹과 연동해야겠지만, 현재는 `run.py` 위에서 직접 값을 넣어 실행
- 관리자 정보 및 API 키는 개인정보 보호를 위해 제외, 해당 부분에 본인 정보 입력
- 관리자 객체 생성 > 클라이언트 객체 생성 > 채용공고 요청 > 메일 전송 순으로 실행 요망
- 관리자 객체의 메일 주소를 발신자 주소로, 클라이언트 객체의 메일 주소를 수신자 주소로 설정

---

## 2. Team Members
- KMY: 아키텍처 설계, 사람인 채용공고 수집 프로세스 개발, 메일링 기능 개발
- KJW: `Selenium`을 활용한 원티드 크롤링 기능 구현
- LDG: 프로젝트 매니저, 연봉 지도 시각화 시도
- JMJ: `BeautifulSoup`을 활용한 잡코리아 크롤링 기능 구현

---

## 3. Implementation

### Languages:
- Python 3.9.10

### IDE:
- Visual Studio Code
- Jupyter Notebook

### Libraries:
- bs4 0.0.1
- pandas 1.4.1
- requests 2.27.1
- selenium 4.3.1
- webdriver-manager 3.5.4

---

## 4. Main Classes
- `Admin(Person)`: 클라이언트를 관리하고 메일을 보내는 객체
- `Client(Person, Content)`: 컨텐츠(=채용공고)를 요청하고 저장하는 객체
- `Content()`: 채용정보를 요청하고 반환하는 기능을 갖고 있는 부모 객체
- `Saramin(Content)`: 사람인 API를 통해 채용공고를 수집하고 반환하는 객체
- `Jobkorea(Content)`: 잡코리아 크롤링을 통해 합격자소서를 수집하고 반환하는 객체
- `Wanted(Content)`: 원티드 크롤링을 통해 기술역량을 수집하고 반환하는 객체

---

## 5. Main Functions
- `request`로 시작하는 클래스 내장 함수들은 주로 웹을 통해 데이터를 수집하거나   
  전체적인 크롤링 프로세스를 지휘하는 역할
- `Content()`에서 `request_contents()`가 `main()` 함수 같은 역할 수행,   
  각각의 객체별 역할에 따라 제한된 채용공고 데이터를 요청하는 함수
- `get`으로 시작하는 클래스 내장 함수들은 가져온 데이터를 가공하는 역할 (예외 있음)
- `Admin()`의 `send_mail()`은 `SMTP`를 사용해 메일을 전송하는 함수,   
  메일을 전송하는 과정에서 `Client(Content)`의 `get_html()`을 요청
- `Content()`의 `get_html()`은 컨텐츠(딕셔너리)를 HTML 형식으로 변환하는 역할,   
  `Content()`안에 있던 `get_html()`이 구현 중 길어져 `content.html.py`로 분리,   
  어떠한 딕셔너리를 넣어도 같은 결과를 만들기 위해 딕셔너리의 Depth를 고려한 재귀함수 사용

---

## 6. Client Request

```python
requires = {
    'locations': '희망 지역 리스트',
    'jobs': '희망 직업 리스트',
    'assay': '자기소개서 포함 여부 (Y/N)',                             # 잡코리아 연결
    'skill': '기술 역량 포함 여부 (Y/N)',                              # 원티드 연결
    'skill_map': '조건에 맞는 전체 기술 역량의 워드 클라우드 포함 여부 (Y/N)', # 원티드 연결
    'salary_map': '지역별 연봉 지도 포함 여부 (Y/N)',
    'count': '보여줄 채용공고 개수 (기본값: 5, 최대값: 110)',
    'code_map': '지역, 직업 파라미터 코드 딕셔너리',
    'companies': """클라이언트가 지정한 특정 회사 (생략 가능),
                    없을 경우 사람인 API에서 가져온 회사명 목록으로 대체,
                    잡코리아 및 원티드에서 검색 키워드로 사용)"""
}
```

---

## 7. Contents

```python
content.contents = {
    '회사명': {
        '회사 주소': ('사람인 회사 페이지 바로가기', {company_url}),
        '채용공고 제목': ({title}, {position_url}),
        ...
        '잡코리아 제공 합격자소서': {
            '합격자소서 번호': {
                '합격자소서 제목': ({title}, {url}),
                ...
            }, ...
        },
        '원티드 제공 기술역량': {
            '채용공고 번호': {
                '직무': ({title}, {url}),
                ...
            }, ...
        },
    }, ...
}
```

---

## 8. Saramin Contents

```python
saramin.contents = {
    '회사명': {
        '회사 주소': ('사람인 회사 페이지 바로가기', {company_url}),
        '채용공고 제목': ({title}, {position_url}),
        '업종': {industry},
        '지역': {location},
        '근무형태': {job-type},
        '경력': {experience-level},
        '학력': {required-education-level},
        '직무 키워드': {keyword},
        '연봉': {salary},
        '접수 시작일': {opening_date},
        '접수 마감일': {expiration_date},
        'D-Day': {expiration_date - today},
        '마감일 형식': {close-type},
        '연봉 지도': '특정 지역에 관한 연봉 맵 (folium.Map 타입)' # 현재 미구현
    }, ...
}
```

---

## 9. Jobkorea Contents

```python
jobkorea.contents = {
    '회사명': {
        '합격자소서 번호': {
            '합격자소서 제목': ({title}, {url})
            '전문가 자소서 총평': {advice_lines}
            '자소서 항목': {index},
            '질문': {answer}, ...
        }, ...
    }, ...
}
```

---

## 10. Wanted Contents

```python
wanted.contents = {
    '회사명': {
        '채용공고 번호': {
            '직무': ({title}, {url})
            '주요업무': {tasks}
            '자격요건': {attributes}
            '우대사항': {benefits}
        }, ...
    }, ...
}
```
