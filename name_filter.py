from helpers import CsvWriter, load_utf_json, read_csv


def filter_names():
    misc = load_utf_json('misc_names.json')
    wiki = load_utf_json('wiki_names.json')
    with CsvWriter('arm_names.csv', ('name', 'id')) as csv_writer:
        for name, name_id in read_csv('all_names.csv'):
            if name == "Александр Рослин":
                continue
            full_name = name.split()
            for namelet in (full_name[0], full_name[-1]):
                if not namelet.endswith('Себастьян'):
                    if namelet == 'Айвазовский' or namelet.endswith('ян') or namelet.endswith('янц') \
                            or namelet in wiki or namelet in misc:
                        csv_writer.write((name, name_id))


if __name__ == '__main__':
    filter_names()
