from bs4 import BeautifulSoup
import requests
import re
import models.country_model as model
import repos.country_repo as repo

BASE_URL = 'https://en.wikipedia.org'


def get_countries(url):
    countries = {}
    # get html of wiki page
    page = requests.get(url=url)
    if page.status_code == 200:
        # parse the html response
        soup = BeautifulSoup(page.text, 'html.parser')
        # get table of countries
        countries_table = soup.find('table', attrs={'class': 'sortable wikitable'})
        # get rows from table
        rows = countries_table.find_all('tr')
        for row in rows:
            # select the cell with country names
            cell = row.find('td')
            if cell is not None:
                # get span with country name
                span = cell.find('span')
                if span is not None:
                    try:
                        # get country name
                        country_name = span['id']
                        # get country page url
                        a = cell.find('b').find('a')
                        if a is not None:
                            country_url = a['href']
                            # add country to dict
                            countries[country_name] = country_url
                    except KeyError:
                        pass

    return countries


def get_country_info(country_name, country_url):
    info = {'name': country_name, 'capital': None, 'population': None, 'density': None, 'area': None, 'language': None,
            'time_zone': None, 'government': None}

    number_regex = re.compile('\\d+\\.?\\d*')
    citations_regex = re.compile('\\[.+?]')

    # get html of wiki page
    page = requests.get(url=country_url)
    if page.status_code == 200:
        # parse the html response
        soup = BeautifulSoup(page.text, 'html.parser')
        # get table of info
        table = soup.find('table', attrs={'class': 'infobox geography vcard'})
        # get rows from table
        rows = table.find_all('tr')
        for row in rows:
            try:
                th_text = row.find('th').text.lower()
                if 'capital' in th_text:
                    text = row.find('td').find('a').text.strip()
                    info['capital'] = citations_regex.sub('', text)
                elif 'population' in th_text:
                    text = row.next_sibling.find('td').text.strip().replace(',', '')
                    info['population'] = int(re.search('\\d+', text).group(0))
                elif 'density' in th_text:
                    text = row.find('td').text.strip()
                    info['density'] = float(number_regex.search(text).group(0))
                elif 'area' in th_text:
                    text = row.next_sibling.find('td').text.strip().replace(',', '')
                    info['area'] = float(number_regex.search(text).group(0))
                elif ('official' in th_text or 'national' in th_text) and 'language' in th_text \
                        and 'recognised' not in th_text:
                    languages = set()
                    for a in row.find('td').find_all('a'):
                        text = a.text.strip()
                        if re.match('[A-Za-z]+', text) and len(text) > 2:
                            languages.add(text)
                    if len(languages) == 0:
                        languages.add(row.find('td').text.strip())
                    info['language'] = ','.join(languages)
                elif 'time zone' in th_text:
                    text = row.find('td').text.strip()
                    info['time_zone'] = re.search('UTC(.\\d+)?|GMT(.\\d+)?', text).group(0)
                elif 'government' == th_text:
                    text = row.find('td').text.strip()
                    info['government'] = citations_regex.sub('', text)
            except AttributeError:
                pass

    return info


def populate_database(countries):
    print('Getting info about countries...')
    countries_obj = []
    for country_name, country_url in countries.items():
        country_name = country_name.replace('_', ' ')
        info = get_country_info(country_name, BASE_URL + country_url)
        countries_obj.append(model.Country(name=info['name'], capital=info['capital'], population=info['population'],
                                           density=info['density'], area=info['area'], language=info['language'],
                                           time_zone=info['time_zone'], government=info['government']))
    repo.insert_countries(countries_obj)


if __name__ == '__main__':
    populate_database(get_countries(BASE_URL + '/wiki/List_of_sovereign_states'))
    # print(get_country_info('Ethiopia', BASE_URL + '/wiki/Antigua_and_Barbuda'))
