""""""
import csv


from settings import base_dir, time_stamp


def write_csv_file(csv_table, delimiter=','):
    """
    Input: Nested list csv_table and a string file_name
    Action: Write fields in csv_table into a comma-separated CSV file with the name file_name
    """
    file_name = base_dir / 'csv_files' / f'data_{time_stamp}.csv'

    with open(file_name, 'w', newline='', encoding='UTF-8') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
        for row in csv_table:
            csv_writer.writerow(row)
    return True


def create_table(data):
    """"""
    table = []
    for currency in data:
        row = list(data[currency].values())
        table.append(row)

    first_line = list(list(data.values())[0].keys())
    table.insert(0, first_line)
    return table


def create_csv_file(data: dict[str, dict]):
    csv_table = create_table(data)
    write_csv_file(csv_table)
