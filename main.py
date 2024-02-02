import pandas
import utils
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')
winery_age = utils.get_age()
age = utils.get_correct_year_name(winery_age)

drinks = pandas.read_excel('wine3.xlsx', keep_default_na=False)
drinks_by_category = {}
for category in drinks['Категория'].unique():
    drinks_by_category[category] = [drinks.iloc[i].to_dict() for i in range(len(drinks))
                                    if category in drinks.iloc[i].values]

render_page = template.render(
    winery_age=winery_age,
    year_name=age,
    drinks_by_category=utils.sort_dict(drinks_by_category)
)

with open('index.html', 'w', encoding='utf8') as file:
    file.write(render_page)


server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
