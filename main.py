# Import all the required libraries (pd - dataframe, requests - get request, BeautifulSoup - Web Scraping,
# schedule - continue program for desired time)
import keyboard
from numpy import mod
import pandas as pd
from pandas.core.algorithms import mode
import requests
from bs4 import BeautifulSoup
import schedule
from datetime import date



# Class NbaDataGenerator to contain functions which gather data from internet
class NbaDataGenerator():
    def __init__(self, teamname):
        self.teamname = teamname.upper()

    # Gets the stats of all current players of an inputted team
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

    # Gets the last game result of the team inputted
    def getLastGame(self):
        
        URL = 'https://www.basketball-reference.com/teams/' + str(self.teamname) + '/2021.html'
        page = requests.get(URL)
        csvFile = pd.read_csv('test2.csv')
        soup = BeautifulSoup(page.content, 'html.parser')
        meta = soup.find('div', attrs={'id': 'meta'})
        file = open("test2.csv")
        numline = len(file.readlines())
        list_of_a = []
        list_of_p = []
        for last_game in meta.find_all('a'):
            list_of_a.append(last_game.text)
        for ppg in meta.find_all('p'):
            list_of_p.append(ppg)
         
        ppg = ""
        
        
        
        if list_of_a[4][7] == 'L':
            # print('In their last game, ' + self.teamname + ' lost against ' + list_of_a[4][41:46])
            # score_file.write(
            #     'In their last game, ' + self.teamname + ' lost against ' + list_of_a[4][41:46] + ' ' + list_of_a[4][
            #                                                                                        9:16] + '\n')
            final = ""
            againstTeam = ""
            result = ""
            for i in list_of_a[4]:
                if not (i.isspace()):
                    final += i
            
            # print(len(final))
            # print('The score was ' + list_of_a[4][9:16])
            finalscore = 0
            if len(final) == 14:
                finalscore = final[1:8]
                againstTeam = final[11:]
                result = final[0]
                ppgT = list_of_p[6].next.next.next.next
            elif len(final) == 13:
                finalscore = final[1:8]
                againstTeam = final[10:]
                result = final[0]
                ppgT = list_of_p[7].next.next.next.next
            elif len(final) == 12:
                finalscore = final[1:7]
                result = final[0]
                ppgT = list_of_p[5].next.next.next.next
            elif len(final) == 11:
                finalscore = final[1:6]
                result = final[0]
                ppgT = list_of_p[3].next.next.next.next
            
            print(final)
            for i in ppgT:
                if not (i.isspace()):
                    ppg += i
            ppg = ppg[:5]
        
            finalList = ['empty']
            if not(csvFile['TEAM'].isin([self.teamname]).any()):
                Df = pd.DataFrame({'Team':[self.teamname],'Result':[result],'Score':[finalscore],'OPPTeam':[againstTeam], 'Date Checked':date.today().strftime("%d/%m/%Y"), 'PPG':ppg})
                for i in range(numline):
                    Df.index = [str(i+1)]
                Df.to_csv('test2.csv',mode='a', header=False, index=True)
                finalList.append(final)
                

        else:
            print('In their last game, ' + self.teamname + ' beat ' + list_of_a[4][41:46])
            # score_file.write('In their last game, ' + self.teamname + ' beat ' + list_of_a[4][41:46] + ' ' + list_of_a[4][9:16] + '\n')
            print('The score was ' + list_of_a[4][9:16])
        

# These lines are just for easier functionality. Asks questions in the event log. These are optional and aren't needed
onceOrContinuous = input('Would you like the program to run once or run continuously? Yes (1) or No (2) : ')
team = input('Which team would you like details on? Please enter their 3 letter abbreviation: ')
info = input('What info would you like: ALL THE PLAYERS AND THEIR STATS (1) or THE RESULT OF LAST GAME(2): ')

if int(onceOrContinuous) == 1:
    repeatTime = input('How many seconds would you like the program to repeat in? ')
    if int(info) == 2:
        Generator = NbaDataGenerator(team)
        LastGameGenerator = Generator.getLastGame
        schedule.every(int(repeatTime)).seconds.do(LastGameGenerator)
        # print('Press "E" to end the program')
        while True:
            schedule.run_pending()
            ############################
            # Run 'sudo python main.py #
            #     on MAC systems       #
            #   as using keyboard will #
            #   require administrator  #
            #           access         #
            ###########################3

            # if keyboard.is_pressed('E'):
            #     break
    elif int(info) == 1:
        Generator = NbaDataGenerator(team)
        PlayerStatsGenerator = Generator.getPlayersStats
        schedule.every(10).seconds.do(PlayerStatsGenerator)
        print('Press "E" to end the program')
        while True:
            schedule.run_pending()
            # if keyboard.is_pressed('E'):
            #     break
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
