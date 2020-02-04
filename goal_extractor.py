import re
import aiohttp
from understat import Understat
import csv
from tabulate import tabulate
from CSV_reader import CSV_reader


def teamAbbreviator(full_name):
    if full_name == 'Arsenal FC' or full_name == 'Arsenal':
        return 'ARS'
    elif full_name == 'Aston Villa':
        return 'AVL'
    elif full_name == 'AFC Bournemouth' or full_name == 'Bournemouth':
        return 'BOU'
    elif full_name == 'Brighton & Hove Albion' or full_name == 'Brighton':
        return 'BHA'
    elif full_name == 'Burnley FC' or full_name == 'Burnley':
        return 'BUR'
    elif full_name == 'Chelsea FC' or full_name == 'Chelsea':
        return 'CHE'
    elif full_name == 'Crystal Palace':
        return 'CRY'
    elif full_name == 'Everton FC' or full_name == 'Everton':
        return 'EVE'
    elif full_name == 'Leicester City' or full_name == 'Leicester':
        return 'LEI'
    elif full_name == 'Liverpool FC' or full_name == 'Liverpool':
        return 'LIV'
    elif full_name == 'Manchester City':
        return 'MCI'
    elif full_name == 'Manchester United':
        return 'MUN'
    elif full_name == 'Newcastle United':
        return 'NEW'
    elif full_name == 'Norwich City' or full_name == 'Norwich':
        return 'NOR'
    elif full_name == 'Sheffield United':
        return 'SHU'
    elif full_name == 'Southampton FC' or full_name == 'Southampton':
        return 'SOU'
    elif full_name == 'Tottenham Hotspur' or full_name == 'Tottenham':
        return 'TOT'
    elif full_name == 'Watford FC' or full_name == 'Watford':
        return 'WAT'
    elif full_name == 'West Ham United' or full_name == 'West Ham':
        return 'WHU'
    elif full_name == 'Wolverhampton Wanderers':
        return 'WOL'


async def update_goalscorers():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        players_list = await understat.get_league_players('epl', 2019)
        relevant_data = []
        for player in players_list:
            if '&#039;' in player['player_name']:
                player['player_name'] = player['player_name'].replace('&#039;', '\'')
            if len(player['player_name'].split(' ')[-1]) > 13:
                split = re.split('\W+', player['player_name'])
                player['player_name'] = ''
                for sub_name in split:
                    player['player_name'] += sub_name[0]
            relevant_data.append([player['player_name'], teamAbbreviator(player['team_title']), player['goals'], player['assists']])
        with open('goalscorers.csv', mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            for row in relevant_data:
                writer.writerow(row)


def list_goalscorers():
    data = CSV_reader('goalscorers.csv')
    data.sort(key=lambda x: int(x[2]), reverse=True)
    top = []
    for i in range(15):
        top.append([data[i][0], data[i][2], data[i][3]])
    print(tabulate(top, ['Name', 'G', 'A'], tablefmt='orgtbl'))


def list_goalscorers_2():
    data = CSV_reader('goalscorers.csv')
    data.sort(key=lambda x: int(x[2]), reverse=True)
    top = []
    for i in range(25):
        top.append([data[i][0].split(' ')[len(data[i][0].split(' ')) - 1], data[i][2], data[i][3]])
    return top


def list_assisters():
    data = CSV_reader('goalscorers.csv')
    data.sort(key=lambda x: int(x[3]), reverse=True)
    top = []
    for i in range(15):
        top.append([data[i][0], data[i][2], data[i][3]])
    print(tabulate(top, ['Name', 'G', 'A'], tablefmt='orgtbl'))


def list_assisters_2():
    data = CSV_reader('goalscorers.csv')
    data.sort(key=lambda x: int(x[3]), reverse=True)
    top = []
    for i in range(25):
        top.append([data[i][0].split(' ')[len(data[i][0].split(' ')) - 1], data[i][2], data[i][3]])
    return top
