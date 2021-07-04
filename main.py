import pandas as pd
import requests
from bs4 import BeautifulSoup
import schedule


class NbaDataGenerator():
    def __init__(self, teamname):
        self.teamname = teamname

    def getPlayersStats(self):
        URL = 'https://www.basketball-reference.com/teams/' + str(self.teamname) + '/2021.html'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        gsw_players = []
        gsw_players_table = soup.find(name='table', attrs={'id': 'per_game'})
        for row in gsw_players_table.find_all('tr')[1:]:
            player = {'Name': row.find('a').text.strip(), 'Age': row.find('td', {'data-stat': 'age'}).text,
                      'Min PG': row.find('td', {'data-stat': 'mp_per_g'}).text,
                      'Field Goal %': row.find('td', {'data-stat': 'fg_pct'}).text,
                      'Rebounds PG': row.find('td', {'data-stat': 'trb_per_g'}).text,
                      'Assists PG': row.find('td', {'data-stat': 'ast_per_g'}).text,
                      'Steals PG': row.find('td', {'data-stat': 'stl_per_g'}).text,
                      'Blocks PG': row.find('td', {'data-stat': 'blk_per_g'}).text,
                      'Turnovers PG': row.find('td', {'data-stat': 'tov_per_g'}).text,
                      'Points PG': row.find('td', {'data-stat': 'pts_per_g'}).text}
            gsw_players.append(player)

        print(pd.DataFrame(gsw_players).to_string())

    def getLastGame(self):
        # score_file = open('scores', 'a')
        URL = 'https://www.basketball-reference.com/teams/' + str(self.teamname) + '/2021.html'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        meta = soup.find('div', attrs={'id': 'meta'})
        list_of_a = []
        for last_game in meta.find_all('a'):
            list_of_a.append(last_game.text)
        if list_of_a[4][7] == 'L':
            print('In their last game, ' + self.teamname + ' lost against ' + list_of_a[4][41:46])
            # score_file.write(
            #     'In their last game, ' + self.teamname + ' lost against ' + list_of_a[4][41:46] + ' ' + list_of_a[4][
            #                                                                                        9:16] + '\n')
            print('The score was ' + list_of_a[4][9:16])
        else:
            print('In their last game, ' + self.teamname + ' beat ' + list_of_a[4][41:46])
            # score_file.write('In their last game, ' + self.teamname + ' beat ' + list_of_a[4][41:46] + ' ' + list_of_a[4][9:16] + '\n')
            print('The score was ' + list_of_a[4][9:16])


onceOrContinuous = input('Would you like the program to run once or run continuously? Yes (1) or No (2) : ')
team = input('Which team would you like details on? Please enter their 3 letter abbreviation: ')
info = input('What info would you like: ALL THE PLAYERS AND THEIR STATS (1) or THE RESULT OF LAST GAME(2): ')

if int(onceOrContinuous) == 1:
    if int(info) == 2:
        Generator = NbaDataGenerator(team)
        LastGameGenerator = Generator.getLastGame
        schedule.every(10).seconds.do(LastGameGenerator)
        while True:
            schedule.run_pending()
    elif int(info) == 1:
        Generator = NbaDataGenerator(team)
        PlayerStatsGenerator = Generator.getPlayersStats
        schedule.every(10).seconds.do(PlayerStatsGenerator)
        while True:
            schedule.run_pending()
    else:
        print('Wrong number. Please enter 1 or 2 ONLY')
elif int(onceOrContinuous) == 2:
    if int(info) == 1:
        Generator = NbaDataGenerator(str(team))
        Generator.getPlayersStats()
    elif int(info) == 2:
        Generator = NbaDataGenerator(str(team))
        Generator.getLastGame()
    else:
        print('Wrong number. Please enter 1 or 2 ONLY')

# end = False
# while not end:
#
#
#
#     if int(info) == 1:
#         print('')
#         getPlayersStats(team)
#     elif int(info) == 2:
#         print("")
#         getLastGame(team)
#     elif int(info) == 3:
#         print('')
#         getPlayersStats(team)
#         print('')
#         getLastGame(team)
#     else:
#         print("Wrong number entered. Please enter 1, 2 or 3")
#
#     finish = input('Would you like to stop the program? Yes (1) or No (2): \n')
#     if int(finish) == 1:
#         end = True
