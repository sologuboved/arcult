from bs4 import BeautifulSoup
import requests

from helpers import dump_utf_json


def dowload_arm_typical_names(lower):
    names = set()
    for name in BeautifulSoup(
            requests.get('https://ru.wiktionary.org/wiki/Категория:Армянские_фамилии/ru').content,
            'lxml',
    ).find('div', {'dir': 'ltr'}).find_all('a', {'href': True})[:-1]:
        name = name.text
        names |= process_name(name, lower)
    excl = {'Абрамов', 'Бабаев', 'Григорьев', 'Захаров', 'Мурадов', 'Мясников', 'Оников', 'Самсонов', 'Симонов'}
    if lower:
        names -= {name.lower() for name in excl}
    else:
        names -= excl
    dump_utf_json(sorted(list(names)), 'wiki_arm_typical_names.json')


def process_name(name, lower):
    if lower:
        name = name.lower()
    if name[-2:] in ('ов', 'ев'):
        return {name}
    names = set()
    if name.endswith('ц'):
        names.add(name + 'ев')
        name = name[:-1]
    if name.endswith('ян'):
        names.add(name + 'ов')
        name = name[:-2]
        if name[-1] in ('а', 'е', 'ё', 'и', 'о', 'у', 'ю', 'э', 'ы', 'я', 'й', 'ц', 'ч', 'ш', 'щ', 'ь'):
            names.add(name + 'ев')
        if name[-1] == 'ь':
            names.add(name[:-1] + 'ов')
        else:
            names.add(name + 'ов')
    return names


if __name__ == '__main__':
    dowload_arm_typical_names(True)
