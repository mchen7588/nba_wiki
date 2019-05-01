import requests
from bs4 import BeautifulSoup
from collections import namedtuple
import pandas as pd
from tabulate import tabulate
import csv
import os

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
    'head_coach',
    'team_wiki',
    'city_wiki',
    'stadium_wiki',
])

BASE_WIKI_URL = 'https://en.wikipedia.org'


def header():
    print('----------------------------')
    print('----------nba wiki----------')
    print('----------------------------')


def get_html(url):
    response = requests.get(url)

    return response.text


def get_table(html, search_query):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.body.find_all('table', class_=search_query)

    return table


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
            continue

        if get_division(row):
            division = get_division(row)

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

    team_wiki_html = get_html(BASE_WIKI_URL + team_wiki)
    team_wiki_table = get_table(team_wiki_html, 'infobox vcard')
    rows_from_team_table = get_rows(team_wiki_table)
    head_coach = get_head_coach(rows_from_team_table)

    team = NBATeamWiki._asdict(NBATeamWiki(
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
        head_coach=head_coach,
        team_wiki=team_wiki,
        city_wiki=city_wiki,
        stadium_wiki=stadium_wiki
    ))

    return team


def get_head_coach(rows_from_team_table):
    row_with_head_coach = None
    for row in rows_from_team_table:
        if row.find('th', text='Head coach'):
            row_with_head_coach = row

    return get_text_from_html(row_with_head_coach.find('a', title=True))


def get_text_from_html(html):
    return html.text.strip() if html else None


def download_nba_csv(nba_wiki_df):
    output_dir = get_folder('output')
    csvfile = os.path.abspath(os.path.join(output_dir, 'wiki-nba_team_info.csv'))
    nba_wiki_df.to_csv(csvfile, index=False, quoting=csv.QUOTE_ALL)
    print('success!!!!!')


def get_folder(folder):
    base = os.path.abspath(os.path.dirname(__file__))
    path = os.path.abspath(os.path.join(base, folder))

    if not os.path.exists(path) or not os.path.isdir(path):
        os.mkdir(folder)

    return path


def main():
    header()
    nba_wiki_html = get_html(BASE_WIKI_URL + '/wiki/National_Basketball_Association')
    nba_wiki_table = get_table(nba_wiki_html, 'navbox wikitable')
    rows_from_nba_table = get_rows(nba_wiki_table)
    # headers = get_headers(rows_from_nba_table[0])
    # print('headers: ', headers)
    all_team_info = get_all_team_info(rows_from_nba_table)
    df = pd.DataFrame(all_team_info)
    print('df.shape: ', df.shape)
    print('df.head: ', tabulate(df.loc[:, :'year_joined'].head()))
    print('min capacity: ', df['stadium_capacity'].min())
    print('max capacity: ', df['stadium_capacity'].max())
    print('total capacity: ', df['stadium_capacity'].sum())
    print(df[['division', 'stadium_capacity']].groupby('division').sum())
    print(tabulate(df.loc[[df['stadium_capacity'].idxmin()], :'stadium_capacity'], headers='keys', tablefmt='psql'))
    print(tabulate(df.loc[[df['stadium_capacity'].idxmax()], :'stadium_capacity'], headers='keys', tablefmt='psql'))
    download_nba_csv(df)
    print('*****END*****')


if __name__ == '__main__':
    main()
