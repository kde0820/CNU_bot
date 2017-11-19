"""
학생생활관 홈페이지 크롤링
"""
import requests
from bs4 import BeautifulSoup
import pymysql

# 은행사 공지사항 URL page number 제외
DORM = "https://dorm.cnu.ac.kr/_prog/_board/?code=sub05_0501&site_dvs_cd=kr&menu_dvs_cd=0501&skey=&sval=&site_dvs=&GotoPage="
CONCAT_URL = "https://dorm.cnu.ac.kr/_prog/_board"

DORM_info = []


def inputData(list1):
    cnx = pymysql.connect(user='root', password='1234qwer', host='110.35.41.233', port='13306', database='cnu_bachelor_info')
    cursor = cnx.cursor()
    print(list[0])

    stmt = "INSERT INTO board (bid, title, link, writer, pdate) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE title=VALUES(title)"

    cursor.executemany(stmt, list1)

    cnx.commit()
    cnx.close()


def main():
    for i in range(1, 6):  # 5 페이지 가져옴
        '''은행사 공지사항'''
        URL = DORM + str(i)  # 기본 URL에 페이지 번호를 붙여줌
        soup = getURL(URL)
        crawlling(soup, DORM_info)

    inputData(DORM_info)


# 해당 URL에서 페이지 소스를 받아옴
def getURL(URL):
    r = requests.get(URL)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    return soup


# 학생생활관 은행사 공지 크롤링
def crawlling(soup, data_list):
    table = soup.find('div', {'class': "board_list"})
    tbody = table.find('tbody')
    tr_list = tbody.find_all('tr')

    for tr in tr_list:
        c_title = tr.find('td', {'class': 'title'})
        c_href = tr.find('td', {'class': 'title'}).a.get('href')
        c_center = tr.find('td', {'class': 'center'})
        c_date = tr.find('td', {'class': 'date'})

        title = c_title.a.get_text()  # 제목
        link = CONCAT_URL + c_href[1:]  # 링크
        writer = c_center.get_text()  # 작성자
        date = c_date.get_text()  # 작성일

        query_data = (8, title, link, writer, date)  # 제목,링크,작성자,작성일 로 구성된 데이터
        data_list.append(query_data)  # 데이터를 리스트에 추가


if __name__ == "__main__":
    main()