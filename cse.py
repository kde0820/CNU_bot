"""
컴퓨터공학과 홈페이지 크롤링
"""
import requests
from bs4 import BeautifulSoup
import pymysql

# 페이지 번호를 제외한 URL
INFO = "http://computer.cnu.ac.kr/index.php?mid=notice&page="       # 학사 공지
G_INFO = "http://computer.cnu.ac.kr/index.php?mid=gnotice&page="    # 일반 소식
S_INFO = "http://computer.cnu.ac.kr/index.php?mid=saccord&page="    # 사업단 소식

# 크롤링한 결과를 저장할 리스트
CSE_info = []
CSE_g_info = []
CSE_s_info = []


def inputData(list1, list2, list3):
    cnx = pymysql.connect(user='root', password='1234qwer', host='110.35.41.233', port='13306', database='cnu_bachelor_info')
    cursor = cnx.cursor()
    print(list[0])
    stmt = "INSERT INTO board (bid, title, link, writer, pdate) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE title=VALUES(title)"

    cursor.executemany(stmt, list1)
    cursor.executemany(stmt, list2)
    cursor.executemany(stmt, list3)

    cnx.commit()
    cnx.close()


def main():
    for i in range(6, 1, -1):  # 5 페이지 가져옴
        '''학사공지'''
        URL = INFO + str(i)  # 기본 URL에 페이지 번호를 붙여줌
        soup = getURL(URL)
        if (i == 1):  # 게시판에서 공지로 등록되어있는 글은 한번만 저장함
            crawlling_notice(soup, CSE_info, 5)
        else:
            crawlling(soup, CSE_info, 5)

        '''일반소식'''
        URL = G_INFO + str(i)
        soup = getURL(URL)
        if (i == 1):
            crawlling_notice(soup, CSE_g_info, 6)
        else:
            crawlling(soup, CSE_g_info, 6)

        '''사업단소식'''
        URL = S_INFO + str(i)
        soup = getURL(URL)
        if (i == 1):
            crawlling_notice(soup, CSE_s_info, 7)
        else:
            crawlling(soup, CSE_s_info, 7)

    inputData(CSE_info, CSE_g_info, CSE_s_info)


# 해당 URL에서 페이지 소스를 받아와서 리턴
def getURL(URL):
    r = requests.get(URL)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    return soup


# 해당 태그의 텍스트에서 공백을 제거하여 리턴
def del_blank(tag):
    txt = tag.get_text()
    return ''.join(txt.split())


# 페이지 소스 크롤링
def crawlling(soup, data_list, board):
    table = soup.find('div', {'class': 'bd_lst_wrp'})
    tbody = table.find('tbody')
    tr_list = tbody.find_all('tr')

    for tr in tr_list:
        if (tr.get('class') == None):
            c_title = tr.find('td', {'class': 'title'})
            c_href = tr.find('td', {'class': 'title'}).a.get('href')
            c_author = tr.find('td', {'class': 'author'})
            c_date = tr.find('td', {'class': 'time'})

            title = del_blank(c_title.a)  # 제목
            link = c_href  # 링크
            writer = c_author.get_text()  # 작성자
            date = c_date.get_text()  # 작성일

            query_data = (board, title, link, writer, date)  # 제목,링크,작성자,작성일 로 구성된 데이터
            data_list.append(query_data)  # 데이터를 리스트에 추가


# 게시판의 공지글만 가져와서 리스트에 추가
def crawlling_notice(soup, data_list, board):
    table = soup.find('div', {'class': 'bd_lst_wrp'})
    tbody = table.find('tbody')
    tr_list = tbody.find_all('tr')

    for tr in tr_list:
        c_title = tr.find('td', {'class': 'title'})
        c_href = tr.find('td', {'class': 'title'}).a.get('href')
        c_author = tr.find('td', {'class': 'author'})
        c_date = tr.find('td', {'class': 'time'})

        title = del_blank(c_title.a)  # 제목
        link = c_href  # 링크
        writer = c_author.get_text()  # 작성자
        date = c_date.get_text()  # 작성일

        query_data = (board, title, link, writer, date)  # 제목, 링크, 작성자, 작성일 로 구성된 데이터
        data_list.append(query_data)  # 데이터를 리스트에 추가


if __name__ == '__main__':
    main()