from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

now = datetime.datetime.now()

event1 = datetime.datetime(year=now.year, month=now.month, day=now.day)
event2 = datetime.datetime(year=1920, month=1, day=1)

delta = event1.year-event2.year
print(delta)


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
    case=(year_case())
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
