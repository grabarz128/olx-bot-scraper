import requests
import re

from bs4 import BeautifulSoup

def crawling(website_link, link_class):
    '''
    Args: website_link = string; link of website to be crawled
          link_class = string; class name for job link on website
    Returns: jobs_link = list; list of jobs 
    '''
    
    # get content of website and parse it
    website_request = requests.get(website_link, timeout=5)
    website_content = BeautifulSoup(website_request.content, 'html.parser')
    
    # extract link 
    moto_list = []
    iter = 0
    for line in website_content.find_all(class_ = link_class, href=True):
        moto_link = line.get('href')
        if re.search("^/d/oferta",moto_link):
            moto_link = 'https://www.olx.pl' + moto_link
        moto_list.append(moto_link)

    return moto_list


def send_message(chat_id, text, bot):
    '''
    Takes the chat id of a telegram bot and the text that was  crawled from the
    website and sends it to the bot
    Args: chat_id = string; chat id of the telegram bot, 
          text = string; crawled text to be sent
          bot = string; link to telegram bot API
    Returns: None
    '''
    
    parameters = {'chat_id': chat_id, 'text': text}
    message = requests.post(bot + 'sendMessage', data=parameters)


