import os
import psycopg2
import crawl
import configparser
import sqlite3 as lite
from crawl import crawling,send_message

# read config parameters from ini fili
config = configparser.RawConfigParser()
config.read('config.ini')
ini_dict = dict(config.items('telegram'))
ini_sql_dict = dict(config.items('elephantsql'))

#scraper options
website_link = ini_dict['website_link']
link_class = ini_dict['link_class']
bot = ini_dict['bot']
chat_id = ini_dict['chat_id']

#elephantsql options
password_ = ini_sql_dict['password']
user_ = ini_sql_dict['user']
database_ = ini_sql_dict['database']
port_ = ini_sql_dict['port']
host_ = ini_sql_dict['host']


def check_result_send_mess():
    '''
    This function looks up the values stored in the SQL database
    and compares them to the crawled  and sends out any links
    not in the db to the telegram bot
    Args: None
    Returns: None
    '''
    
    # try to create SQL database and table to store links in, else send error message to bot
    try:
        conn = psycopg2.connect(database = database_, user = user_, password = password_, host = host_, port = port_)
        moto_db = conn.cursor()
        moto_db.execute('CREATE TABLE IF NOT EXISTS motorcycles_links (id SERIAL, link TEXT NOT NULL)')
        conn.commit()
      
    except:
       send_message(chat_id, 'The database could not be accessed', bot)
        
    # crawl the link from website
    crawled_links = crawling(website_link,link_class)
    
    # check if there were new links added
    for item in crawled_links:
        job_exists = moto_db.execute('SELECT link FROM motorcycles_links WHERE link = %s', [item])
        if len(moto_db.fetchall()) != 1:
            mess_content = item 
            send_message(chat_id, mess_content,bot)
            moto_db.execute('INSERT INTO motorcycles_links (link) VALUES (%s);', [item])
            conn.commit()
        else:
            continue

    # end SQL connection
    moto_db.close()

