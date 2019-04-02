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


def main():
    header()
    html = get_html()
    nba_wiki_table = get_nba_wiki_table(html)
    print('table :', nba_wiki_table)


if __name__ == '__main__':
    main()
