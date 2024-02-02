import pandas
import utils
import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from collections import defaultdict

parser = argparse.ArgumentParser('wine store site\n')
parser.add_argument('filename', default='wine.xlsx', nargs='?',
                    help='name of the file, that contains description of wines')
args = parser.parse_args()

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')
winery_age = utils.get_age()
age = utils.get_correct_year_name(winery_age)

eng_column = {
    'Категория': 'category',
    'Название': 'name',
    'Сорт': 'variety',
    'Цена': 'price',
    'Картинка': 'picture',
    'Акция': 'promotion'
}
drinks = pandas.read_excel(args.filename, keep_default_na=False).rename(columns=eng_column)
drinks_by_category = defaultdict(list)
for drink in drinks.to_dict(orient='records'):
    drinks_by_category[drink['category']].append(drink)

render_page = template.render(
    winery_age=winery_age,
    year_name=age,
    drinks_by_category=utils.sort_dict(drinks_by_category)
)

with open('index.html', 'w', encoding='utf8') as file:
    file.write(render_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
