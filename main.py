from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

from environs import Env
import datetime
import pandas
from collections import defaultdict
import configargparse


def get_args_from_user():
	parser = configargparse.ArgumentParser()
	parser.add_argument(
		'-p',
		'--path',
		env_var='EXCEL_PATH',
		required=True,
		type=str,
		help='Пусть к excel файлу, '
		'указывается вместе с именем и расширением файла.'
	)
	parser.add_argument(
		'-s',
		'--sheet_name',
		env_var='SHEET_NAME',
		default=0,
		type=str,
		help='Имя листа в excel файле. '
		'Необходимо указывать, если в файле '
		'больше одного листа.'
	)
	parser.add_argument(
		'-y',
		'--creation_year',
		env_var='CREATION_YEAR',
		default=1913,
		type=int,
		help='Год создания винодельни.'
	)
	args = parser.parse_args()
	return args


def get_age(year):
	creation_date = datetime.datetime(year=year, month=1, day=1)
	now_date = datetime.datetime.now()
	delta_ages = now_date.year - creation_date.year
	return delta_ages


def get_word_for_years(age):
	if age % 100 == 11:
		age_word = 'лет'
	elif age % 10 == 1:
		age_word = 'год'
	elif age % 100 in [12, 13, 14]:
		age_word = 'лет'
	elif age % 10 in [2, 3, 4]:
		age_word = 'года'
	else:
		age_word = 'лет'
	return age_word


def get_winery_age(year):
	winery_age_number = get_age(year)
	winery_age_word = get_word_for_years(winery_age_number)
	winery_age = f'{winery_age_number} {winery_age_word}'
	return winery_age


def get_excel_data(path, sheet_name):
	excel_data = pandas.read_excel(
		io=r'{}'.format(path),
		sheet_name=sheet_name,
		keep_default_na=False
	)
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

	env_params = Env()
	env_params.read_env()

	args = get_args_from_user()

	template = env.get_template('template.html')

	rendered_page = template.render(
		winery_ages=get_winery_age(args.creation_year),
		all_wines=get_excel_data(args.path, args.sheet_name)
	)

	with open('index.html', 'w', encoding='utf8') as file:
		file.write(rendered_page)

	server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
	server.serve_forever()
	return


if __name__ == '__main__':
	main()
