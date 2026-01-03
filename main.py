from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

import datetime
import pandas
from pprint import pprint
from collections import defaultdict


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


def get_excel_data():
	excel_data = pandas.read_excel('wine3.xlsx', sheet_name='Лист1', keep_default_na=False)
	wines = excel_data.to_dict('records')

	grouped_wines = defaultdict(list)
	for wine in wines:
		grouped_wines[wine['Категория']].append(wine)
	return grouped_wines


def main():
	env = Environment(
		loader=FileSystemLoader('.'),
		autoescape=select_autoescape(['html', 'xml'])
	)

	template = env.get_template('template.html')

	rendered_page = template.render(
		winery_ages=get_winery_ages(),
		wines = get_excel_data()
	)

	with open('index.html', 'w', encoding='utf8') as file:
		file.write(rendered_page)

	server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
	server.serve_forever()
	return

if __name__ == '__main__':
	main()