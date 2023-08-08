import json
import os
import shutil
from urllib.parse import urljoin

import inflect
import requests

from global_vars import ARCULT_METADATA, ARM_ART_NAMES
from helpers import dump_utf_json, read_csv, which_watch


class Downloader:
    def __init__(self, filename=ARCULT_METADATA, write_meta=True, download_jpg=True):
        self.filename = filename
        self.write_meta = write_meta
        self.download_jpg = download_jpg
        self.path = None
        if self.download_jpg:
            self.path = os.path.join(os.sep, 'opt', 'opendata_am', 'arcult')
            shutil.rmtree(self.path, ignore_errors=True)
            os.mkdir(self.path)
        self.api_url = 'https://ar.culture.ru/api/Subject'
        self.metadata = dict()
        self.num_processed = self.num_empty = self.num_downloaded = 0

    def collect_metadata(self, art_slug, raw_metadata):
        self.metadata[art_slug] = [{
            'id': raw_metadatum['_id'],
            'title': raw_metadatum['title'],
            'slug': raw_metadatum['slug'],
            'image': raw_metadatum['topImage']['attachment']['original'],
        } for raw_metadatum in raw_metadata]

    def download_images(self, art_slug, raw_metadata):
        target_path = os.path.join(os.sep, self.path, art_slug)
        os.mkdir(target_path)
        for metadatum in raw_metadata:
            print(f"\t...{metadatum['title']['ru']}")
            slug = metadatum['slug']
            src_path = urljoin(
                'https://ar.culture.ru/attachments/',
                metadatum['topImage']['attachment']['original']['path'],
            )
            target_filename = os.path.join(os.sep, target_path, f'{slug}.{src_path.rsplit(".", 1)[-1]}')
            with open(target_filename, 'wb') as handler:
                handler.write(requests.get(src_path).content)
            self.num_downloaded += 1

    @which_watch
    def main(self):
        print(f"{ARM_ART_NAMES} -> {self.filename}...")
        rows = list(read_csv(ARM_ART_NAMES))
        for name, art_id, art_slug in rows:
            response = requests.get(self.api_url, params={
                'f': json.dumps({'authors': art_id}),
                'sel': "title topImage slug",
            })
            print(name + '...')
            raw_metadata = response.json()['data']
            if not raw_metadata:
                self.num_empty += 1
                continue
            self.num_processed += 1
            if self.write_meta:
                self.collect_metadata(art_slug, raw_metadata)
            if self.download_jpg:
                self.download_images(art_slug, raw_metadata)
        print(f"Processed {self.num_processed} / {len(rows)}, "
              f"{self.num_empty} are empty; "
              f"downloaded {self.num_downloaded} {inflect.engine().plural('image', self.num_downloaded)} ")
        dump_utf_json(self.metadata, self.filename)


if __name__ == '__main__':
    Downloader().main()
