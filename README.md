# Recruit Pirates
  1. [Introduction](#1-introduction)
  2. [How to Use](#2-how-to-use)
  3. [Project Description](#3-project-description)
  4. [Implementation](#4-implementation)
  5. [Main Classes](#5-main-classes)
  6. [Main Methods](#6-main-methods)
  7. [Input/Output](#7-inputoutput)
  8. [Error List](#8-error-list)
  9. [Post-Project](#9-post-project)

---

## 1. Introduction
- 현대 사회는 플랫폼 시장의 활성화로 온라인 상에 이전과는 비교할 수 없을 수준의 많은 정보가 올라오지만,   
이와 동시에 플랫폼의 다양화로 인해 이전보다 더 많은 시간을 들이지 않으면 정보의 손실이 발생
- 구직 플랫폼 역시 마찬가지로 각자의 개성을 가지고 있는 다양한 플랫폼이 존재하지만,   
모든 회사가 모든 플랫폼을 활용하지는 않기 때문에 모든 채용공고를 확인함에 있어 불편함이 존재
- 여러 구직 플랫폼으로부터 채용공고를 수집해 요약된 정보를 메일로 알려주는 기능을 기대하고 있지만,   
짧은 프로젝트 기간에 맞춰 서비스를 완성시키기 위해 수집할 정보에 제한을 두고 진행
- 직종, 회사명을 키워드로 사람인에서 최신공고를 수집하고, 잡코리아와 원티드로부터 해당 공고와 관련된   
합격자소서, 기술역량 등의 정보를 추가해 메일로 전송하는 서비스 구현

<br>

![mail](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fb8Seh7%2Fbtry8PDYnMT%2FnDPQhDbrwhdWoyOHJkKko0%2Fimg.png)

---

## 2. How to Use
- 실제 서비스를 위해선 웹과 연동해야겠지만, 현재는 `run.py` 위에 직접 값을 넣어 실행
- 관리자 정보 및 API 키는 개인정보 보호를 위해 제외, 해당 부분에 본인 정보 입력
- 관리자 객체 생성 > 클라이언트 객체 생성 > 채용공고 요청 > 메일 전송 순으로 실행 요망
- 관리자 객체의 메일 주소를 발신자 주소로, 클라이언트 객체의 메일 주소를 수신자 주소로 설정

---

## 3. Project Description

### Team Name
> 해적왕 (The Pirate King)

### Team Members
- 김민엽: 아키텍처 설계, 사람인 채용공고 수집 기능 및 전반적인 조율 담당
- 김지원: `Selenium`을 활용한 원티드 크롤링 기능 구현
- 이동근: 프로젝트 매니저, 연봉 지도 시각화 시도
- 정민주: `BeautifulSoup`을 활용한 잡코리아 크롤링 기능 구현

### Project Period
> Start Date: 2022-04-06   
> End Date: 2022-04-10

---

## 4. Implementation

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

## 5. Main Classes
- `Admin(Person)`: 클라이언트를 관리하고 메일을 보내는 객체
- `Client(Person, Content)`: 컨텐츠(=채용공고)를 요청하고 저장하는 객체
- `Content()`: 채용정보를 요청하고 반환하는 기능을 갖고 있는 부모 객체
- `Saramin(Content)`: 사람인 API를 통해 채용공고를 수집하고 반환하는 객체
- `Jobkorea(Content)`: 잡코리아 크롤링을 통해 합격자소서를 수집하고 반환하는 객체
- `Wanted(Content)`: 원티드 크롤링을 통해 기술역량을 수집하고 반환하는 객체

---

## 6. Main Methods
- `request`로 시작하는 메소드는 주로 웹을 통해 데이터를 수집하거나   
  전체적인 크롤링 프로세스를 지휘하는 역할
- `Content()`에서 `request_contents()`가 `main()` 함수 같은 역할 수행,   
  각각의 객체별 역할에 따라 제한된 채용공고 데이터를 요청하는 메소드
- `get`으로 시작하는 메소드는 가져온 데이터를 가공하는 역할 (예외 있음)
- `Admin()`의 `send_mail()`은 `SMTP`를 사용해 메일을 전송하는 메소드,   
  메일을 전송하는 과정에서 `Client(Content)`의 `get_html()`을 요청
- `Content()`의 `get_html()`은 컨텐츠(딕셔너리)를 HTML 형식으로 변환하는 역할,   
  `Content()`안에 있던 `get_html()`이 구현 중 길어져 `content.html.py`로 분리,   
  어떠한 딕셔너리를 넣어도 같은 결과를 만들기 위해 딕셔너리의 Depth를 고려한 재귀함수 사용

---

## 7. Input/Output

### Client Input

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

### Client Output

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

### Saramin Output

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

### Jobkorea Output

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

### Wanted Output

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

---

## 8. Error List

### Python Circular Imports
- 부모/자식 객체가 서로를 호출하는 구조로 설계한 것이 원인으로,   
부모 객체에서 자식 객체를 Import하는 구문을 자식 객체가 필요한 순간 바로 위로 이동

### Gmail Unsupported Tags
- [What HTML tags are supported in Gmail?](https://zapier.com/help/doc/what-html-tags-are-supported-in-gmail)
- 에러가 아니라 단순히 Gmail에서 해당 태그를 지원하지 않는다는 것을 인지하고   
`details` 태그를 `blockquote` 태그로 변경

---

## 9. Post-Project
- [Daily DevBlog](http://daily-devblog.com/)를 벤치마킹하여 처음엔 웹상에서 돌아가는 서비스로 만들고 싶었지만,   
  매우 짧은 프로젝트 기간 동안 만들기엔 무리라 판단하여 기각 (개인적으로라도 구현해볼 것)
- 재귀함수를 사용하여 채용정보를 HTML로 변환하는 부분을 비교적 짧게 기술한 것은 좋지만,   
  결과물이 미적으로 아름답지 않음 (Gmail에 css를 포함하긴 어려울 듯)
- 잡코리아의 경우 반복 시도 시 차단되는 문제가 있어 최적의 딜레이 시간 탐색할 필요
- 원티드의 경우 셀레니움을 사용하는 것이 탐탁치 않음, POST 요청 등 다른 방안 탐색할 필요
- 하루 100회 제한의 사람인 API로 여러 명의 클라이언트 요청을 받기엔 무리가 있기 때문에,
  한번에 대량의 정보를 요청해서 DB에 따로 저장해 두었다가 반환하는 방법도 고려할 필요
- 클라이언트의 요청을 DB에 저장하고 데이터를 분석해 관심사를 파악하면 재밌을 듯
- 딕셔너리를 HTML로 변환하는 함수는 따로 라이브러리로 만들어서 나중에 사용해도 괜찮을 듯
