import requests
from bs4 import BeautifulSoup
import os.path
import csv
import lxml
from datetime import datetime


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
    for i in range(1, all_pages+1):
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

    attrs = []
    for link in links:
        req = requests.get(url=link, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')
        attributes = soup.find_all(class_='realty_detail_attr')

        dict = {}
        for attr in attributes:
            match attr.find('span').text.strip().replace('\xa0', ''):
                case 'Количество комнат':
                    try:
                        rooms = int(attr.find('b').text.strip())
                    except Exception:
                        rooms = ''
                    dict["rooms"] = rooms
                case 'Общая площадь':
                    try:
                        full_area = float(attr.find('b').text.strip().rstrip('\xa0кв.м'))
                    except Exception:
                        full_area = ''
                    dict['full_area'] = full_area
                case 'жилая':
                    try:
                        living_area = float(attr.find('b').text.strip().rstrip('\xa0кв.м'))
                    except Exception:
                        living_area = ''
                    dict['living_area'] = living_area
                case 'кухня':
                    try:
                        kitchen_area = float(attr.find('b').text.strip().rstrip('\xa0кв.м'))
                    except Exception:
                        kitchen_area = ''
                    dict['kitchen_area'] = kitchen_area
                case 'Этаж/этажность':
                    try:
                        floor_number = int(attr.find(class_='nowrap').text.strip().split('/')[0])
                        floors_in_building = int(attr.find(class_='nowrap').text.strip().split('/')[1])
                    except Exception:
                        floor_number = ''
                        floors_in_building = ''
                    dict['floor_number'] = floor_number
                    dict['floors_in_building'] = floors_in_building
                case 'Отделка':
                    try:
                        repair_type = attr.find(class_='nowrap').text.strip().replace('\xa0', ' ')
                    except Exception:
                        repair_type = ''
                    dict['repair_type'] = repair_type
                case 'Санузел':
                    try:
                        bathroom_type = attr.find(class_='nowrap').find('span').text.strip()
                    except Exception:
                        bathroom_type = ''
                    dict['bathroom_type'] = bathroom_type
                case 'Материал':
                    try:
                        material_type = attr.find(class_='nowrap').text.strip()
                    except Exception:
                        material_type = ''
                    dict['material_type'] = material_type
                case 'Год постройки':
                    try:
                        year_build = int(attr.find(class_='nowrap').text.strip())
                    except Exception:
                        year_build = ''
                    dict['year_build'] = year_build
                case 'Вид':
                    try:
                        flat_type = attr.find(class_='nowrap').text.strip()
                    except Exception:
                        flat_type = ''
                    dict['flat_type'] = flat_type
                case 'Балкон/лоджия':
                    try:
                        balcony_type = attr.find(class_='nowrap').text.strip().replace('\xa0', ' ')
                    except Exception:
                        balcony_type = ''
                    dict['balcony_type'] = balcony_type
        try:
            price = float(soup.find(class_='realty_detail_price').text.strip().rstrip(' руб.').replace('\xa0', ''))

        except Exception:
            price = 0
        dict['price'] = price
        attrs.append(dict)
        print('.')

    field_names = [
        'price',
        'rooms',
        'full_area',
        'living_area',
        'kitchen_area',
        'floor_number',
        'floors_in_building',
        'repair_type',
        'bathroom_type',
        'material_type',
        'year_build',
        'flat_type',
        'balcony_type']

    with open('data/property_info.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        for row in attrs:
            writer.writerow(row)


if __name__ == '__main__':

    all_pages = find_pages()
    print(f'В каталоге найдено {all_pages} страниц.')
    links = get_links(all_pages)
    print('Ссылки на объявления получены. Начинаю парсинг данных.')
    beginning = datetime.now()
    get_data(links)
    diff_time = datetime.now() - beginning
    print(f'Сбор информации окончен. Это заняло {diff_time}.')

