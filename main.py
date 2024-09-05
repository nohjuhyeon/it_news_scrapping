from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import time

from news_letter.venture_doctors import venture_doctors
from news_letter.ict_news import ict_news
from news_letter.statistic_bank import statistic_bank
from news_letter.seoul_institute import seoul_institute

# 실행할 함수 정의
# 스케줄러 초기화
scheduler = BackgroundScheduler()

# 매주 월요일 오전 9시에 함수 실행
scheduler.add_job(venture_doctors, CronTrigger(hour=12, minute=0))
scheduler.add_job(ict_news, CronTrigger( hour=12, minute=15))
scheduler.add_job(statistic_bank, CronTrigger( hour=12, minute=30))
scheduler.add_job(seoul_institute, CronTrigger(hour=12, minute=45))

# 스케줄러 시작
scheduler.start()

print("Scheduler started...")

# 메인 프로그램이 종료되지 않도록 유지
try:
    while True:
        time.sleep(1)  # Keep the main thread alive
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print("Scheduler shut down.")