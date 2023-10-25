import requests
import re

from bs4 import BeautifulSoup


class result():
    def __init__(self,link, price, advName) -> None:
        self.link = link
        self.price = price
        self.advName = advName

    def __repr__(self) -> str:
        return f"{self.link}, {self.price}, {self.advName}"

def crawling(website_link, link_class):
    '''
    Args: website_link = string; link of website to be crawled
          link_class = string; class name for job link on website
    Returns: jobs_link = list; list of jobs 
    '''
    
    # get content of website and parse it
    website_request = requests.get(website_link, timeout=40)
    website_content = BeautifulSoup(website_request.content, 'html.parser')
    
    # extract link 
    url = []
    price = []
    adv_name = []
    pack = []
    
    for line in website_content.find_all(class_ = link_class['link_class']):
        moto_link = line.get('href')
        if re.search("^/d/oferta",moto_link):
            moto_link = 'https://www.olx.pl' + moto_link
    
        url.append(moto_link)
    
    for line in website_content.find_all("p",class_ = link_class['price_class']):
        if re.search("do negocjacji",line.get_text()):          
            price.append(line.get_text().replace("do negocjacji",""))
        else:
            price.append(line.get_text())

    for line in website_content.find_all("h6",class_ = link_class['adv_name_class']):
        adv_name.append(line.get_text())
    
    if len(url) == len(price) == len(adv_name):
        for i in range(len(url)):
            if re.search("extended_search_extended_delivery", url[i]):
                continue
            pack.append(result(url[i], price[i], adv_name[i]))

    return pack


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


