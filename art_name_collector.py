import datetime
import json

import requests

from helpers import CsvWriter, which_watch


def collect_names():
    api_url = 'https://ar.culture.ru/api/Person'
    today = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
    beg = datetime.datetime.combine(datetime.date(year=2018, month=1, day=1), datetime.datetime.min.time())
    ids = set()
    while beg <= today:
        fin = (beg + datetime.timedelta(days=32)).replace(day=1)
        print(f"{beg:%Y-%m-%d} - {fin:%Y-%m-%d}")
        response = requests.get(
                api_url,
                params={
                    'l': 1500,
                    'f': json.dumps({'created': {
                        '$gte': f'{beg:%Y-%m-%dT%H:%M:%S.%fZ}',
                        '$lt': f'{fin:%Y-%m-%dT%H:%M:%S.%fZ}',
                    }}),
                    'sel': "title id",
                },
            )
        for item in response.json()['data']:
            name_id = item['id']
            if name_id in ids:
                continue
            ids.add(name_id)
            yield item['title']['ru'], name_id
        beg = fin


@which_watch
def download_names():
    with CsvWriter('all_art_names.csv', ('name', 'id')) as csv_writer:
        for row in collect_names():
            csv_writer.write(row)


if __name__ == '__main__':
    download_names()
