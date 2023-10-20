from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
from pprint import pprint
import collections

# first_excel_file = pandas.read_excel('wine.xlsx')
# wine_dictionary = first_excel_file.to_dict()
#
#
# dict_list = list(wine_dictionary.values())
# internal_dict = dict_list[0]
# wines_list = []
# for wine in internal_dict:
#     result = {}
#     for key in wine_dictionary:
#         dict_value = wine_dictionary[key]
#         null_value = dict_value[wine]
#         result[key] = null_value
#     wines_list.append(result)


second_excel_file = pandas.read_excel('wine2.xlsx', keep_default_na=False)
second_file_dict = second_excel_file.to_dict(orient='records')

category_dict = collections.defaultdict(list)
for key in second_file_dict:
    category = key['Категория']
    category_dict[category].append(key)
print(category_dict)


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

now = datetime.datetime.now()

event1 = datetime.datetime(year=now.year, month=now.month, day=now.day)
event2 = datetime.datetime(year=1920, month=1, day=1)

delta = event1.year-event2.year


def year_case():
    age = delta
    if (age % 10 == 1) and (age != 11) and (age % 100 != 11):
        return "год"
    elif (age % 10 > 1) and (age % 10 < 5) and (age != 12) and (age != 13) and (age != 14):
        return "года"
    else:
        return "лет"


rendered_page = template.render(
    year=delta,
    case=year_case(),
    wines=category_dict)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
