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
            try:
                # select the cell with country names
                cell = row.find('td')
                if 'other states' in cell.text.lower():
                    break
                # get span with country name
                span = cell.find('span')
                # get country name
                country_name = span['id']
                # get country page url
                a = cell.find('b').find('a')
                country_url = a['href']
                # add country to dict
                countries[country_name] = country_url
            except (KeyError, AttributeError):
                pass

    return countries


def get_country_info(country_name, country_url):
    print('Getting information about: %s...' % country_name)

    info = {'name': country_name, 'capital': None, 'population': None, 'density': None, 'area': None, 'language': None,
            'time_zone': None, 'government': None}

    citations_regex = re.compile('\\[.+?]')
    parenthesis_regex = re.compile('\\(.+?\\)')

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
                    text = row.find('td').text.strip()
                    info['capital'] = re.search('[^0-9()\\[\\]]+', text).group(0).strip()
                elif 'population' in th_text:
                    text = row.next_sibling.find('td').text.strip().replace(',', '')
                    info['population'] = int(re.search('\\d+', text).group(0))
                elif 'density' in th_text:
                    text = row.find('td').text.strip().replace(',', '')
                    info['density'] = float(re.search('\\d+\\.?\\d*', text).group(0))
                elif 'area' in th_text:
                    text = row.next_sibling.find('td').text.strip().replace(',', '')
                    info['area'] = float(re.search('\\d+\\.?\\d*', text).group(0))
                elif ('official' in th_text or 'national' in th_text) and 'language' in th_text \
                        and ('recognised' not in th_text and 'minority' not in th_text):
                    found_languages = [a.text.strip() for a in row.find('td').find_all('a')]
                    languages = {text for text in found_languages if re.match('^[A-Za-z\\-\' ]+$', text)
                                 and len(text) > 2 and text != 'de jure' and text != 'de facto'}
                    if len(languages) == 0:
                        text = row.find('td').text.strip()
                        languages.add(citations_regex.sub('', text))
                    info['language'] = ','.join(languages)
                elif 'time zone' in th_text:
                    text = row.find('td').text.strip()
                    info['time_zone'] = re.search('UTC(.\\d+)?|GMT(.\\d+)?', text).group(0).replace('GMT', 'UTC')
                elif 'government' == th_text:
                    text = row.find('td').text.strip().split('\n')[0]
                    info['government'] = parenthesis_regex.sub('', citations_regex.sub('', text))
            except AttributeError:
                pass

    return info


def populate_database(countries):
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
    # print(get_country_info('Romania', BASE_URL + '/wiki/Romania'))
