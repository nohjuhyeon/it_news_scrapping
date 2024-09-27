from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from newspaper import Article
from webdriver_manager.chrome import ChromeDriverManager
import time
import os 

from news_crawling_func.ict_scraping_func import nate, chosun, digital_times, hani, munhwa, naver, busan, kookje,kbs,boannews,ddaily,itworld,news1,datanews,ciokorea,dnews,topdaily, kukinews, economist, asiatime, metroseoul,donga,skyedaily,sbs_biz,mtn,kotra,newspim,nocut,newsprime, medipana, marketinsight, dailynk, kgnews, dailymedi, kyeongin, newstomato, esquirekorea, lawtimes


def init_browser():
    # Chrome 브라우저 옵션 및 WebDriver 설정
    chrome_options = Options()
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def fetch_news_date(news_link, browser):
    # 뉴스 날짜를 사이트에서 가져오는 함수
    handlers = {
        'n.news.naver': naver,
        'www.busan': busan,
        'www.hani': hani,
        'www.dt': digital_times,
        'www.kookje': kookje,
        'www.munhwa': munhwa,
        'm.news.nate': nate,
        'ddaily.co.kr':ddaily,
        'itworld.co.kr':itworld,
        'news1.kr':news1,
        'datanews.co.kr':datanews,
        'ciokorea':ciokorea,
        'dnews.co.kr':dnews,
        'topdaily.kr': topdaily, 
        'kukinews.com': kukinews, 
        'economist.co.kr': economist,  
        'asiatime.co.kr': asiatime, 
        'metroseoul.co.kr': metroseoul,
        'it.donga' : donga,
        'skyedaily' : skyedaily,
        'news.mtn' : mtn,
        'dream.kotra' : kotra,
        'newspim' : newspim,
        'nocutnews' : nocut,
        'newsprime' : newsprime,
        'medipana.com' : medipana,
        'marketinsight': marketinsight, 
        'dailynk': dailynk, 
        'kgnews': kgnews, 
        'dailymedi': dailymedi, 
        'kyeongin': kyeongin, 
        'newstomato': newstomato, 
        'esquirekorea': esquirekorea,
        'lawtimes' : lawtimes

    }
    for key, handler in handlers.items():
        if key in news_link:
            return handler(browser)
    return None

def process_links(link_elements, collection, browser,news_topic,crawling_count):
    results = collection.find({},{'_id':0,'news_link':1})
    link_list = [i['news_link'] for i in results]
    original_window = browser.current_window_handle


    for link_element in link_elements:
        
        link = link_element.get_attribute('href')
        time.sleep(1)  # 대기 시간
        if link not in link_list:
            try:
                if 'https://zdnet.co.kr/error/' in link or 'cuts.top' in link  or 'dailysecu' in link or 'datanet' in link or 'search.naver' in link or 'kmib.co.kr' in link or 'cctvnews' in link:
                    pass  # 해당 링크는 무시


                elif 'chosun.com' in link:
                    link_element.click()
                    browser.switch_to.window(browser.window_handles[-1])
                    try:
                        chosun(link, collection, browser,news_topic)
                        crawling_count+=1
                    except:
                        pass
                    browser.close()
                    browser.switch_to.window(browser.window_handles[-1])

                elif 'biz.sbs' in link:
                    link_element.click()
                    browser.switch_to.window(browser.window_handles[-1])
                    try:
                        sbs_biz(link, collection, browser,news_topic)
                        crawling_count+=1
                    except:
                        pass
                    browser.close()
                    browser.switch_to.window(browser.window_handles[-1])

                elif 'news.kbs' in link:
                    link_element.click()
                    browser.switch_to.window(browser.window_handles[-1])
                    try:
                        kbs(link, collection, browser,news_topic)
                        crawling_count+=1
                    except:
                        pass
                    browser.close()
                    browser.switch_to.window(browser.window_handles[-1])
            
                elif 'boannews.com' in link:
                    link_element.click()
                    browser.switch_to.window(browser.window_handles[-1])
                    try:
                        boannews(link, collection, browser,news_topic)
                        crawling_count+=1
                    except:
                        pass
                    browser.close()
                    browser.switch_to.window(browser.window_handles[-1])
            
                else:
                    article = Article(link, language='ko')
                    article.download()
                    article.parse()
                    title, date, content = article.title, article.publish_date, article.text
                    
                    if date is None:
                        link_element.click()
                        browser.switch_to.window(browser.window_handles[-1])
                        try:
                            date = fetch_news_date(link, browser)
                        except:
                            pass
                        browser.close()
                        browser.switch_to.window(browser.window_handles[-1])
                    
                    insert_news(collection, title, content, date, link,news_topic) 
                    crawling_count+=1
            except:
                pass
        for handle in browser.window_handles:
            if handle != original_window:
                browser.switch_to.window(handle)
                browser.close()

        browser.switch_to.window(original_window)
    return crawling_count

def insert_news(collection, title, content, date, link,news_topic):
    # 뉴스 데이터를 MongoDB에 삽입하는 함수
    collection.insert_one({
        'news_title': title,
        'news_content': content,
        'news_date': date,
        'news_link': link,
        'news_topic':news_topic
    })
 
def ict_news():
    crawling_count = 0
    # MongoDB 클라이언트 및 컬렉션 설정
    mongo_url = os.getenv("DATABASE_URL")
    mongo_client = MongoClient(mongo_url)
    collection = mongo_client["news_scraping"]['ict_news']

    # 브라우저 초기화 및 사이트 접속
    browser = init_browser()
    browser.get("https://ictnewsclipping.stibee.com/")
    
    first_content = browser.find_element(by=By.CSS_SELECTOR,value='#__next > div.styles__NewsLettersLayout-sc-1081fac-0.lkUNZD > div.styles__NewsletterList-sc-1081fac-2.hNvBbS > div:nth-child(1) > a')
    first_content.click()
    time.sleep(1)
    # 메인 페이지에서 콘텐츠 리스트를 가져옴
    

    for j in range(10):
        time.sleep(1)
        content_list_first = browser.find_elements(by=By.CSS_SELECTOR,value='div.stb-left-cell > div.stb-text-box > table > tbody > tr > td')
        content_title = browser.find_element(by=By.CSS_SELECTOR,value='#__next > div.styles__ContentLayout-sc-1gp3t1j-0.dsJnNu > div.styles__ContentTitleWrapper-sc-f7jtp3-0.jWHlht > div.styles__Title-sc-f7jtp3-1.edStrD').text
        if '[ICT 뉴스' in content_title:
            for i in content_list_first:
                try:
                    news_topic = i.find_element(by=By.CSS_SELECTOR,value='div > span').text
                except:
                    news_topic = i.find_element(by=By.CSS_SELECTOR,value='h2 > span').text
                contents_list = i.find_elements(by=By.CSS_SELECTOR,value='a')
                crawling_count = process_links(contents_list, collection, browser,news_topic,crawling_count)
        else:
            j = j - 1
        before_btn = browser.find_element(by=By.CSS_SELECTOR,value='#__next > div.styles__ContentLayout-sc-1gp3t1j-0.dsJnNu > div.styles__Layout-sc-1p30c38-0.gHNJKT > div > div.styles__PaginationButton-sc-1p30c38-2.dTIEOP.prev > div > div > div.title')
        before_btn.click()
                    
        


    # 브라우저 종료
    browser.quit()
    print('ict news crawling finish')
    print('crawling count : ',crawling_count)

# 크롤링 함수 실행
ict_news()