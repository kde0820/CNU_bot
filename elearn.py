"""
이러닝 홈페이지 크롤링
"""
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import time
import pymysql

E_URL = "http://e-learn.cnu.ac.kr/"
S_URL = "http://e-learn.cnu.ac.kr/lms/mypage/schedule/doListView.dunet"

username = '201502022'  # 아이디
password = ''  # 패스워드

E_hw = []


def inputData(list):
    cnx = pymysql.connect(user='root', password='1234qwer', host='110.35.41.233', port='13306', database='cnu_bachelor_info')
    cursor = cnx.cursor()
    print(list[0])
    stmt = "INSERT INTO e_ref (title, r_date) VALUES (%s, %s) ON DUPLICATE KEY UPDATE title=VALUES(title)"
    cursor.executemany(stmt, list)

    cnx.commit()
    cnx.close()


def main():
    ''' PhantomJS를 이용하여 이러닝 사이트에 접속 '''
    driver = webdriver.PhantomJS("C:\\Users\\a\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe")
    driver.set_window_size(1124, 850)
    driver.get(E_URL)

    login_elearn(driver)  # 이러닝 사이트에 로그인
    s_source = schedule(driver)  # 일정관리 페이지소스

    driver.quit()  # PhantomJs 종료

    crawlling_hw(s_source, E_hw)  # 일정 목록

    # inputData(E_hw)


# 이러닝 사이트에 로그인
def login_elearn(driver):
    login = None
    while not login:  # NoSuchElementException 처리
        try:
            login = driver.find_element_by_xpath("//a[@ id = 'pop_login']")  # 로그인창
        except NoSuchElementException:
            time.sleep(.5)

    login.click()  # 로그인창 활성화
    time.sleep(.5)

    loginform = driver.find_elements_by_tag_name('form')  # 로그인 폼
    userid = loginform[1].find_element_by_class_name('input_id')  # 아이디
    userpass = loginform[1].find_element_by_class_name('input_pw')  # 패스워드

    userid.send_keys(username)  # 아이디 전송
    userpass.send_keys(password)  # 패스워드 전송

    login_button = loginform[1].find_element_by_id('btn-login')  # 로그인 버튼
    login_button.click()  # 로그인 버튼 클릭
    time.sleep(2)


# 일정관리 탭에 접속하여 페이지 소스 리턴
def schedule(driver):
    driver.get(S_URL)  # 일정관리 접속
    time.sleep(2)

    html_source = driver.page_source  # 웹페이지 소스 가져옴

    return html_source


# 과제 목록 크롤링
def crawlling_hw(html_source, data_list):
    soup = BeautifulSoup(html_source, 'html.parser')
    div = soup.find('div', {'class': 'calendar_list'})
    slist = div.find('ul')
    li_list = slist.find_all('li', {'class': 'bg'})

    for li in li_list:
        title = li.find('span').get_text()
        info = li.find('span', {'class': 'stxt'}).get_text()

        query_data = (title, info)
        data_list.append(query_data)
    print(data_list)

# 해당 태그의 텍스트에서 공백을 제거하여 리턴
def del_blank(tag):
    txt = tag.get_text()
    return ''.join(txt.split())


if __name__ == "__main__":
    main()