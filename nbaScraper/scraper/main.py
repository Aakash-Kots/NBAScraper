import pandas as pd
import requests
from datetime import datetime
from bs4 import BeautifulSoup
date = datetime.today().strftime('%Y-%m-%d')

def getPlayersStats(teamName):
    URL = 'https://www.basketball-reference.com/teams/' + str(teamName) + '/2021.html'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    gsw_players = []
    gsw_players_table = soup.find(name='table', attrs={'id': 'per_game'})
    for row in gsw_players_table.find_all('tr')[1:]:
        player = {}
        player['Name'] = row.find('a').text.strip()
        player['Age'] = row.find('td', {'data-stat': 'age'}).text
        player['Min PG'] = row.find('td', {'data-stat': 'mp_per_g'}).text
        player['Field Goal %'] = row.find('td', {'data-stat': 'fg_pct'}).text
        player['Rebounds PG'] = row.find('td', {'data-stat': 'trb_per_g'}).text
        player['Assists PG'] = row.find('td', {'data-stat': 'ast_per_g'}).text
        player['Steals PG'] = row.find('td', {'data-stat': 'stl_per_g'}).text
        player['Blocks PG'] = row.find('td', {'data-stat': 'blk_per_g'}).text
        player['Turnovers PG'] = row.find('td', {'data-stat': 'tov_per_g'}).text
        player['Points PG'] = row.find('td', {'data-stat': 'pts_per_g'}).text
        gsw_players.append(player)

    return(pd.DataFrame(gsw_players).to_string())


def getLastGame(teamName):
    URL = 'https://www.basketball-reference.com/teams/' + str(teamName) + '/2021.html'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    meta = soup.find('div', attrs={'id':'meta'})
    list_of_a = []
    for last_game in meta.find_all('a'):
        list_of_a.append(last_game.text)
    if list_of_a[4][7] == 'L':
        return('In their last game, ' + teamName + ' lost against ' + list_of_a[4][41:46])
    else:
        return('In their last game, ' + teamName + ' beat ' + list_of_a[4][43:46])
        return('The score was ' + list_of_a[4][9:16])
