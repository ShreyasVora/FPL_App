import math
import asyncio
import csv
import pickle
import numpy
from tabulate import tabulate
import os
from colorama import Fore, init
import math

from CSV_reader import CSV_reader
from fixture_difficulty_calculator import FPL_fixture_difficulty
from fixture_run_diff import fixture_run_difficulty
from goal_extractor import update_goalscorers, list_goalscorers, list_assisters
from update_xlsx_files import update_diff_lists, update_diff_table, update_scores
import myPlan
from FPL_past import fixtureFinder, ppg_printer
from FPL_future import scorePredictor, roundPredictor, colourNumbers
from myTeam import teamEditor, alternativeFinder
from pointsPredictor import runPredictor, pointsPredictor, pointsLost, runPredictor_2

init(autoreset=True)

menu = [[Fore.LIGHTCYAN_EX + '1', 'View Fixture Difficulties', '\N{WHITE RIGHT-POINTING TRIANGLE}  '],
        ['2', 'Update Files', '\N{WHITE RIGHT-POINTING TRIANGLE}  '], ['3', 'Predict Fixture', '  '],
        ['4', 'Predict Round of Fixtures', '\N{WHITE RIGHT-POINTING TRIANGLE}  '],
        ['5', 'Predict Best Points Scorers', '  '], ['6', 'View Past Results', '  '], ['7', 'View Tables', '  '],
        ['8', 'FPL_Plan', '\N{WHITE RIGHT-POINTING TRIANGLE}  '],
        ['9', 'FPL_Team', '\N{WHITE RIGHT-POINTING TRIANGLE}  '], ['0', 'End Program', '  '],
        ['S', 'Settings', '\N{WHITE RIGHT-POINTING TRIANGLE}  ']]
print(tabulate(menu, tablefmt='plain'))

menu_choice = ''

while menu_choice != 0:

    menu_choice = input('Enter main menu choice: ').upper()
    if menu_choice == 'S':
        print(Fore.LIGHTCYAN_EX + 'Options Menu:\n1. Change Form sensitivity for xPoints\n2. Add / Remove players '
                                  'from nailed team selection\n3. Add / Remove players from bench fodder list')
        menu_choice_2 = int(input('Enter sub-menu choice: '))
        if menu_choice_2 == 1:
            data = CSV_reader('code_settings.csv')
            new_form_value = input('Current form value is ' + data[0][0] + '. Change it to: ')
            x = [new_form_value, data[1], data[2]]
        elif menu_choice_2 == 2:
            data = CSV_reader('code_settings.csv')
            players = data[1][0]
            for i in range(1, len(data[1])):
                players = players + ', ' + data[1][i]
            menu_choice_3 = input('Current nailed players: ' + players + '. Add / Remove? (A / R) ').upper()
            if menu_choice_3 == 'A':
                y = data[1]
                name = input('Who? ')
                y.append(name)
                x = [data[0], y, data[2]]
            elif menu_choice_3 == 'R':
                name = input('Who? ')
                if name in data[1]:
                    index = data[1].index(name)
                else:
                    index = 2000
                y = []
                for i in range(len(data[1])):
                    if i != index:
                        y.append(data[1][i])
                x = [data[0], y, data[2]]
        elif menu_choice_2 == 3:
            data = CSV_reader('code_settings.csv')
            players = data[2][0]
            for i in range(1, len(data[2])):
                players = players + ', ' + data[2][i]
            menu_choice_3 = input('Current bench fodder players: ' + players + '. Add / Remove? (A / R) ').upper()
            if menu_choice_3 == 'A':
                y = data[2]
                name = input('Who? ')
                y.append(name)
                x = [data[0], data[1], y]
            elif menu_choice_3 == 'R':
                name = input('Who? ')
                if name in data[2]:
                    index = data[2].index(name)
                else:
                    index = 2000
                y = []
                for i in range(len(data[2])):
                    if i != index:
                        y.append(data[2][i])
                x = [data[0], data[1], y]
        else:
            x = CSV_reader('code_settings.csv')
        with open('code_settings.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            for row in x:
                writer.writerow(row)
    else:
        menu_choice = int(menu_choice)

    if menu_choice == 1:
        # View difficulties over different gameweek ranges
        print(Fore.LIGHTCYAN_EX + '1. Specific GW range\n2. General\n3. Specific Team\n4. View Difficulty Tables')
        menu_choice_2 = int(input('Enter sub menu choice: '))
        if menu_choice_2 == 1:
            start = int(input('From which GW would you like to start? '))
            finish = int(input('From which GW would you like to finish? '))
            print('')
            FPL_fixture_difficulty(start, finish, 'detailed', 'DEF')
            print('')
            FPL_fixture_difficulty(start, finish, 'detailed', 'ATT')
            print('')
        elif menu_choice_2 == 2:
            start = int(input('Start from GW: '))
            for finish in range(start, start + 6):
                print('\nOver the course of ' + str(finish - start + 1) + ' gameweeks:')
                FPL_fixture_difficulty(start, finish, 'none', 'DEF')
                FPL_fixture_difficulty(start, finish, 'none', 'ATT')
        elif menu_choice_2 == 3:
            start = int(input('From which GW would you like to start? '))
            finish = int(input('From which GW would you like to finish? '))
            team_name = input('Team name? ').upper()
            output = fixture_run_difficulty(start, finish, team_name, 'DEF')
            team_att = [Fore.MAGENTA + output[2][0] + Fore.RESET, Fore.MAGENTA + output[2][1] + Fore.RESET]
            output[1].insert(0, team_name + ' ATT')
            output[1].insert(0, '')
            output[0][0].insert(0, team_att[0])
            output[0][0].insert(0, 'Home')
            output[0][1].insert(0, team_att[1])
            output[0][1].insert(0, 'Away')
            print(tabulate([output[1], output[0][0], output[0][1]], tablefmt='simple'))
            output = fixture_run_difficulty(start, finish, team_name, 'ATT')
            team_def = [Fore.MAGENTA + output[2][0] + Fore.RESET, Fore.MAGENTA + output[2][1] + Fore.RESET]
            output[1].insert(0, team_name + ' DEF')
            output[1].insert(0, '')
            output[0][0].insert(0, team_def[0])
            output[0][0].insert(0, 'Home')
            output[0][1].insert(0, team_def[1])
            output[0][1].insert(0, 'Away')
            print(tabulate([output[1], output[0][0], output[0][1]], tablefmt='simple'))
        elif menu_choice_2 == 4:
            print(Fore.GREEN + '\nDefence:')
            print(update_diff_lists('DEF', disp=True))
            print(Fore.GREEN + '\nAttack:')
            print(update_diff_lists('ATT', disp=True))

    elif menu_choice == 2:
        print(
            Fore.LIGHTCYAN_EX + '1. Update scores\n2. Update and view goalscorers\n3. Update player form\n4. Open '
                                'difficulty tables')
        menu_choice_2 = int(input('Enter sub menu choice: '))
        if menu_choice_2 == 1:
            update_scores()
            print(Fore.GREEN + 'Scores up to date.')
            update_diff_lists('OVR', disp=False)
            update_diff_lists('DEF', disp=False)
            update_diff_lists('ATT', disp=False)
            update_diff_table()

        elif menu_choice_2 == 2:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(update_goalscorers())
            menu_choice_3 = True
            while menu_choice_3:
                x = input('Sort by (G / A): ').upper()
                if x == 'G':
                    list_goalscorers()
                elif x == 'A':
                    list_assisters()
                elif x == '0':
                    menu_choice_3 = False

        elif menu_choice_2 == 3:
            runPredictor(reload=True)

        elif menu_choice_2 == 4:
            print(Fore.LIGHTCYAN_EX + '1. Team ratings\n2. Fixture ratings tables')
            menu_choice_3 = int(input('Enter sub menu choice: '))
            if menu_choice_3 == 1:
                os.system('start "excel" "C:\\Users\\User\\OneDrive\\Documents\\python\\fixture_difficulty_table.xlsx"')
            elif menu_choice_2 == 2:
                os.system('start "excel" "C:\\Users\\User\\OneDrive\\Documents\\python\\FPL_Fixture_Difficulty.xlsx"')

    elif menu_choice == 3:
        print(Fore.LIGHTCYAN_EX + '1. Predict match score\n2. View clean sheet probability')
        menu_choice_3 = int(input('Enter sub-menu choice: '))
        home = input('Who will be the home team? ').upper()
        away = input('Who will be the away team? ').upper()
        cs = (menu_choice_3 == 2)
        if not cs:
            mode = input('Accurate or Random? ').upper()
        else:
            mode = 'A'
        if mode == 'A' or mode == 'a':
            mode = 'accurate'
        elif mode == 'R' or mode == 'r':
            mode = 'random'
        data = scorePredictor(home, away)
        if mode == 'accurate' and not cs:
            array = [home, colourNumbers(round(data[0], 2)), colourNumbers(round(data[1], 2)), away]
        elif not cs:
            x = [numpy.random.poisson(data[0], 1)[0], numpy.random.poisson(data[1], 1)[0]]
            array = [home, colourNumbers(x[0]), colourNumbers(x[1]), away]
        else:
            z = [round(data[0], 2), round(data[1], 2)]
            y = [0, 0]
            y[0] = 100 * math.exp(- z[0])
            y[1] = 100 * math.exp(- z[1])
            z[1] = round(y[0], 1 - int(math.floor(math.log10(abs(y[0])))))
            z[0] = round(y[1], 1 - int(math.floor(math.log10(abs(y[1])))))
            array = [home, colourNumbers(z[0]), colourNumbers(z[1]), away]
        print(tabulate([array], tablefmt='grid'))

    elif menu_choice == 4:
        print(Fore.LIGHTCYAN_EX + '1. Predict match scores\n2. View clean sheet probabilities')
        menu_choice_3 = int(input('Enter sub-menu choice: '))
        if menu_choice_3 == 1:
            gw = int(input('Which gameweek? '))
            mode = input('Accurate or Random? ').upper()
            if mode == 'A':
                mode = 'accurate'
            elif mode == 'R':
                mode = 'random'
            roundPredictor(gw, mode, cs=False)
        elif menu_choice_3 == 2:
            gw = int(input('Which gameweek? '))
            roundPredictor(gw, 'accurate', cs=True)

    elif menu_choice == 5:

        runPredictor_2()

    elif menu_choice == 6:

        team_name = input('Which team? ').upper()
        place = input('Home, Away, or Either? (H / A / E) ').upper()
        output = fixtureFinder(team_name, place)
        headers = ['P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts', '']
        trio = headers + headers + headers
        if place == 'H' or place == 'A':
            results = output[0]
            table = tabulate([headers, output[1]], tablefmt='plain')
            for result in results:
                print(result)
            print(table)
        else:
            print(tabulate([*zip(*[output[0], output[1]])]))
            print(tabulate([headers, output[2]], tablefmt='plain'))
            print(tabulate([headers, output[3]], tablefmt='plain'))
            print(tabulate([headers, output[2].__add__(output[3])], tablefmt='plain'))

    elif menu_choice == 7:
        teams = ['ARS', 'AVL', 'BOU', 'BHA', 'BUR', 'CHE', 'CRY', 'EVE', 'LEI', 'LIV', 'MCI', 'MUN', 'NEW', 'NOR',
                 'SHU', 'SOU', 'TOT', 'WAT', 'WHU', 'WOL']
        place = input('Home, Away, or Either? (H / A / E) ').upper()
        table = []
        for team_name in teams:
            output = fixtureFinder(team_name, place)
            if place == 'H' or place == 'A':
                results = output[1]
            else:
                results = output[2].__add__(output[3])
            results = [str(x) for x in results]
            results.insert(0, team_name)
            results[8] = int(results[8])
            table.append(results)
        table.sort(key=lambda x: x[8], reverse=True)
        headers = ['#', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts', '']
        for i in range(20):
            table[i][0] = str(i + 1) + ' ' + table[i][0]
        print(tabulate(table, headers))

    elif menu_choice == 8:

        myPlan.editPlan()

    elif menu_choice == 9:

        print(Fore.LIGHTCYAN_EX + 'FPL_Team Menu\n1. View / Edit Team\n2. Search best replacements\n3. View xPoints '
                                  'over range of gameweeks\n0. Exit FPL_Team')
        state = False
        while not state:
            menu_choice_2 = int(input('Enter FPL_Team choice: '))
            if menu_choice_2 == 1:
                teamEditor()
            elif menu_choice_2 == 2:
                position = input('Position: ').upper()
                teams = []
                x = 0
                while x != '0':
                    x = input('Team to add: ').upper()
                    if not x == '0':
                        teams.append(x)
                start = int(input('Starting from GW: '))
                stop = int(input('Ending at GW: '))
                num = int(input('Number to rotate: '))
                fodder = int(input('How much fodder? '))
                alternativeFinder(teams, position, start, stop, num, fodder)
            elif menu_choice_2 == 3:
                with open('player_data.pkl', 'rb') as file:
                    premier_league = pickle.load(file)
                with open('recent_data.pkl', 'rb') as file:
                    premier_league_form = pickle.load(file)
                start = int(input('GW Start '))
                finish = int(input('GW Finish '))
                X = int(input('View expected top N performers. N = '))
                players_list = []
                points_list = []
                data_list = []
                for gw in range(start, finish + 1):
                    data = pointsPredictor(gw, premier_league, premier_league_form)
                    data_list.append(data)
                players_list = CSV_reader('player_data.csv')[0]
                position_list = CSV_reader('player_data.csv')[1]
                for name in players_list:
                    points = 0
                    for i in range(len(data_list)):
                        for player in data_list[i]:
                            if name in player[0]:
                                points += float(player[1])
                    points_list.append(round(points, 1))
                array = []
                for i in range(len(players_list)):
                    if ppg_printer(players_list[i]) is None:
                        print(players_list[i])
                    lower_bound = (finish - start + 1) * ppg_printer(players_list[i])
                    upper_bound = (finish - start + 1) * ppg_printer(players_list[i])
                    if lower_bound >= 0.8 * points_list[i]:
                        lower_bound = round(max(0, points_list[i] - pointsLost(finish - start + 1, position_list[i]) + (finish - start + 1) * (ppg_printer(players_list[i]) - 4) / 2.5, 1))
                    if upper_bound <= 1.3 * points_list[i]:
                        upper_bound = round(points_list[i] + pointsLost(finish - start + 1, position_list[i]) + (finish - start + 1) * (ppg_printer(players_list[i]) - 6) / 2.5, 1)
                    array.append([players_list[i], lower_bound, points_list[i], upper_bound])
                array.sort(key=lambda x: x[3], reverse=True)
                print(tabulate(array[:X], ['Name', 'Minimum', 'xPoints', 'Maximum']))
            state = (menu_choice_2 == 0)
