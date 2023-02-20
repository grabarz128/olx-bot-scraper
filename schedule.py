import schedule
import time
import database_check
from database_check import check_result_send_mess

# schedule crawler
schedule.every().day.at("07:00").do(check_result_send_mess)
schedule.every().day.at("12:00").do(check_result_send_mess)
schedule.every().day.at("16:00").do(check_result_send_mess)
schedule.every().day.at("21:00").do(check_result_send_mess)

# run script infinitely
while True:
    schedule.run_pending()
    time.sleep(1)