"""This module is responsible for getting information about countries from Wikipedia and populate the database.

It uses requests for getting a web page,
unidecode to sanitize data,
Beautiful Soup for pulling data out of HTML files.
"""

from bs4 import BeautifulSoup
import requests
import unidecode
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
    """Returns text after removing characters in order to be casted to an integer.

    Parameters
    ----------
    text : str
        the text to be formatted.

    Returns
    -------
    str
        a string formatted to be casted to integer.
    """
    return text.replace(u'\xa0', '').replace(' ', '').replace('.', '').replace(',', '')


def format_text_to_float(text):
    """Returns text after removing and adding characters in order to be casted to a float number.

    Parameters
    ----------
    text : str
        the text to be formatted.

    Returns
    -------
    str
        a string formatted to be casted to float.
    """
    return text.replace(u'\xa0', '').replace(' ', '').replace('.', '').replace(',', '.')


def format_text_time_zone(text):
    """Returns text after removing blank spaces inside time zone text.

    Parameters
    ----------
    text : str
        the text to be formatted.

    Returns
    -------
    str
        a string formatted to match time zone (ex. UTC+2).
    """
    text = re.sub(r'\s*\+\s*', '+', text)
    text = re.sub(r'\s*-\s*', '-', text)
    return text


def get_countries(url):
    """Returns a dictionary containing pairs (key, value) where
    the key is the wiki URL of a country and
    the value is the Country object of the corresponding url,
    having name, area, population and density set from the input url.

    Parameters
    ----------
    url : str
        the URL to wiki page containing a table with countries name, area, population and density.

    Returns
    -------
    dict
        a dictionary containing (key, value) pairs of URL of the country and Country object.
    """
    countries = {}
    # get html of wiki page
    try:
        page = requests.get(url=url)
    except requests.exceptions.ConnectionError:
        print("Connection error!")
        return None

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
    """Returns country filled with information (capital, neighbours, language, time zone and government)
    from the corresponding wiki page, where country_url is the URL of the page.

    Parameters
    ----------
    country_url : str
        the URL to wiki page containing information about the country.
    country : Country
        the Country object to be filled with information from wiki page.

    Returns
    -------
    Country
        the Country object given as parameter after has been filled with information.
    """
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


def unidecode_country(country):
    """Replaces diacritics with corresponding english characters.

    Parameters
    ----------
    country : Country
        the Country object to have fields sanitized.

    Returns
    -------
    Country
        the Country object after fields were sanitized.
    """
    country.name = unidecode.unidecode(country.name)
    country.capital = unidecode.unidecode(country.capital)
    country.neighbours = unidecode.unidecode(country.neighbours)
    country.language = unidecode.unidecode(country.language)
    country.time_zone = unidecode.unidecode(country.time_zone)
    country.government = unidecode.unidecode(country.government)

    return country


def populate_database(countries):
    """Inserts countries into database.

    Parameters
    ----------
    countries : dict
        the dictionary containing (key, value) pairs of URL of the country and Country object.
    """
    countries_obj = []
    for country_url, country in countries.items():
        country = get_country_info(BASE_URL + country_url, country)
        country = unidecode_country(country)
        countries_obj.append(country)

    repo.insert_countries(countries_obj)


if __name__ == '__main__':
    _countries = get_countries(BASE_URL + '/wiki/Lista_țărilor_după_densitatea_populației')
    if _countries is not None:
        populate_database(_countries)
