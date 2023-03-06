# olx-bot-scraper

## Simple bot which scraps links form olx.pl website, put them in database and send new links to us via telegram bot  

To run bot we just have to execute function **check_result_send_mess()** in script _database_check.py_.  

After fight with cloud platforms as heroku, pythoneverywhere, azure etc. I decided to just put this on VPS and use CRON schedule.  
I have used external database but we also can use local, depending on which service we put our script.  
Before starting we need to fill in _config_template.ini_ and change name to _config.ini_

- Database - free PostgreSQL base on [elephantsql](https://www.elephantsql.com/)  
- Sending message - [Telegram bot API](https://core.telegram.org/bots/api) and HTTP requests from [requests](https://pypi.org/project/requests/)  
- Scraping - [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)    
- PostrgreSQL connection - [pscopg2](https://www.psycopg.org/docs/)
- Read config - [configparser](https://docs.python.org/3/library/configparser.html)

More functionalities, soon!

