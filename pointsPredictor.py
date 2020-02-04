import time
import math
import csv
import asyncio
import aiohttp
from understat import Understat
from tabulate import tabulate
from CSV_reader import CSV_reader
import pickle
from goal_extractor import teamAbbreviator
from FPL_future import scorePredictor
from tqdm import tqdm
from colorama import Fore, init

init(autoreset=True)


class _PlayerForm:

    def __init__(self, name, team, xG, xA, xGr, xAr, id):
        self.name = name
        self.goal_ratio = xGr
        self.assist_ratio = xAr
        self.player_id = id
        self.team = team
        self.xG = xG
        self.xA = xA


class _TeamForm:

    def __init__(self, team, xG, id):
        self.team_id = id
        self.team = team
        self.xG = xG


class LeagueForm:

    def __init__(self):
        self.players = {}
        self.teams = {}

    def addPlayer(self, name, team, xGr, xG, xAr, xA, id):
        self.players[name] = _PlayerForm(name, team, xG, xA, xGr, xAr, id)

    def addTeam(self, team, xG, id):
        self.teams[team] = _TeamForm(team, xG, id)


class _Player:

    def __init__(self, name, team, pos, G, xG, A, xA, id):
        self.name = name
        self.position = pos
        self.goals = G
        self.assists = A
        self.player_id = id
        self.team = team
        self.xG = xG
        self.xA = xA


class _Team:

    def __init__(self, team, xG, id):
        self.team_id = id
        self.team = team
        self.xG = xG


class League:

    def __init__(self):
        self.players = {}
        self.teams = {}

    def addPlayer(self, name, team, pos, G, xG, A, xA, id):
        self.players[name] = _Player(name, team, pos, G, xG, A, xA, id)

    def addTeam(self, team, xG, id):
        self.teams[team] = _Team(team, xG, id)


teams = ['Manchester City', 'Manchester United', 'Watford', 'Leicester', 'Crystal Palace', 'Bournemouth', 'Burnley',
         'Wolverhampton Wanderers', 'Brighton', 'Southampton', 'West Ham', 'Arsenal', 'Everton', 'Newcastle United',
         'Chelsea', 'Liverpool', 'Tottenham', 'Sheffield United', 'Aston Villa', 'Norwich']
data = CSV_reader('player_data.csv')
names = data[0]
positions = data[1]


def positionfunction(position):
    if position == 'D' or position == 'D S' or position == 'D M S' or position == 'D M':
        return 'D'
    elif position == 'M' or position == 'M S' or position == 'F M' or position == 'D F M S':
        return 'M'
    elif position == 'GK' or position == 'GK S':
        return 'G'
    elif position == 'F M S' or position == 'F S' or position == 'S' or position == 'F':
        return 'A'
    else:
        print(position)
        return None


async def update_Total(league):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        print(Fore.RED + 'Extracting season data')
        for team in tqdm(teams):
            players = await understat.get_league_players("epl", 2019, team_title=team)
            for player in players:
                if int(player['games']) > 9:
                    if player['player_name'] in names:
                        pos = positions[names.index(player['player_name'])]
                        league.addPlayer(player['player_name'], player['team_title'], pos,
                                         player['goals'], player['xG'], player['assists'], player['xA'], player['id'])
                    else:
                        names.append(player['player_name'])
                        positions.append(positionfunction(player['position']))
                        with open('player_data.csv', mode='w', newline='', encoding='utf-8-sig') as file:
                            writer = csv.writer(file)
                            writer.writerow(names)
                            writer.writerow(positions)
                        league.addPlayer(player['player_name'], player['team_title'], pos,
                                         player['goals'], player['xG'], player['assists'], player['xA'], player['id'])
        teams_league = await understat.get_teams('epl', 2019)
        for j in range(20):
            xG = 0
            for i in range(len(teams_league[j]['history'])):
                xG += teams_league[j]['history'][i]['xG']
            league.addTeam(teams_league[j]['title'], xG, teams_league[j]['id'])
    with open('player_data.pkl', 'wb') as output:
        pickle.dump(league, output, pickle.HIGHEST_PROTOCOL)


def xGPrinter(team):
    with open('player_data.pkl', 'rb') as input:
        premier_league = pickle.load(input)
    for team_name, team_object in premier_league.teams.items():
        if team_name == team:
            return team_object.xG
    return None


async def update_Form(league, form):
    games_no = int(CSV_reader('code_settings.csv')[0][0])
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        teams_league = await understat.get_teams('epl', 2019)
        for j in range(20):
            xG = 0
            for i in range(len(teams_league[j]['history']) - games_no, len(teams_league[j]['history'])):
                xG += teams_league[j]['history'][i]['xG']
            form.addTeam(teams_league[j]['title'], xG, teams_league[j]['id'])
        print(Fore.RED + 'Updating player form data')
        time.sleep(0.5)
        for key, player in tqdm(league.players.items()):
            recent_matches = await understat.get_player_matches(player.player_id)
            recent_matches = recent_matches[:games_no]
            xG = 0
            xA = 0
            G = 0
            A = 0
            for i in range(games_no):
                if len(recent_matches) > games_no - 1:
                    xG += float(recent_matches[i]['xG'])
                    xA += float(recent_matches[i]['xA'])
                    G += float(recent_matches[i]['goals'])
                    A += float(recent_matches[i]['assists'])
            xGr = xG / form.teams[player.team].xG
            xAr = xA / form.teams[player.team].xG
            form.addPlayer(player.name, player.team, xGr, xG, xAr, xA, player.player_id)
        with open('recent_data.pkl', 'wb') as output:
            pickle.dump(form, output, pickle.HIGHEST_PROTOCOL)


def ConcededPointsLost(lambda_value):
    exp_points_lost = 0
    for x in range(20):
        prob_GC_is_x = (lambda_value ** x) * math.exp(- lambda_value) / math.factorial(x)
        exp_points_lost += math.floor(x / 2) * prob_GC_is_x
    return exp_points_lost


def pointsPredictor(GW, league, form):
    sheet = CSV_reader('FPL_Fixtures.csv')  # still to fix
    teams = ['ARS', 'AVL', 'BOU', 'BHA', 'BUR', 'CHE', 'CRY', 'EVE', 'LEI', 'LIV', 'MCI', 'MUN', 'NEW', 'NOR',
             'SHU', 'SOU', 'TOT', 'WAT', 'WHU', 'WOL']
    fixtures = []
    xGF = []
    xGA = []
    for i in range(20):
        fixtures.append(sheet[GW][i])
    for team in teams:
        opponent = fixtures[teams.index(team)]
        if '&' in opponent:
            x = opponent.split('&')
            yxGF = []
            yxGA = []
            for opponent in x:
                if '(H)' in opponent:
                    opponent = opponent.replace(' (H)', '')
                    score = scorePredictor(team, opponent)
                    yxGF.append(score[0])
                    yxGA.append(score[1])
                elif '(A)' in opponent:
                    opponent = opponent.replace(' (A)', '')
                    score = scorePredictor(opponent, team)
                    yxGF.append(score[1])
                    yxGA.append(score[0])
            xGF.append(yxGF)
            xGA.append(yxGA)
        elif '(H)' in opponent:
            opponent = opponent.replace(' (H)', '')
            score = scorePredictor(team, opponent)
            xGF.append(score[0])
            xGA.append(score[1])
        elif '(A)' in opponent:
            opponent = opponent.replace(' (A)', '')
            score = scorePredictor(opponent, team)
            xGF.append(score[1])
            xGA.append(score[0])
    names = []
    xPoints = []
    for key, player in form.players.items():
        names.append(player.name)
        if league.players[player.name].position == 'D':
            team_index = teams.index(teamAbbreviator(player.team))
            try:
                if isinstance(xGF[team_index], list):
                    xPoints.append(
                        round(xGF[team_index][0] * (6 * player.goal_ratio + 2.25 * player.assist_ratio) + 4 * math.exp(
                            - xGA[team_index][0]) - ConcededPointsLost(xGA[team_index][0]) + 2
                            + xGF[team_index][1] * (6 * player.goal_ratio + 2.25 * player.assist_ratio) + 4 * math.exp(
                            - xGA[team_index][1]) - ConcededPointsLost(xGA[team_index][1]) + 2, 2))
                else:
                    xPoints.append(
                        round(xGF[team_index] * (6 * player.goal_ratio + 2.25 * player.assist_ratio) + 4 * math.exp(
                            - xGA[team_index]) - ConcededPointsLost(xGA[team_index]) + 2, 2))
            except IndexError:
                xPoints.append(0)
        elif league.players[player.name].position == 'M':
            team_index = teams.index(teamAbbreviator(player.team))
            try:
                if isinstance(xGF[team_index], list):
                    xPoints.append(
                        round(xGF[team_index][0] * (5 * player.goal_ratio + 2.25 * player.assist_ratio) + math.exp(
                            - xGA[team_index][0]) + 2 +
                            xGF[team_index][1] * (5 * player.goal_ratio + 2.25 * player.assist_ratio) + math.exp(
                            - xGA[team_index][1]) + 2, 2))
                else:
                    xPoints.append(
                        round(xGF[team_index] * (5 * player.goal_ratio + 2.25 * player.assist_ratio) + math.exp(
                            - xGA[team_index]) + 2, 2))
            except IndexError:
                xPoints.append(0)
        elif league.players[player.name].position == 'A':
            team_index = teams.index(teamAbbreviator(player.team))
            try:
                if isinstance(xGF[team_index], list):
                    xPoints.append(
                        round(xGF[team_index][0] * (4 * player.goal_ratio + 2.25 * player.assist_ratio) + 2 +
                        xGF[team_index][1] * (4 * player.goal_ratio + 2.25 * player.assist_ratio) + 2, 2))
                else:
                    xPoints.append(
                        round(xGF[team_index] * (4 * player.goal_ratio + 2.25 * player.assist_ratio) + 2, 2))
            except IndexError:
                xPoints.append(0)
        else:
            team_index = teams.index(teamAbbreviator(player.team))
            try:
                if isinstance(xGF[team_index], list):
                    xPoints.append(
                        round(xGF[team_index][0] * (6 * player.goal_ratio + 2.25 * player.assist_ratio) + 4 * math.exp(
                            - xGA[team_index][0]) - ConcededPointsLost(xGA[team_index][0]) + 2 +
                            xGF[team_index][1] * (6 * player.goal_ratio + 2.25 * player.assist_ratio) + 4 * math.exp(
                            - xGA[team_index][1]) - ConcededPointsLost(xGA[team_index][1]) + 2, 2))
                else:
                    xPoints.append(
                        round(xGF[team_index] * (6 * player.goal_ratio + 2.25 * player.assist_ratio) + 4 * math.exp(
                            - xGA[team_index]) - ConcededPointsLost(xGA[team_index]) + 2, 2))
            except IndexError:
                xPoints.append(0)
    array = []
    for i in range(len(names)):
        array.append([names[i], xPoints[i]])
    return array


def pointsLost(num, pos):
    if pos == 'A' or pos == 'M':
        return 9 * math.log(num + 2.24) - 7.6
    else:
        return 9 * math.log(num + 1.33) - 4


def runPredictor(reload):
    if reload:
        premier_league = League()
        premier_league_form = LeagueForm()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(update_Total(premier_league))
        loop.run_until_complete(update_Form(premier_league, premier_league_form))
        return None
    else:
        with open('player_data.pkl', 'rb') as file:
            premier_league = pickle.load(file)
        with open('recent_data.pkl', 'rb') as file:
            premier_league_form = pickle.load(file)
    gameweek = int(input('Gameweek: '))
    X = input('View expected top N performers. Enter number or \'all\': ').upper()
    if X == 'ALL':
        print(tabulate(pointsPredictor(gameweek, premier_league, premier_league_form).sort(key=lambda x: x[1], reverse=True), ['Name', 'xPoints']))
    else:
        print(tabulate(pointsPredictor(gameweek, premier_league, premier_league_form)[:int(X)].sort(key=lambda x: x[1], reverse=True), ['Name', 'xPoints']))


def runPredictor_3(start, finish, N):
    with open('player_data.pkl', 'rb') as file:
        premier_league = pickle.load(file)
    with open('recent_data.pkl', 'rb') as file:
        premier_league_form = pickle.load(file)
    points_list = []
    data_list = []
    for gw in range(start, finish + 1):
        data = pointsPredictor(gw, premier_league, premier_league_form)
        data_list.append(data)
    for playerid in range(len(data_list[0])):
        points = 0
        for gwno in range(len(data_list)):
            points += data_list[gwno][playerid][1]
        points_list.append([data_list[0][playerid][0], round(points, 1)])
    points_list.sort(key=lambda x: x[1], reverse=True)
    points_list = points_list[:N]
    col1 = '[color=#FFFF00]Name[color=#FFFFFF]'
    col2 = '[color=#FFFF00]xPts[color=#FFFFFF]'
    for i in range(len(points_list)):
        col1 += '\n' + points_list[i][0]
        col2 += '\n' + str(points_list[i][1])
    return [col1, col2]
