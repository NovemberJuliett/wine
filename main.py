from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
import argparse


def incline_years(age):
    if (age % 10 == 1) and (age != 11) and (age % 100 != 11):
        return "год"
    if (age % 100 > 10) and (age % 100 < 20):
        return "лет"
    if (age % 10 > 1) and (age % 10 < 5):
        return "года"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="Путь до файла")
    args = parser.parse_args()
    file_path = args.file_path
    excel_file = pandas.read_excel(file_path, keep_default_na=False)
    excel_file_dict = excel_file.to_dict(orient='records')

    category_dict = collections.defaultdict(list)
    for column_name in excel_file_dict:
        category = column_name['Категория']
        category_dict[category].append(column_name)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    now = datetime.datetime.now()
    event1 = datetime.datetime(year=now.year, month=now.month, day=now.day)
    event2 = datetime.datetime(year=1920, month=1, day=1)
    delta = event1.year - event2.year

    rendered_page = template.render(
        year=delta,
        case=incline_years(delta),
        wines=category_dict)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
