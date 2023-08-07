from bs4 import BeautifulSoup
import requests

from helpers import dump_utf_json


def dowload_arm_artists():
    names = list()
    for group in BeautifulSoup(
            requests.get('https://ru.wikipedia.org/wiki/Категория:Художники_Армении').content,
            'lxml',
    ).find_all('div', {'class': 'mw-category-group'})[9:]:
        for name in group.find_all('a', {'href': True}):
            names.append(process_name(name.text))
    dump_utf_json(names, 'wiki_names.json')


def process_name(name):
    if ',' in name:
        return name.split(',')[0]
    return name.split()[0]


if __name__ == '__main__':
    dowload_arm_artists()
