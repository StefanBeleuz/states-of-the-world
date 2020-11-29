from bs4 import BeautifulSoup
import requests

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


def populate_database(countries):
    pass


if __name__ == '__main__':
    print(get_countries(BASE_URL + '/wiki/List_of_sovereign_states'))
