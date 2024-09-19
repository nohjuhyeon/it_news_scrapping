
from newspaper import Article
from transformers import pipeline, BertTokenizer, BertForSequenceClassification

# Summarization pipeline을 설정합니다.
summarizer = pipeline('summarization', model='facebook/bart-large-cnn')

# 기사 URL 설정
url = 'https://www.inven.co.kr/webzine/news/?news=263028'

# 기사 객체 생성 및 다운로드
article = Article(url, language='ko')
article.download()
article.parse()

# 기사 정보 출력
print("제목:", article.title)
print("작성자:", article.authors)
print("게시 날짜:", article.publish_date)
print("본문 내용:", article.text.replace('\n',''))

# NLP 분석을 위한 설정

# `transformers` 라이브러리를 이용한 텍스트 요약
text = article.text.replace('\n','')  # 원본 본문
summary = summarizer(text[:500],  do_sample=False)

print("transformers 요약:", summary[0]['summary_text'])
