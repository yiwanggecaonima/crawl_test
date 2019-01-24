from basicSpider import *
from UA import UA
from bs4 import BeautifulSoup
import json
import pymongo
import re
from config import *
client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]
def get_html(url):

    headers = [("User-Agent",
                "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36")]
    proxy = {"http": "113.67.11.20:9000"}

    return downloadHtml(url = url, headers=headers, proxy=proxy)

def get_page(html):
    #soup = BeautifulSoup(html,'lxml')
    print(type(html))
    sub = json.loads(html)
    return sub['subjects']
        
def save_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('Successfully Saved to Mongo', result)
        return True
    return False

def main():
    url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&page_limit=50&page_start=0'
    html = get_html(url)
    result = get_page(html)
    if result:
        save_mongo(result)
        
if __name__ == '__main__':
    main()
