from operator import itemgetter

from helpers import CsvWriter, load_utf_json, read_csv


def filter_names():
    ref = {name for src in [load_utf_json(filename) for filename in (
        'misc_arm_art_names.json',
        'wiki_arm_art_names.json',
        'wiki_arm_typical_names.json',
    )] for name in src}
    filtered = list()
    for row in read_csv('all_art_names.csv'):
        name = row[0]
        if name == "Александр Рослин":
            continue
        name = name.split()
        for namelet in (name[0], name[-1]):
            if not namelet.endswith('Себастьян'):
                if namelet.endswith('ян') or namelet.endswith('янц') or namelet in ref:
                    filtered.append(row)
    filtered.sort(key=itemgetter(0))
    with CsvWriter('arm_art_names.csv', ('name', 'id', 'slug')) as csv_writer:
        csv_writer.bulk(filtered)


if __name__ == '__main__':
    filter_names()
