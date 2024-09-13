import json
from pymongo import MongoClient

# mongoClient = MongoClient("mongodb://127.0.0.1:27017/news_scraping")
# # database 연결
# database = mongoClient["news_scrapping"]
# # collection 작업
# collection = database['ict_news']
# # collection.delete_many({'news_date': None})

# # results = collection.find({ 'news_date': None },{'_id':0,'news_link':1})
# # for document in results:
# #     print(document)
# # pass

# 파일을 열고 데이터를 로드하는 코드
with open("train_original.json", "r", encoding="utf-8") as file:
    data = json.load(file)
train_list = []
for i in data['documents']:
    dict_article = {}
    dict_article['category'] = i['category']
    dict_article['title'] = i['title']
    content_list = []
    for j in i['text']:
        for k in j:
            content_list.append(k['sentence'])
    dict_article['text'] = ' '.join(content_list)
    extractive = ''
    for j in i['extractive']:
        try:
            extractive += content_list[j] + ' '
        except:
            pass
    dict_article['extractive']= extractive[:-1]
    dict_article['abstractive'] = ' '.join(i['abstractive'])
    train_list.append(dict_article)
# 파일 데이터를 확인 (예: 출력)
with open("output.json", "w", encoding="utf-8") as file:
    json.dump(train_list, file, ensure_ascii=False, indent=4)
pass
# print(data)
