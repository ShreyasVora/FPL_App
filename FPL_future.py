import math
import numpy as np
from CSV_reader import CSV_reader
from tabulate import tabulate
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from colorama import init, Fore

init(autoreset=True)


class Implementation:
    """
    A class that represents an implementation of the Elo Rating System
    """

    def __init__(self, base_rating=1000):
        """
        Runs at initialization of class object.
        :param base_rating - The rating a new player would have
        """
        self.base_rating = base_rating
        self.players = []

    def __getPlayerList(self):
        """
        Returns this implementation's player list.
        :return - the list of all player objects in the implementation.
        """
        return self.players

    def getPlayer(self, name):
        """
        Returns the player in the implementation with the given name.
        :param name - name of the player to return.
        :return - the player with the given name.
        """
        for player in self.players:
            if player.name == name:
                return player
        return None

    def contains(self, name):
        """
        Returns true if this object contains a player with the given name.
        Otherwise returns false.
        :param name - name to check for.
        """
        for player in self.players:
            if player.name == name:
                return True
        return False

    def addPlayer(self, name, rating=None):
        """
        Adds a new player to the implementation.
        :param name - The name to identify a specific player.
        :param rating - The player's rating.
        """
        if rating == None:
            rating = self.base_rating

        self.players.append(_Player(name=name, rating=rating))

    def recordMatch1(self, name1, name2, goal_difference):
        """
        Should be called after a game is played.
        This version is used to record overall strength of teams, based on the result only.
        :param name1 - name of the first player.
        :param name2 - name of the second player.
        :param goal_difference - goals scored by player 1 minus goals scored by player 2
        """
        player1 = self.getPlayer(name1)
        player2 = self.getPlayer(name2)

        expected1 = player1.compareRating(player2)
        expected2 = player2.compareRating(player1)

        k = len(self.__getPlayerList()) * 42

        rating1 = player1.rating
        rating2 = player2.rating

        if goal_difference > 0:
            score1 = 0.90 + goal_difference * 0.05
            score2 = 1 - score1

        elif goal_difference < 0:
            score2 = 0.90 - goal_difference * 0.05
            score1 = 1 - score2

        elif goal_difference == 0:
            score1 = 0.5
            score2 = 0.5

        newRating1 = rating1 + k * (score1 - expected1)
        newRating2 = rating2 + k * (score2 - expected2)

        if newRating1 < 0:
            newRating1 = 0
            newRating2 = rating2 - rating1

        elif newRating2 < 0:
            newRating2 = 0
            newRating1 = rating1 - rating2

        player1.rating = newRating1
        player2.rating = newRating2

    def recordMatch2(self, name1, name2, goals_scored, h_or_a):
        """
        Should be called after a game is played.
        This version is used to record attacking / defensive strength of teams, based on how many goals were scored.
        :param name1 - name of the first player.
        :param name2 - name of the second player.
        :param goals_scored - how many goals have been scored
        :param h_or_a - by which team were the goals scored?
        """
        player1 = self.getPlayer(name1)
        player2 = self.getPlayer(name2)

        expected1 = player1.compareRating(player2)
        expected2 = player2.compareRating(player1)

        k = len(self.__getPlayerList()) * 42

        rating1 = player1.rating
        rating2 = player2.rating

        if h_or_a == 'h':
            score1 = (goals_scored / 4) ** (1/3)
            score2 = 1 - score1
        elif h_or_a == 'a':
            score2 = (goals_scored / 4) ** (1/3)
            score1 = 1 - score2
        else:
            print('error')

        newRating1 = rating1 + k * (score1 - expected1)
        newRating2 = rating2 + k * (score2 - expected2)

        if newRating1 < 0:
            newRating1 = 0
            newRating2 = rating2 - rating1

        elif newRating2 < 0:
            newRating2 = 0
            newRating1 = rating1 - rating2

        player1.rating = newRating1
        player2.rating = newRating2

    def getPlayerRating(self, name):
        """
        Returns the rating of the player with the given name.
        :param name - name of the player.
        :return - the rating of the player with the given name.
        """
        player = self.getPlayer(name)
        return player.rating

    def getRatingList(self):
        """
        Returns a list of tuples in the form of ({name},{rating})
        :return - the list of tuples
        """
        lst = []
        for player in self.__getPlayerList():
            lst.append((player.name, player.rating))
        return lst


class _Player:
    """
    A class to represent a player in the Elo Rating System
    """

    def __init__(self, name, rating):
        """
        Runs at initialization of class object.
        :param name - TODO
        :param rating - TODO
        """
        self.name = name
        self.rating = rating

    def compareRating(self, opponent):
        """
        Compares the two ratings of the this player and the opponent.
        :param opponent - the player to compare against.
        :returns - The expected score between the two players.
        """
        return (1 + 10 ** ((opponent.rating - self.rating) / 400.0)) ** -1


def scorePredictor(home_team, away_team):
    # source: https://github.com/dashee87/blogScripts/blob/master/Jupyter/2017-06-04-predicting-football-results-
    # with-statistical-modelling.ipynb
    epl_1920 = pd.read_csv("all_fixtures.csv")
    epl_1920 = epl_1920[['HomeTeam', 'AwayTeam', 'HomeGoals', 'AwayGoals']]
    epl_1920.head()

    goal_model_data = pd.concat([epl_1920[['HomeTeam', 'AwayTeam', 'HomeGoals']].assign(home=1).rename(
        columns={'HomeTeam': 'team', 'AwayTeam': 'opponent', 'HomeGoals': 'goals'}),
        epl_1920[['AwayTeam', 'HomeTeam', 'AwayGoals']].assign(home=0).rename(
            columns={'AwayTeam': 'team', 'HomeTeam': 'opponent', 'AwayGoals': 'goals'})])
    poisson_model = smf.glm(formula="goals ~ home + team + opponent", data=goal_model_data,
                            family=sm.families.Poisson()).fit()
    poisson_model.summary()
    return [np.array(poisson_model.predict(pd.DataFrame(data={'team': home_team, 'opponent': away_team, 'home': 1},
                                                        index=[1])))[0], np.array(poisson_model.predict(pd.DataFrame(
        data={'team': away_team, 'opponent': home_team, 'home': 0}, index=[1])))[0]]


def captainSelector(GW):
    sheet = CSV_reader('FPL_Fixtures.csv')  # all good
    teams = ['ARS', 'AVL', 'BOU', 'BHA', 'BUR', 'CHE', 'CRY', 'EVE', 'LEI', 'LIV', 'MCI', 'MUN', 'NEW', 'NOR',
             'SHU', 'SOU', 'TOT', 'WAT', 'WHU', 'WOL']
    fixtures = []
    for i in range(20):
        fixtures.append(sheet[GW][i])
    goals_scored = []
    for i in range(20):
        if '&' in fixtures[i]:
            matches = fixtures[i].split('&')
            x = 0
            if '(H)' in matches[0]:
                indiv_match = matches[0].replace(' (H)', '')
                x += round(scorePredictor(teams[i], indiv_match)[0], 2)
            elif '(A)' in matches[0]:
                indiv_match = matches[0].replace(' (A)', '')
                x += round(scorePredictor(indiv_match, teams[i])[1], 2)
            else:
                x += 0
            if '(H)' in matches[1]:
                indiv_match = matches[1].replace(' (H)', '')
                x += round(scorePredictor(teams[i], indiv_match)[0], 2)
            elif '(A)' in matches[1]:
                indiv_match = matches[1].replace(' (A)', '')
                x += round(scorePredictor(indiv_match, teams[i])[1], 2)
            else:
                x += 0
            goals_scored.append(x)
        elif '(H)' in fixtures[i]:
            indiv_match = fixtures[i].replace(' (H)', '')
            goals_scored.append(round(scorePredictor(teams[i], indiv_match)[0], 2))
        elif '(A)' in fixtures[i]:
            indiv_match = fixtures[i].replace(' (A)', '')
            goals_scored.append(round(scorePredictor(indiv_match, teams[i])[1], 2))
        else:
            goals_scored.append(0)

    data = topPlayers()
    xGA = []
    players = []
    for i in range(20):
        xGA.append(round(data[i][4] * goals_scored[i], 2))
        full_name = data[i][0].split(' ')
        name = full_name[len(full_name) - 1]
        players.append(name)

    def sortSecond(val):
        return val[1]

    array = []
    for i in range(20):
        array.append([players[i], xGA[i], fixtures[i]])
    array.sort(key=sortSecond, reverse=True)

    teams_sorted = []
    ratings_sorted = []
    fixtures = []
    for i in range(7):
        teams_sorted.append(array[i][0])
        ratings_sorted.append(array[i][1])
        fixtures.append(array[i][2])

    print(tabulate([teams_sorted, ratings_sorted, fixtures], tablefmt='rst'))


def topPlayers():
    data = CSV_reader('goalscorers.csv')
    teams = ['ARS', 'AVL', 'BOU', 'BHA', 'BUR', 'CHE', 'CRY', 'EVE', 'LEI', 'LIV', 'MCI', 'MUN', 'NEW', 'NOR',
             'SHU', 'SOU', 'TOT', 'WAT', 'WHU', 'WOL']
    top_inv = []
    top_player = []
    team_goals = []
    for team in teams:
        inv = 0
        goals = 0
        for row in data:
            if row[1] == team:
                old_inv = inv
                goals += int(row[2])
                inv = max(inv, int(row[2]) + int(row[3]))
                if not inv - old_inv == 0:
                    player = row[0]
        top_inv.append(inv)
        top_player.append(player)
        team_goals.append(goals)
    pct_inv = []
    for i in range(20):
        pct_inv.append(round(top_inv[i] / team_goals[i], 3))
    data = []
    for i in range(20):
        x = [top_player[i], teams[i], top_inv[i], team_goals[i], pct_inv[i]]
        data.append(x)
    return data


def colourNumbers(num):
    if num < 10:
        return Fore.RED + str(num) + Fore.RESET
    elif num < 20:
        return Fore.LIGHTRED_EX + str(num) + Fore.RESET
    elif num < 40:
        return Fore.LIGHTYELLOW_EX + str(num) + Fore.RESET
    elif num < 60:
        return Fore.GREEN + str(num) + Fore.RESET
    else:
        return Fore.LIGHTGREEN_EX + str(num) + Fore.RESET


def colourNumbers_2(num):
    if num < 10:
        return '[color=#FF0000]' + str(num) + ' %' + '[color=#FFFFFF]'
    elif num < 20:
        return '[color=#FF8000]' + str(num) + ' %' + '[color=#FFFFFF]'
    elif num < 40:
        return '[color=#FFFF00]' + str(num) + ' %' + '[color=#FFFFFF]'
    elif num < 60:
        return '[color=#00FF00]' + str(num) + ' %' + '[color=#FFFFFF]'
    else:
        return '[color=#008000]' + str(num) + ' %' + '[color=#FFFFFF]'


def inclusiveIndicator(element, array):
    for row in array:
        if element in row:
            return True
    return False


def roundPredictor(GW, mode, cs):
    sheet = CSV_reader('FPL_Fixtures.csv')  # all good
    teams = ['ARS', 'AVL', 'BOU', 'BHA', 'BUR', 'CHE', 'CRY', 'EVE', 'LEI', 'LIV', 'MCI', 'MUN', 'NEW', 'NOR',
             'SHU', 'SOU', 'TOT', 'WAT', 'WHU', 'WOL']
    data = []
    for i in range(20):
        x = sheet[GW][i]
        if '&' in x:
            games = x.split('&')
            for x in games:
                if '(H)' in x:
                    data.append([teams[i], x.split(' ')[0]])
                elif '(A)' in x:
                    data.append([x.split(' ')[0], teams[i]])
        elif '(H)' in x and not inclusiveIndicator(teams[i], data):
            data.append([teams[i], x.split(' ')[0]])
        elif '(A)' in x and not inclusiveIndicator(teams[i], data):
            data.append([x.split(' ')[0], teams[i]])
    end = True
    scorePredictions = []
    if cs:
        for i in range(len(data)):
            z = scorePredictor(data[i][0], data[i][1])
            y = [0, 0]
            y[0] = 100 * math.exp(- z[0])
            y[1] = 100 * math.exp(- z[1])
            z[1] = round(y[0], 1-int(math.floor(math.log10(abs(y[0])))))
            z[0] = round(y[1], 1-int(math.floor(math.log10(abs(y[1])))))
            scorePredictions.append(z)
    else:
        for i in range(len(data)):
            y = scorePredictor(data[i][0], data[i][1])
            scorePredictions.append(y)
    x = scorePredictions
    if mode == 'random':
        while end:
            cs = 0
            x = []
            for y in scorePredictions:
                x.append([np.random.poisson(y[0], 1)[0], np.random.poisson(y[1], 1)[0]])
            for i in range(len(x)):
                if x[i][0] + x[i][1] == 0:
                    cs += 2
                elif x[i][0] * x[i][1] == 0:
                    cs += 1
            if cs < int(round(len(data) / 2) + 1):
                end = False
    array = []
    if cs:
        for i in range(len(x)):
            array.append([data[i][0], colourNumbers(x[i][0]), colourNumbers(x[i][1]), data[i][1]])
        print(tabulate(array, tablefmt='grid'))
    else:
        for i in range(len(x)):
            array.append([data[i][0], colourNumbers(round(x[i][0], 2)), colourNumbers(round(x[i][1], 2)), data[i][1]])
        print(tabulate(array, tablefmt='grid'))


def roundPredictor_2(GW, cs):
    sheet = CSV_reader('FPL_Fixtures.csv')  # all good
    teams = ['ARS', 'AVL', 'BOU', 'BHA', 'BUR', 'CHE', 'CRY', 'EVE', 'LEI', 'LIV', 'MCI', 'MUN', 'NEW', 'NOR',
             'SHU', 'SOU', 'TOT', 'WAT', 'WHU', 'WOL']
    data = []
    for i in range(20):
        x = sheet[GW][i]
        if '&' in x:
            games = x.split('&')
            for x in games:
                if '(H)' in x:
                    data.append([teams[i], x.split(' ')[0]])
                elif '(A)' in x:
                    data.append([x.split(' ')[0], teams[i]])
        elif '(H)' in x and not inclusiveIndicator(teams[i], data):
            data.append([teams[i], x.split(' ')[0]])
        elif '(A)' in x and not inclusiveIndicator(teams[i], data):
            data.append([x.split(' ')[0], teams[i]])
    scorePredictions = []
    if cs:
        for i in range(len(data)):
            z = scorePredictor(data[i][0], data[i][1])
            y = [0, 0]
            y[0] = 100 * math.exp(- z[0])
            y[1] = 100 * math.exp(- z[1])
            z[1] = round(y[0], 1-int(math.floor(math.log10(abs(y[0])))))
            z[0] = round(y[1], 1-int(math.floor(math.log10(abs(y[1])))))
            scorePredictions.append(z)
    else:
        for i in range(len(data)):
            y = scorePredictor(data[i][0], data[i][1])
            scorePredictions.append(y)
    x = scorePredictions
    if cs:
        col1 = ''
        col2 = ''
        col3 = ''
        col4 = ''
        for i in range(len(x)):
            col1 += data[i][0] + '\n'
            col2 += colourNumbers_2(x[i][0]) + '\n'
            col3 += colourNumbers_2(x[i][1]) + '\n'
            col4 += data[i][1] + '\n'
        array = [col1, col2, col3, col4]
        return array
    else:
        col1 = ''
        col2 = ''
        col3 = ''
        col4 = ''
        for i in range(len(x)):
            col1 += data[i][0] + '\n'
            col2 += str(round(x[i][0], 2)) + '\n'
            col3 += str(round(x[i][1], 2)) + '\n'
            col4 += data[i][1] + '\n'
        array = [col1, col2, col3, col4]
        return array
