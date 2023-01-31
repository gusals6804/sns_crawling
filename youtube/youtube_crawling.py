# 라이브러리 임포트
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(executable_path='./chromedriver.exe')

driver.get('https://youtu.be/_eGsjswtvPA')  # 링크 열기
driver.implicitly_wait(7)

time.sleep(1.5)

driver.execute_script('window.scrollTo(0, 800)')  # 한번 스크롤
time.sleep(3)

last_height = driver.execute_script('return document.documentElement.scrollHeight')  # 스크롤 전체 높이

while True:
    driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')  # 스크롤 다운
    time.sleep(3)

    new_height = driver.execute_script('return document.documentElement.scrollHeight')  # 스크롤 다운 후 스크롤 높이

    if new_height == last_height:  # 댓글 마지막 페이지면 while문 벗어남
        break

    last_height = new_height
    time.sleep(3)

    # 대댓글 다열기
    rereple = driver.find_elements_by_css_selector("#more-replies")
    for re in rereple:
        driver.execute_script("arguments[0].click()", re)
        time.sleep(1.5)
    time.sleep(2)

    try:
        driver.find_element_by_css_selector('#dismiss-button > a').click()  # 유튜브 1달 무료 팝업닫기

    except:
        pass

# 댓글 크롤링
html_source = driver.page_source
soup = BeautifulSoup(html_source, 'html.parser')

id_list = soup.select('div#header-author > h3 > #author-text > span')  # id 리스트
comment_list = soup.select('yt-formatted-string#content-text')  # comment 리스트

# 파싱해서 넣을 실제 데이터 리스트
id_final = []
comment_final = []

for i in range(len(comment_list)):
    temp_id = id_list[i].text
    temp_id = temp_id.replace('\n', '').replace('\t', '').replace(' ', '').strip()
    id_final.append(temp_id)  # 댓글 작성자

    temp_comment = comment_list[i].text
    temp_comment = temp_comment.replace('\n', '').replace('\t', '').replace('\r', '').strip()
    comment_final.append(temp_comment)  # 댓글 내용

# DataFrame 만들기(list -> dictionary -> dataframe)
# list -> dictionary
youtube_dic = {"아이디": id_final, "댓글 내용": comment_final}
# dictionary -> dataframe
youtube_pd = pd.DataFrame(youtube_dic)

print(youtube_pd.head())

youtube_pd.to_csv('./youtube_lg_review.csv', encoding='utf-8')