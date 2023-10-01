import requests
from bs4 import BeautifulSoup
import os.path
import csv
import lxml


def find_pages():
    url = 'https://www.tomsk.ru09.ru/realty/?type=1&otype=1'
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }

    req = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    pages = soup.find(class_='pager_pages').find_all('a')
    last_page = int(pages[-2].get('href').split('=')[-1])

    return last_page+1


def get_links(all_pages):
    links_list = []
    for i in range(1, 2):
        headers = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        }
        url = f'https://www.tomsk.ru09.ru/realty/?type=1&otype=1&page={i}'
        req = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')
        links = soup.find_all(class_='visited_ads')
        for item in links:
            adv_link = 'https://www.tomsk.ru09.ru'+ item.get("href")
            links_list.append(adv_link)
    return links_list





if __name__ == '__main__':
    all_pages=find_pages()
    get_links(all_pages)


