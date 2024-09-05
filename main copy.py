# * 웹 크롤링 동작
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager
webdriver_manager_directory = ChromeDriverManager().install()
import time
# ChromeDriver 실행

from selenium.webdriver.chrome.options import Options

from pymongo import MongoClient

mongoClient = MongoClient("mongodb://127.0.0.1:27017/news_scraping")
# database 연결
database = mongoClient["news_scrapping"]
# collection 작업
collection = database['ict_news']
collection.delete_many({'news_date': None})

results = collection.find({ 'news_date': None },{'_id':0,'news_link':1})
for document in results:
    print(document)
pass