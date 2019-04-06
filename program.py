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

    # print(Counter([len(row.find_all('td')) for row in rows]))
    celtics = rows[3].find_all('td')
    team_name = celtics[0].get_text().strip()
    team_wiki = celtics[0].a['href']
    print('team_name: ', team_name)
    print('team_wiki: ', team_wiki)
    city, state = celtics[1].get_text().strip().split(',')
    city_wiki = celtics[1].find_all('a')[0]['href']
    print('city: ', city)
    print('state: ', state)
    print('city_wiki: ', city_wiki)
    stadium = celtics[2].get_text().strip()
    stadium_wiki = celtics[2].a['href']
    print('stadium: ', stadium)
    print('stadium_wiki: ', stadium_wiki)
    stadium_capacity = celtics[3].get_text().strip()
    print('stadium_capacity: ', stadium_capacity)
    coordinate = celtics[4].find('span', class_='geo').get_text()
    lat, lon = (float(x) for x in coordinate.split(';'))
    print('lat: ', lat)
    print('lon: ', lon)
    year_founded = int(celtics[5].get_text().replace('*', ''))
    print('year_founded: ', year_founded)
    year_joined = int(celtics[-1].get_text())
    print('year_joined: ', year_joined)


if __name__ == '__main__':
    main()
