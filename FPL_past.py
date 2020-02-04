import numpy
from tabulate import tabulate
from CSV_reader import CSV_reader
import csv
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


def comparisonFn(x, y):
    if x > y:
        return Fore.RED + str(x) + ' \N{BLACK DOWN-POINTING TRIANGLE} ' + str(y) + '  ' + Fore.RESET
    elif x < y:
        return Fore.GREEN + str(x) + ' \N{BLACK UP-POINTING TRIANGLE} ' + str(y) + '  ' + Fore.RESET
    else:
        return Fore.YELLOW + str(x) + ' unchanged' + Fore.RESET


def comparisonFn_2(x, y):
    if x > y + 10:
        return '[color=#FF0000]' + str(x) + ' -> ' + str(y) + '  ' + '[color=#FFFFFF]'
    elif x < y - 10:
        return '[color=#00FF00]' + str(x) + ' -> ' + str(y) + '  ' + '[color=#FFFFFF]'
    else:
        return '[color=#FFFF00]' + str(x) + ' -> ' + str(y) + '[color=#FFFFFF]'


def recordFixture(home_team, away_team, home_goals, away_goals):
    data = CSV_reader('fixture_difficulty.csv')
    def_data = CSV_reader('defence_difficulty.csv')
    att_data = CSV_reader('attack_difficulty.csv')
    teams = data[0]
    difficulties = []
    defence = []
    attack = []
    for i in range(40):
        difficulties.append(int(data[1][i]))
        defence.append(int(def_data[1][i]))
        attack.append(int(att_data[1][i]))

    home_index = teams.index(home_team)
    away_index = teams.index(away_team)
    home_rating = difficulties[home_index]
    home_def_rating = defence[home_index]
    home_att_rating = attack[home_index]
    away_rating = difficulties[away_index]
    away_def_rating = defence[away_index]
    away_att_rating = attack[away_index]

    i = Implementation()
    i_h_goals = Implementation()
    i_a_goals = Implementation()
    i.addPlayer(home_team, rating=home_rating)
    i_h_goals.addPlayer(home_team, rating=home_att_rating)
    i_a_goals.addPlayer(home_team, rating=home_def_rating)
    i.addPlayer(away_team, rating=away_rating)
    i_h_goals.addPlayer(away_team, rating=away_def_rating)
    i_a_goals.addPlayer(away_team, rating=away_att_rating)
    GD = home_goals - away_goals
    i.recordMatch1(home_team, away_team, GD)
    i_h_goals.recordMatch2(home_team, away_team, home_goals, 'h')
    i_a_goals.recordMatch2(home_team, away_team, away_goals, 'a')
    result = i.getRatingList()
    result_home = i_h_goals.getRatingList()
    result_away = i_a_goals.getRatingList()
    headers = ['', 'OVR', 'DEF', 'ATT', 'Score']
    home = [home_team, comparisonFn(difficulties[home_index], round(result[0][1])),
            comparisonFn(defence[home_index], round(result_away[0][1])),
            comparisonFn(attack[home_index], round(result_home[0][1])), home_goals]
    away = [away_team, comparisonFn(difficulties[away_index], round(result[1][1])),
            comparisonFn(defence[away_index], round(result_home[1][1])),
            comparisonFn(attack[away_index], round(result_away[1][1])), away_goals]
    print(tabulate([home, away], headers, tablefmt='grid'))

    difficulties[home_index] = round(result[0][1])
    difficulties[away_index] = round(result[1][1])

    defence[home_index] = round(result_away[0][1])
    defence[away_index] = round(result_home[1][1])

    attack[home_index] = round(result_home[0][1])
    attack[away_index] = round(result_away[1][1])

    with open('fixture_difficulty.csv', mode='w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(teams)
        writer.writerow(difficulties)

    with open('defence_difficulty.csv', mode='w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(teams)
        writer.writerow(defence)

    with open('attack_difficulty.csv', mode='w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(teams)
        writer.writerow(attack)


def recordFixture_2(home_team, away_team, home_goals, away_goals):
    data = CSV_reader('fixture_difficulty.csv')
    def_data = CSV_reader('defence_difficulty.csv')
    att_data = CSV_reader('attack_difficulty.csv')
    teams = data[0]
    difficulties = []
    defence = []
    attack = []
    for i in range(40):
        difficulties.append(int(data[1][i]))
        defence.append(int(def_data[1][i]))
        attack.append(int(att_data[1][i]))

    home_index = teams.index(home_team)
    away_index = teams.index(away_team)
    home_rating = difficulties[home_index]
    home_def_rating = defence[home_index]
    home_att_rating = attack[home_index]
    away_rating = difficulties[away_index]
    away_def_rating = defence[away_index]
    away_att_rating = attack[away_index]

    i = Implementation()
    i_h_goals = Implementation()
    i_a_goals = Implementation()
    i.addPlayer(home_team, rating=home_rating)
    i_h_goals.addPlayer(home_team, rating=home_att_rating)
    i_a_goals.addPlayer(home_team, rating=home_def_rating)
    i.addPlayer(away_team, rating=away_rating)
    i_h_goals.addPlayer(away_team, rating=away_def_rating)
    i_a_goals.addPlayer(away_team, rating=away_att_rating)
    GD = home_goals - away_goals
    i.recordMatch1(home_team, away_team, GD)
    i_h_goals.recordMatch2(home_team, away_team, home_goals, 'h')
    i_a_goals.recordMatch2(home_team, away_team, away_goals, 'a')
    result = i.getRatingList()
    result_home = i_h_goals.getRatingList()
    result_away = i_a_goals.getRatingList()
    home = [home_team, comparisonFn_2(difficulties[home_index], round(result[0][1])),
            comparisonFn_2(defence[home_index], round(result_away[0][1])),
            comparisonFn_2(attack[home_index], round(result_home[0][1])), str(home_goals)]
    away = [away_team, comparisonFn_2(difficulties[away_index], round(result[1][1])),
            comparisonFn_2(defence[away_index], round(result_home[1][1])),
            comparisonFn_2(attack[away_index], round(result_away[1][1])), str(away_goals)]

    difficulties[home_index] = round(result[0][1])
    difficulties[away_index] = round(result[1][1])

    defence[home_index] = round(result_away[0][1])
    defence[away_index] = round(result_home[1][1])

    attack[home_index] = round(result_home[0][1])
    attack[away_index] = round(result_away[1][1])

    with open('fixture_difficulty.csv', mode='w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(teams)
        writer.writerow(difficulties)

    with open('defence_difficulty.csv', mode='w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(teams)
        writer.writerow(defence)

    with open('attack_difficulty.csv', mode='w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(teams)
        writer.writerow(attack)

    return [home, away]


def resultRecorder(home, away, h_or_a):
    if h_or_a == 'h':
        if home > away:
            return [1, 1, 0, 0, home, away, home - away, 3]
        elif away > home:
            return [1, 0, 0, 1, home, away, home - away, 0]
        else:
            return [1, 0, 1, 0, home, away, home - away, 1]
    elif h_or_a == 'a':
        if home > away:
            return [1, 0, 0, 1, away, home, away - home, 0]
        elif home < away:
            return [1, 1, 0, 0, away, home, away - home, 3]
        else:
            return [1, 0, 1, 0, away, home, away - home, 1]


def fixtureFinder(team_name, place):

    data = CSV_reader('all_fixtures.csv')
    games = []
    home_games = []
    away_games = []
    results = numpy.array([0, 0, 0, 0, 0, 0, 0, 0])
    results_home = numpy.array([0, 0, 0, 0, 0, 0, 0, 0])
    results_away = numpy.array([0, 0, 0, 0, 0, 0, 0, 0])
    for row in data:
        if place == 'H':
            if team_name == row[0]:
                games.append(row[0] + ' ' + row[2] + ' - ' + row[3] + ' ' + row[1])
                y = numpy.array(resultRecorder(int(row[2]), int(row[3]), 'h'))
                results = results.__add__(y)
        elif place == 'A':
            if team_name == row[1]:
                games.append(row[0] + ' ' + row[2] + ' - ' + row[3] + ' ' + row[1])
                y = numpy.array(resultRecorder(int(row[2]), int(row[3]), 'a'))
                results = results.__add__(y)
        else:
            if team_name == row[0]:
                home_games.append(row[0] + ' ' + row[2] + ' - ' + row[3] + ' ' + row[1])
                away_games.append('')
                y = numpy.array(resultRecorder(int(row[2]), int(row[3]), 'h'))
                results_home = results_home.__add__(y)
            elif team_name == row[1]:
                away_games.append(row[0] + ' ' + row[2] + ' - ' + row[3] + ' ' + row[1])
                home_games.append('')
                y = numpy.array(resultRecorder(int(row[2]), int(row[3]), 'a'))
                results_away = results_away.__add__(y)
    if place == 'H':
        return [games, list(results)]
    elif place == 'A':
        return [games, list(results)]
    else:
        return [home_games, away_games, results_home, results_away]


def rerecordAllFixtures():
    init = CSV_reader('initial_info.csv')
    with open('attack_difficulty.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(init[0])
        writer.writerow(init[1])
    with open('defence_difficulty.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(init[0])
        writer.writerow(init[1])
    with open('fixture_difficulty.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(init[0])
        writer.writerow(init[2])
    all_data = CSV_reader('all_fixtures.csv')
    for row in all_data:
        if not row[0] == 'HomeTeam':
            recordFixture(row[0] + ' (A)', row[1] + ' (H)', int(row[2]), int(row[3]))


if __name__ == '__main__':
    rerecordAllFixtures()
