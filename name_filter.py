from helpers import CsvWriter, read_csv


def filter_names():
    with CsvWriter('arm_names.csv', ('name', 'id')) as csv_writer:
        for name, name_id in read_csv('all_names.csv'):
            full_name = name.split()
            for namelet in (full_name[0], full_name[-1]):
                if not namelet.endswith('Себастьян') and namelet.endswith('ян'):
                    csv_writer.write((name, name_id))


if __name__ == '__main__':
    filter_names()
