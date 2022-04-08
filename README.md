# Recruit Pirates
- 사람인, 잡코리아, 원티드로부터 채용 정보를 받아오는 서비스
- 종합한 정보를 메일로 전송하는 방식을 구상

---

## 팀 요구사항

### 사람인 연봉 지도 기대 반환값
```python
saramin.content = {
    'salary_map': '특정 지역에 관한 연봉 맵 (folium.Map 타입)'
}
```

### 잡코리아 기대 반환값
```python
jobkorea.content = {
    'company': { # 회사 이름
        'assay': '회사 채용공고별 합격자소서 리스트 (또는 다른 타입의 문자열 집합)'
    }
}
```

### 원티드 기대 반환값
```python
jobkorea.content = {
    'company': { # 회사 이름
        'skill': '회사 채용공고별 기술 역량 리스트 (문자열 집합)'
        # 필요하다면 우대사항 등 추가
        '우대사항': ...
    }
}
```

---

## Notice

### 클라이언트 요청 사항을 종합한 딕셔너리

```python
requires = {
    'locations': '희망 지역 리스트',
    'jobs': '희망 직업 리스트',
    'assay': '자기소개서 포함 여부 (Y/N)', # 잡코리아 연결
    'skill': '기술 역량 포함 여부 (Y/N)', # 원티드 연결
    'skill_map': '조건에 맞는 전체 기술 역량의 워드 클라우드 포함 여부 (Y/N)', # 원티드 연결
    'count': '보여줄 채용공고 개수 (기본값: 5, 최대값: 110)',
    'code_map': '지역, 직업 파라미터 코드 딕셔너리',
    'companies': """클라이언트가 지정한 특정 회사 목록 (생략 가능),
                    없을 경우 사람인 API에서 가져온 회사명 목록으로 대체,
                    잡코리아 및 원티드에서 사용)"""
}
```

### 사람인 API 반환값 json을 정리한 딕셔너리

```python
saramin_client = {
    'company': { # 회사 이름
        'company_id': '회사 페이지 주소',
        'position_id': '채용 공고 id (파라미터로 사용해 채용공고 페이지 이동 가능)',
        'title': '채용 공고 제목',
        'industry': '채용 공고의 서비스 분야 (SI, 게임 등)',
        'location': '직장 위치',
        'job_type': '정규직 등',
        'exp': '요구 경력',
        'edu': '요구 학력',
        'keyword': '채용 공고 키워드',
        'salary': '연봉 구간',
        'opening_date': '채용 공고가 올라온 날짜',
        'expiration_date': '채용이 끝나는 날짜',
        'dday': '채용 종료까지 남은 일자',
        'close-type': '마감일 형식 (접수 마감일, 상시 등)',
        'assay': '합격자소서',
        'skill': '기술 역량'
    }
}
```
