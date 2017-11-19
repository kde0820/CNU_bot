"""
식단 크롤링
"""
from selenium import webdriver
from bs4 import BeautifulSoup
import pymysql
import requests
# 식단 페이지 URL
MENU = "http://cnuis.cnu.ac.kr/jsp/etc/weekMenuFrame.jsp"

# 학생생활관 식단 URL
DORM_MENU = "http://dorm.cnu.ac.kr/html/kr/sub03/sub03_0304.html"

MENU_DORM = []
MENU_2 = []
MENU_3 = []


def main():
    soup = get_CNU(MENU)
    crawlling_MENU(soup, MENU_2, MENU_3)

    soup = getURL(DORM_MENU)
    crawlling_DORM(soup, MENU_DORM)

    inputData(MENU_DORM, MENU_2, MENU_3)


def inputData(list1, list2, list3):
    cnx = pymysql.connect(user='root', password='1234qwer', host='110.35.41.233', port='13306', database='cnu_bachelor_info')
    cursor = cnx.cursor()
    print(list[0])
    stmt = "INSERT INTO food (CNUM, m_date, menu, price) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE m_date=VALUES(m_date)"

    cursor.executemany(stmt, list1)
    cursor.executemany(stmt, list2)
    cursor.executemany(stmt, list3)

    cnx.commit()
    cnx.close()


# 해당 URL에서 페이지 소스를 받아옴
def getURL(URL):
    r = requests.get(URL)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    return soup


def get_CNU(URL):
    # PhantomJS 경로 설정
    browser = webdriver.PhantomJS("C:\\Users\\a\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
    browser.get(URL)
    browser.switch_to_frame('bottom')

    html_source = browser.page_source
    browser.quit()

    soup = BeautifulSoup(html_source, 'html.parser')
    return soup


# 해당 태그의 텍스트에서 공백을 제거하여 리턴
def del_blank(tag):
    txt = tag.get_text()
    return ''.join(txt.split())


# 메뉴 크롤링
def crawlling_MENU(soup, data_list1, data_list2):
    tr_list = soup.find_all('tr', {'bgcolor': '#FFFFFF'}, limit=5)  # 요일별 메뉴 (0~4: 월~금)

    for tr in tr_list:
        day = tr.find_all('td', limit=2)  # 날짜(0), 요일(1)
        td_list = tr.find_all('td', {'height': '20'}, limit=3)  # 2학메뉴(0), 2학가격(1), 3학메뉴(2)

        date = del_blank(day[0])
        menu_list_2 = td_list[0].find_all('td')  # 2학 메뉴 리스트
        menu_2 = del_blank(day[1]) + '\n'
        price = del_blank(td_list[1])  # 2학 가격

        menu_list_3 = td_list[2].find_all('td')  # 3학 메뉴 리스트
        menu_3 = del_blank(day[1]) + '\n'

        '''2학 메뉴'''
        for m in menu_list_2:
            menu_2 = menu_2 + del_blank(m) + '\n'
        '''3학 메뉴'''
        for menu in menu_list_3:
            menu_3 = menu_3 + del_blank(menu) + '\n'

        query_data = (2, date, menu_2, price)  # 날짜, 메뉴, 가격으로 구성된 데이터
        data_list1.append(query_data)  # 리스트에 2학 데이터 추가
        query_data2 = (3, date, menu_3, 0)  # 날짜, 메뉴로 구성된 데이터
        data_list2.append(query_data2)  # 리스트에 3학 데이터 추가


# 학생생활관 식단 크롤링
def crawlling_DORM(soup, data_list):
    table = soup.find('table', {'class': 'default_view diet_table'})

    tbody = table.find('tbody')
    tr_list = tbody.find_all('tr')  # 요일별 메뉴 (0~6: 월~일)

    for tr in tr_list:
        td_date = tr.find('td')
        bal = tr.find_all('td', {'class': 'left'})  # 아침(0) & 점심(1)
        dinner = tr.find('td', {'class': 'left last'})  # 저녁

        date = td_date.get_text()
        menu = '아침\n' + bal[0].get_text() + '점심\n' + bal[1].get_text() + '저녁\n' + dinner.get_text()

        query_data = (1, date, menu, 3200)  # 날짜, 메뉴로 구성된 데이터
        data_list.append(query_data)  # 데이터를 리스트에 추가


if __name__ == "__main__":
    main()