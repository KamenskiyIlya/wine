from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

import datetime


def get_winery_ages():
	creation_date = datetime.datetime(year=1913, month=1, day=1)
	now_date = datetime.datetime.now()
	delta_ages = now_date.year - creation_date.year
	if delta_ages%100 == 11:
		winery_ages = f'{delta_ages} лет'
	elif delta_ages%10 == 1:
		winery_ages = f'{delta_ages} год'
	elif delta_ages%100 in [12,13,14]:
		winery_ages = f'{delta_ages} лет'
	elif delta_ages%10 in [2,3,4]:
		winery_ages = f'{delta_ages} года'
	else:
		winery_ages = f'{delta_ages} лет'
	return winery_ages

env = Environment(
	loader=FileSystemLoader('.'),
	autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
	winery_ages=get_winery_ages()
)

with open('index.html', 'w', encoding='utf8') as file:
	file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
