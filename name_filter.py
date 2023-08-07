from operator import itemgetter

from helpers import CsvWriter, load_utf_json, read_csv


def filter_names():
    ref = {name for filename for name in }
    misc, wiki, typical = (load_utf_json(filename) for filename in (
        'misc_arm_art_names.json',
        'wiki_art_names.json',
        'wiki_arm_typical_names.json',
    ))
    filtered = list()
    for name, name_id in read_csv('all_names.csv'):
        if name == "Александр Рослин":
            continue
        full_name = name.split()
        for namelet in (full_name[0], full_name[-1]):
            if not namelet.endswith('Себастьян'):
                if namelet.endswith('ян') or namelet.endswith('янц') or namelet in wiki or namelet in misc:
                    filtered.append((name, name_id))
    filtered.sort(key=itemgetter(0))
    with CsvWriter('arm_art_names.csv', ('name', 'id')) as csv_writer:
        csv_writer.bulk(filtered)


if __name__ == '__main__':
    filter_names()
