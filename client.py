"""This script is responsible for calling API routes and displaying the response on screen.

It uses requests for calling API routes.
"""

import requests

api_url = 'http://127.0.0.1:5000'


def parse_request(url):
    """Returns a pair (route, payload), where
    route is the path to API and payload is the query string stored in a dictionary (if exists).

    Parameters
    ----------
    url : str
        the URL to be parsed.

    Returns
    -------
    tuple
        a tuple of type:
            (route, payload), if a query string is provided.
            (route, None) if there is no query string.
            (None, None) if provided url is not valid.
    """
    try:
        if '?' in url:
            route, data = url.split('?')
            data = data.split('&')
            payload = {}
            for d in data:
                key, value = d.split('=')
                payload[key] = value
            return route, payload
        else:
            return url, None
    except ValueError:
        print('Invalid route!')
        return None, None


def make_request(route, payload):
    """Makes a call to API route and prints the response.

    Parameters
    ----------
    route : str
        the path to API.
    payload: dict
        the query string stored as a dictionary
    """
    try:
        r = requests.get(url=api_url + route, params=payload)
        if r.status_code == 200:
            print(r.text)
        else:
            print('404 - Not found!')
    except requests.exceptions.ConnectionError:
        print("Couldn't connect to api!")
    except requests.exceptions.InvalidURL:
        print('Invalid route!')


def main():
    """The main loop, where the user type a route and receive a response, displayed on the screen."""
    while True:
        url = input('Insert a route or type exit to end the program: ')
        if url == 'exit':
            break

        route, payload = parse_request(url)
        if route is not None:
            make_request(route, payload)


if __name__ == '__main__':
    main()
