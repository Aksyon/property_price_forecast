import requests
from bs4 import BeautifulSoup
import os.path
import csv
import lxml

headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }
def find_pages():
    url = 'https://www.tomsk.ru09.ru/realty/?type=1&otype=1'

    req = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    pages = soup.find(class_='pager_pages').find_all('a')
    last_page = int(pages[-2].get('href').split('=')[-1])

    return last_page+1


def get_links(all_pages):
    links_list = []
    for i in range(1, 2):
        url = f'https://www.tomsk.ru09.ru/realty/?type=1&otype=1&page={i}'
        req = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')
        links = soup.find_all(class_='visited_ads')
        for item in links:
            adv_link = 'https://www.tomsk.ru09.ru'+ item.get("href")
            links_list.append(adv_link)
    return links_list

def get_data(links):
    if not os.path.exists('data'):
        os.mkdir('data')

    with open('data/property_info.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'кол-во комнат',
                'общая площадь',
                'жилая площадь',
                'кухня',
                'этаж',
                'этажность',
                'отделка',
                'санузел',
                'материал',
                'год постройки',
                'вид жилья',
                'балкон',
                'цена',
                'описание'
            )
        )

    for link in links:

        req = requests.get(url=link, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')
        # try:
        #     attributes = soup.find_all(class_='realty_detail_attr')
        #
        #     for attr in attributes:
        #         if attr.find('th').find('span').text.strip().split('&')[0] == 'Количество комнат':
        #             rooms = int(attr.find('b').text.strip())
        #         elif attr.find('th').find('span').text.strip().split('&')[0] == 'Общая площадь':
        #             full_area = int(attr.find('b').text.strip().rstrip(' кв.м'))
        #         elif attr.find('th').find('span').text.strip().split('&')[0] == 'жилая':
        #             living_area = int(attr.find('b').text.strip().rstrip(' кв.м'))
        #         elif attr.find('th').find('span').text.strip().split('&')[0] == 'кухня':
        #             kitchen_area = int(attr.find('b').text.strip().rstrip(' кв.м'))
        #         elif attr.find('th').find('span').text.strip().split('&')[0] == 'Этаж/этажность':
        #             floor_number = int(attr.find('b').text.strip().split('/')[0])
        #         elif attr.find('th').find('span').text.strip().split('&')[0] == 'Этаж/этажность':
        #             floors_in_building = int(attr.find('b').text.strip().split('/')[1])
        #         elif attr.find('th').find('span').text.strip().split('&')[0] == 'Отделка':
        #             repair_type = attr.find('b').text.strip()
        #         elif attr.find('th').find('span').text.strip().split('&')[0] == 'Санузел':
        #             bathroom_type = attr.find('b').text.strip()
        #         elif attr.find('th').find('span').text.strip().split('&')[0] == 'Материал':
        #             material_type = attr.find('b').text.strip()
        #         elif attr.find('th').find('span').text.strip().split('&')[0] == 'Год постройки':
        #             bathroom_type = int(attr.find('b').text.strip())
        #         elif attr.find('th').find('span').text.strip().split('&')[0] == 'Вид':
        #             flat_type = attr.find('b').text.strip()
        #         elif attr.find('th').find('span').text.strip().split('&')[0] == 'Балкон/лоджия':
        #             balcony_type = attr.find('b').text.strip()
        #             print(rooms)
        # except Exception:
        #     continue

        price = soup.find(class_='realty_detail_price inline').text.strip().rstrip(' руб.').split('&nbsp;')
        print(price)





if __name__ == '__main__':
    all_pages=find_pages()
    links = get_links(all_pages)
    get_data(links)


