import requests
from bs4 import BeautifulSoup
from collections import namedtuple, Counter

NBATeamWiki = namedtuple('NBATeamWiki', [
    'name',
    'conference',
    'division',
    'city',
    'state',
    'stadium_name',
    'stadium_capacity',
    'stadium_lat',
    'stadium_lon',
    'year_founded',
    'year_joined',
    'team_wiki',
    'city_wiki',
    'stadium_wiki',
])


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


def get_all_team_info(rows_from_nba_table):
    all_team_info = []
    conference = ''
    division = ''

    for row in rows_from_nba_table[1:]:

        if get_conference(row):
            conference = get_conference(row)
            # print('CONFERENCE: ', conference)
            continue

        if get_division(row):
            division = get_division(row)
            # print('DIVISION: ', division)

        all_team_info.append(get_team_info(row, conference, division))

    return all_team_info


def get_conference(row):
    conference = row.find('th', colspan=True)
    return get_text_from_html(conference)


def get_division(row):
    division = row.find('th', rowspan=True)
    return get_text_from_html(division)


def get_team_info(row, conference=None, division=None):
    team_data = row.find_all('td')
    team_name = get_text_from_html(team_data[0])
    team_wiki = team_data[0].a['href']

    city, state = get_text_from_html(team_data[1]).split(',')
    city_wiki = team_data[1].find_all('a')[0]['href']

    stadium_name = get_text_from_html(team_data[2])
    stadium_wiki = team_data[2].a['href']
    stadium_capacity = int(get_text_from_html(team_data[3]).replace(',', ''))

    coordinate = team_data[4].find('span', class_='geo').get_text()
    lat, lon = (float(x) for x in coordinate.split(';'))

    year_founded = int(get_text_from_html(team_data[5]).replace('*', ''))
    year_joined = int(get_text_from_html(team_data[-1]).replace('*', ''))

    team = NBATeamWiki(
        name=team_name,
        conference=conference,
        division=division,
        city=city,
        state=state,
        stadium_name=stadium_name,
        stadium_capacity=stadium_capacity,
        stadium_lat=lat,
        stadium_lon=lon,
        year_founded=year_founded,
        year_joined=year_joined,
        team_wiki=team_wiki,
        city_wiki=city_wiki,
        stadium_wiki=stadium_wiki
    )

    # print('TEAM: ', team)
    return team


def get_team_html(url):
    response = requests.get(url)

    return response.text


def get_team_wiki_table(html):
    soup = BeautifulSoup(html, 'html.parser')
    team_wiki_table = soup.body.find_all('table', class_="infobox vcard")

    print('team_wiki_table', team_wiki_table)


def get_text_from_html(html):
    return html.text.strip() if html else None


def main():
    header()
    html = get_html()
    nba_wiki_table = get_nba_wiki_table(html)
    rows_from_nba_table = get_rows(nba_wiki_table)
    # headers = get_headers(rows_from_nba_table[0])
    # print('headers: ', headers)
    all_team_info = get_all_team_info(rows_from_nba_table)
    # print('##########COUNT: ', len(all_team_info))
    # print('##########ALL: ', all_team_info)

    team_html = get_team_html('https://en.wikipedia.org/wiki/Atlanta_Hawks')
    get_team_wiki_table(team_html)


if __name__ == '__main__':
    main()
