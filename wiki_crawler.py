from bs4 import BeautifulSoup
import requests
import re
from models.country_model import Country
import repos.country_repo as repo

BASE_URL = 'https://ro.wikipedia.org'

CAPITAL = 'capitala'
POPULATION = 'populație'
DENSITY = 'densitate'
AREA = 'suprafață'
NEIGHBOURS = 'vecini'
LANGUAGE = 'limbi oficiale'
TIME_ZONE = 'fus orar'
GOVERNMENT = 'sistem politic'

citations_regex = re.compile('\\[.+?]')
word_regex = re.compile('[^0-9()\\[\\]]+')


def format_text_to_int(text):
    return text.replace(u'\xa0', '').replace(' ', '').replace('.', '').replace(',', '')


def format_text_to_float(text):
    return text.replace(u'\xa0', '').replace(' ', '').replace('.', '').replace(',', '.')


def format_text_time_zone(text):
    text = re.sub(r'\s*\+\s*', '+', text)
    text = re.sub(r'\s*-\s*', '-', text)
    return text


def get_countries(url):
    countries = {}
    # get html of wiki page
    page = requests.get(url=url)
    if page.status_code == 200:
        # parse the html response
        soup = BeautifulSoup(page.text, 'html.parser')
        # get table of countries
        countries_table = soup.find('table')
        # get rows from table
        rows = countries_table.find_all('tr')
        for row in rows:
            try:
                cells = row.find_all('td')
                # get country info
                country_name = cells[1].find('a').text.strip()
                if country_name == 'Globul':
                    break
                country_area = float(format_text_to_float(cells[2].text.strip()))
                country_population = int(format_text_to_int(cells[3].text.strip()))
                country_density = abs(float(format_text_to_float(cells[4].text.strip())))
                country_url = cells[1].find('a')['href']
                country = Country(name=country_name, area=country_area, population=country_population,
                                  density=country_density, capital='', neighbours='', language='', time_zone='',
                                  government='')
                # add country to dict
                countries[country_url] = country
            except (KeyError, AttributeError):
                pass

    return countries


def get_country_info(country_url, country):
    print('Getting information about: %s...' % country.name)
    # get html of wiki page
    page = requests.get(url=country_url)
    if page.status_code == 200:
        # parse the html response
        soup = BeautifulSoup(page.text, 'html.parser')
        # get table of info
        table = soup.find('table', attrs={'class': 'infocaseta'})
        # get rows from table
        rows = table.find_all('tr')
        for row in rows:
            try:
                # get column text
                th_text = row.find('th').text.lower()
                if CAPITAL in th_text:
                    text = {citations_regex.sub('', a.text.strip()) for a in row.find('td').find_all('a')}
                    if len(text) == 0:
                        # look for non anchor text
                        text = row.find('td').text.strip()
                        country.capital = word_regex.search(text).group(0)
                    else:
                        text = {t for t in text if word_regex.fullmatch(t)}
                        country.capital = ','.join(text)
                elif NEIGHBOURS in th_text:
                    text = {citations_regex.sub('', a.text.strip()) for a in row.find('td').find_all('a')}
                    text = {t for t in text if len(t) > 2 and word_regex.fullmatch(t)}
                    country.neighbours = ','.join(text)
                elif LANGUAGE in th_text:
                    text = {a.text.strip() for a in row.find('td').find_all('a')}
                    text = {t for t in text if len(t) > 2 and word_regex.fullmatch(t)}
                    if len(text) == 0:
                        # look for non anchor text
                        text = row.find('td').text.strip()
                        country.language = word_regex.search(text).group(0).lower()
                    else:
                        country.language = ','.join(text).lower()
                elif TIME_ZONE in th_text:
                    text = row.find('td').text.strip()
                    if not re.match('[A-Za-z]', text):
                        text = 'UTC' + text  # add UTC prefix for text like: +2
                    text = format_text_time_zone(text)
                    country.time_zone = citations_regex.sub('', text)
                elif GOVERNMENT == th_text:
                    text = row.find('td').text.strip()
                    country.government = citations_regex.sub('', text)
            except AttributeError:
                pass

    return country


def populate_database(countries):
    countries_obj = []
    for country_url, country in countries.items():
        country = get_country_info(BASE_URL + country_url, country)
        countries_obj.append(country)

    repo.insert_countries(countries_obj)


if __name__ == '__main__':
    populate_database(get_countries(BASE_URL + '/wiki/Lista_țărilor_după_densitatea_populației'))
