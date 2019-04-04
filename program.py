import requests
from bs4 import BeautifulSoup


def header():
    print('----------------------------')
    print('----------nba wiki----------')
    print('----------------------------')


def get_html():
    url = 'https://en.wikipedia.org/wiki/National_Basketball_Association'
    response = requests.get(url)

    return response.text


def get_nba_wiki_table(html):
    soup = BeautifulSoup(html, 'html.parser')
    nba_wiki_table = soup.body.find_all('table', class_='navbox wikitable')

    return nba_wiki_table


def get_rows(table_html):
    rows = table_html[0].find_all('tr')
    return rows


def get_headers(rows):
    headers = [th.text.strip() for th in rows[0].find_all('th')]
    return headers


def main():
    header()
    html = get_html()
    nba_wiki_table = get_nba_wiki_table(html)
    rows = get_rows(nba_wiki_table)
    print('rows: ', len(rows))

    headers = get_headers(rows)
    print('headers: ', headers)


if __name__ == '__main__':
    main()
