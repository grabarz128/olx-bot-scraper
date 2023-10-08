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
ini_links_dict = dict(config.items('links'))
ini_class_dict = dict(config.items('classes'))

#scraper options

bot = ini_dict['bot']
chat_id = ini_dict['chat_id']

#elephantsql options
password_ = ini_sql_dict['password']
user_ = ini_sql_dict['user']
database_ = ini_sql_dict['database']
port_ = ini_sql_dict['port']
host_ = ini_sql_dict['host']
name_list = ["link", "name", "price"]

def check_result_send_mess(tab_name, search_query):
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
        moto_db.execute('CREATE TABLE IF NOT EXISTS {0} (id SERIAL, link TEXT NOT NULL, name TEXT NOT NULL, price TEXT NOT NULL )'.format(tab_name))
        conn.commit()
            
    except:
        send_message(chat_id, 'The database could not be accessed', bot)
       
        
    # crawl the link from website
    crawled_links = crawling(search_query, ini_class_dict)
    
    # check if there were new links added
    send_message(chat_id, f"=== {tab_name} ===" ,bot)

    for item in crawled_links:
        job_exists = moto_db.execute(f'SELECT link FROM {tab_name} WHERE (link = %s AND price = %s)', (item.link, item.price))
        if len(moto_db.fetchall()) != 1:
            mess_content = item.link 
            send_message(chat_id, mess_content, bot)
            moto_db.execute(f'INSERT INTO {tab_name} (link, name, price) VALUES (%s, %s, %s);', (item.link, item.advName, item.price))
            conn.commit()
        else:
            continue

    # end SQL connection
    moto_db.close()

for key, value in ini_links_dict.items():
    check_result_send_mess(key, value)

#TODO dodać gui z wwuszkiwarka i filtrami
#TODO agereacgja z ronych portali typu olx, facebook marketplace, ebay (czy to ma sens?)


