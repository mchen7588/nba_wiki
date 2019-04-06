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


def get_headers(header_row):
    headers = [get_text_from_html(th) for th in header_row.find_all('th')]
    return headers


def get_conference(row):
    conference = row.find('th', colspan=True)
    print(get_text_from_html(conference))


def get_division(row):
    division = row.find('th', rowspan=True)
    print(get_text_from_html(division))


def get_text_from_html(html):
    return html.text.strip() if html else None


def main():
    header()
    html = get_html()
    nba_wiki_table = get_nba_wiki_table(html)
    rows = get_rows(nba_wiki_table)
    print('rows: ', len(rows))

    headers = get_headers(rows[0])
    print('headers: ', headers)

    get_conference(rows[1])  # East
    get_conference(rows[17])  # West

    get_division(rows[2])  # Atlantic
    get_division(rows[7])  # Central
    get_division(rows[12])  # Southeast
    get_division(rows[18])  # Northwest
    get_division(rows[23])  # Pacific
    get_division(rows[28])  # Southwest


if __name__ == '__main__':
    main()
