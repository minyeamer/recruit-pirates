# HTML 디자인 개선 필요 :(
def get_html(contents: dict, body=list(), head=1) -> list:
    head = min(head, 6)

    try:
        for title, contents in contents.items():
            if not contents:
                continue

            if title.find(' 제공') > -1:
                get_html_details(title, contents, body, head+1)
            else:
                get_html_div(title, contents, body, head)
    except Exception as e:
        print('컨텐츠를 HTML로 변환하는 과정에서 문제가 발생했습니다.')
        print(e)
        return list()

    return body


def get_html_details(title: str, contents: dict, body: list, head: int):
    """
    Gmail에서 <details> 태그 미지원
    다른 방안을 찾을 때까지 blockquote 태그로 대체
    """

    body.append(f'<h{head}>{title.capitalize()}</h{head}>')

    for details in contents.values():
        # body.append('<details>')
        # body.append(f'<summary>{title}</summary>')
        body.append('<blockquote>')
        get_html(details, body, head)
        body.append('</blockquote>')
        # body.append('</details>')


def get_html_div(title: str, contents: any, body: list, head: int):
    body.append(f'<div id="{title}">')

    get_html_header(title, contents, body, head+1)

    if type(contents) is not dict:
        get_html_body(contents, body)
    else:
        get_html(contents, body, head+1)

    body.append('</div>')


def get_html_header(title: str, contents: any, body: list, head: int):
    if head < 3:
        body.append('<hr>')

    ctype = type(contents)
    if ctype is tuple:
        get_html_anchor(contents[0], contents[1], body, head)
    else:
        body.append(f'<h{head}>{title.capitalize()}</h{head}>')


def get_html_anchor(title: str, url: str, body: list, head: int):
    body.append(f'<a href="{url}">')

    if title.find(' 바로가기') > 0:
        body.append(f'<p>{title.capitalize()}</p>')
    else:
        body.append(f'<h{head}>{title.capitalize()}</h{head}>')

    body.append(f'</a>')


def get_html_body(contents: any, body: list):
    ctype = type(contents)
    if ctype is str:
        text = contents.replace('. ', '.<br>')
        body.append(f'<blockquote>{text}</blockquote>')
    elif ctype is list:
        body.append('<ul>')
        for text in contents:
            if text[0] in {'•', '-'}:
                text = text[1:]
            text = text.replace('. ', '.<br>')
            body.append(f'<li>{text}</li>')
        body.append('</ul>')
    elif ctype is tuple:
        pass
    else:
        raise Exception(f'HTML 본문에 의도하지 않은 타입이 입력되었습니다: {ctype}')
