import csv
from functools import wraps
import json
import time

import inflect


class CsvWriter:
    def __init__(self, csv_filename, headers=None, as_dict=False):
        print(f"Downloading {csv_filename}...")
        self._csv_filename = csv_filename
        self._headers = headers
        self._as_dict = as_dict
        self._count = 0
        self._writer = self.csv_writer()
        next(self._writer)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def bulk(self, bulk):
        self._count += len(bulk)
        for row in bulk:
            self._writer.send(row)

    def write(self, row):
        self._count += 1
        self._writer.send(row)

    def close(self):
        self._writer.close()
        print(f"Total: {self._count} {inflect.engine().plural('row', self._count)}")

    def csv_writer(self):
        with open(self._csv_filename, 'w', newline='', encoding='utf-8') as handler:
            if self._as_dict:
                first_row = yield
                if not self._headers:
                    self._headers = sorted(first_row.keys())
                writer = csv.DictWriter(handler, fieldnames=self._headers, restval=None)
                writer.writeheader()
                writer.writerow(first_row)
            else:
                writer = csv.writer(handler)
                if self._headers:
                    writer.writerow(self._headers)
            while True:
                writer.writerow((yield))


def read_csv(csv_fname, is_dict=False, delimiter=','):
    with open(csv_fname, newline=str()) as handler:
        if is_dict:
            for row in csv.DictReader(handler, delimiter=delimiter):
                yield row
        else:
            reader = csv.reader(handler, delimiter=delimiter)
            next(reader)
            for row in reader:
                yield row


def dump_utf_json(entries, json_file):
    with open(json_file, 'w', encoding='utf-8') as handler:
        json.dump(entries, handler, ensure_ascii=False, sort_keys=True, indent=2)
    num_entries = len(entries)
    print(f"Dumped {num_entries} {inflect.engine().plural('entry', num_entries)} to {json_file}")


def load_utf_json(json_file):
    with open(json_file, encoding='utf8') as data:
        return json.load(data)


def which_watch(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        def report_time():
            print("'{}' took {}".format(
                func.__name__,
                time.strftime("%H:%M:%S", time.gmtime(time.perf_counter() - start)),
            ))

        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
        except BaseException as e:
            raise e
        else:
            return result
        finally:
            report_time()

    return wrapper
