import datetime
import json

import requests

from helpers import CsvWriter, which_watch


def collect_names():
    api_url = 'https://ar.culture.ru/api/Person'
    today = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
    beg = datetime.datetime.combine(datetime.date(year=2019, month=1, day=1), datetime.datetime.min.time())
    while beg <= today:
        fin = (beg + datetime.timedelta(days=32)).replace(day=1)
        # url = 'https://ar.culture.ru/api/Person?l=1500&f={"created":{"$gte":"2023-07-01T00:00:00.000Z","$lt":"2023-08-01T00:00:00.000Z"}}&sel=title%20id'
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
        print(response.url + '...')
        for item in response.json()['data']:
            yield item['title']['ru'], item['id']
        beg = fin


@which_watch
def download_names():
    with CsvWriter('all_names.csv', ('name', 'id'), as_dict=False) as csv_writer:
        for row in collect_names():
            csv_writer.write(row)


if __name__ == '__main__':
    download_names()
