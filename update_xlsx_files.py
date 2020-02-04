import asyncio
import aiohttp
from understat import Understat
from goal_extractor import teamAbbreviator
import csv
from CSV_reader import CSV_reader
from tabulate import tabulate
from FPL_past import recordFixture, recordFixture_2


def combsum(x, y):
    return round(1.5 / ((1 / x) + (1 / y)))


def update_diff_table():
    with open('FPL_fixtures.csv', 'r') as file:  # all good
        reader = csv.reader(file)
        initialise = True
        data = CSV_reader('fixture_difficulty.csv')
        fixtures = data[0]
        diffs = data[1]
        all_info = []
        for row in reader:
            if initialise:
                initialise = False
            else:
                row_info = []
                for i in row:
                    if i in fixtures:
                        row_info.append(diffs[fixtures.index(i)])
                    else:
                        row_info.append(1000)
                all_info.append(row_info)

    with open('FPL_Fixtures_numbered.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        teams = ['ARS', 'AVL', 'BOU', 'BHA', 'BUR', 'CHE', 'CRY', 'EVE', 'LEI', 'LIV', 'MCI', 'MUN', 'NEW', 'NOR',
                 'SHU', 'SOU', 'TOT', 'WAT', 'WHU', 'WOL']
        writer.writerow(teams)
        for row in all_info:
            writer.writerow(row)

    with open('FPL_fixtures.csv', 'r') as file:  # all good
        reader = csv.reader(file)
        initialise = True
        data = CSV_reader('defence_difficulty.csv')
        fixtures = data[0]
        diffs = data[1]
        all_info = []
        for row in reader:
            if initialise:
                initialise = False
            else:
                row_info = []
                for game in row:
                    if game == 'None':
                        pass
                    if game in fixtures:
                        row_info.append(diffs[fixtures.index(game)])
                    else:
                        row_info.append(1000)
                all_info.append(row_info)

    with open('FPL_Fixtures_numbered_def.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        teams = ['ARS', 'AVL', 'BOU', 'BHA', 'BUR', 'CHE', 'CRY', 'EVE', 'LEI', 'LIV', 'MCI', 'MUN', 'NEW', 'NOR',
                 'SHU', 'SOU', 'TOT', 'WAT', 'WHU', 'WOL']
        writer.writerow(teams)
        for row in all_info:
            writer.writerow(row)

    with open('FPL_fixtures.csv', 'r') as file:  # all good
        reader = csv.reader(file)
        initialise = True
        data = CSV_reader('attack_difficulty.csv')
        fixtures = data[0]
        diffs = data[1]
        all_info = []
        for row in reader:
            if initialise:
                initialise = False
            else:
                row_info = []
                for i in row:
                    if i in fixtures:
                        row_info.append(diffs[fixtures.index(i)])
                    else:
                        row_info.append(1000)
                all_info.append(row_info)

    with open('FPL_Fixtures_numbered_att.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        teams = ['ARS', 'AVL', 'BOU', 'BHA', 'BUR', 'CHE', 'CRY', 'EVE', 'LEI', 'LIV', 'MCI', 'MUN', 'NEW', 'NOR',
                 'SHU', 'SOU', 'TOT', 'WAT', 'WHU', 'WOL']
        writer.writerow(teams)
        for row in all_info:
            writer.writerow(row)


def update_diff_lists(list_type, disp):
    if list_type == 'OVR':
        data = CSV_reader('fixture_difficulty.csv')
    elif list_type == 'DEF':
        data = CSV_reader('defence_difficulty.csv')
    elif list_type == 'ATT':
        data = CSV_reader('attack_difficulty.csv')
    else:
        return None
    difficulties_home = []
    difficulties_away = []
    if list_type == 'DEF':
        divisor = 90
        shift = 3.5
    elif list_type == 'ATT':
        divisor = 120
        shift = 2.5
    elif list_type == 'OVR':
        divisor = 200
        shift = 0
    teams = ['ARS', 'AVL', 'BOU', 'BHA', 'BUR', 'CHE', 'CRY', 'EVE', 'LEI', 'LIV', 'MCI', 'MUN', 'NEW',
             'NOR', 'SHU', 'SOU', 'TOT', 'WAT', 'WHU', 'WOL']
    for i in range(40):
        if i % 2 == 0:
            difficulties_home.append(round(int(data[1][i]) / (divisor * 1.1) - shift, 2))
        elif i % 2 == 1:
            difficulties_away.append(round(int(data[1][i]) / (divisor * 1.1) - shift, 2))

    if list_type == 'OVR':
        with open('fixture_difficulty_table.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(teams)
            writer.writerow(difficulties_away)
            writer.writerow(difficulties_home)
        data = CSV_reader('fixture_difficulty.csv')
        teams = data[0][:40]
        ratings = data[1][:40]
        for i in range(40):
            for j in range(40):
                teams.append(teams[i] + '&' + teams[j])
                ratings.append(combsum(int(ratings[i]), int(ratings[j])))
        with open('fixture_difficulty.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(teams)
            writer.writerow(ratings)
    elif list_type == 'DEF':
        with open('defence_difficulty_table.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(teams)
            writer.writerow(difficulties_away)
            writer.writerow(difficulties_home)
        data = CSV_reader('defence_difficulty.csv')
        teams = data[0][:40]
        ratings = data[1][:40]
        for i in range(40):
            for j in range(40):
                teams.append(teams[i] + '&' + teams[j])
                ratings.append(combsum(int(ratings[i]), int(ratings[j])))
        with open('defence_difficulty.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(teams)
            writer.writerow(ratings)
    elif list_type == 'ATT':
        with open('attack_difficulty_table.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(teams)
            writer.writerow(difficulties_away)
            writer.writerow(difficulties_home)
        data = CSV_reader('attack_difficulty.csv')
        teams = data[0][:40]
        ratings = data[1][:40]
        for i in range(40):
            for j in range(40):
                teams.append(teams[i] + '&' + teams[j])
                ratings.append(combsum(int(ratings[i]), int(ratings[j])))
        with open('attack_difficulty.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(teams)
            writer.writerow(ratings)
    if disp:
        return tabulate([*zip(*[teams, difficulties_away, difficulties_home])], ['', 'Home', 'Away'], tablefmt='orgtbl')
    else:
        return None

def update_diff_lists_2(list_type):
    if list_type == 'OVR':
        data = CSV_reader('fixture_difficulty.csv')
    elif list_type == 'DEF':
        data = CSV_reader('defence_difficulty.csv')
    elif list_type == 'ATT':
        data = CSV_reader('attack_difficulty.csv')
    else:
        return None
    difficulties_home = []
    difficulties_away = []
    teams = ['ARS', 'AVL', 'BOU', 'BHA', 'BUR', 'CHE', 'CRY', 'EVE', 'LEI', 'LIV', 'MCI', 'MUN', 'NEW',
             'NOR', 'SHU', 'SOU', 'TOT', 'WAT', 'WHU', 'WOL']
    for i in range(40):
        if i % 2 == 0:
            difficulties_home.append(data[1][i])
        elif i % 2 == 1:
            difficulties_away.append(data[1][i])

    if list_type == 'OVR':
        with open('fixture_difficulty_table.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(teams)
            writer.writerow(difficulties_away)
            writer.writerow(difficulties_home)
        data = CSV_reader('fixture_difficulty.csv')
        teams = data[0][:40]
        ratings = data[1][:40]
        for i in range(40):
            for j in range(40):
                teams.append(teams[i] + '&' + teams[j])
                ratings.append(combsum(int(ratings[i]), int(ratings[j])))
        with open('fixture_difficulty.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(teams)
            writer.writerow(ratings)
    elif list_type == 'DEF':
        with open('defence_difficulty_table.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(teams)
            writer.writerow(difficulties_away)
            writer.writerow(difficulties_home)
        data = CSV_reader('defence_difficulty.csv')
        teams = data[0][:40]
        ratings = data[1][:40]
        for i in range(40):
            for j in range(40):
                teams.append(teams[i] + '&' + teams[j])
                ratings.append(combsum(int(ratings[i]), int(ratings[j])))
        with open('defence_difficulty.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(teams)
            writer.writerow(ratings)
    elif list_type == 'ATT':
        with open('attack_difficulty_table.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(teams)
            writer.writerow(difficulties_away)
            writer.writerow(difficulties_home)
        data = CSV_reader('attack_difficulty.csv')
        teams = data[0][:40]
        ratings = data[1][:40]
        for i in range(40):
            for j in range(40):
                teams.append(teams[i] + '&' + teams[j])
                ratings.append(combsum(int(ratings[i]), int(ratings[j])))
        with open('attack_difficulty.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(teams)
            writer.writerow(ratings)
    return [teams, difficulties_away, difficulties_home]


async def update_results():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        games_data = await understat.get_league_results('epl', 2019)
        games_list = []
        for game in games_data:
            games_list.append([teamAbbreviator(game['h']['title']), teamAbbreviator(game['a']['title']),
                               game['xG']['h'], game['xG']['a']])
        with open('all_results_xG.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['HomeTeam', 'AwayTeam', 'HomeGoals', 'AwayGoals'])
            for row in games_list:
                writer.writerow(row)
        games_list = []
        for game in games_data:
            games_list.append([teamAbbreviator(game['h']['title']), teamAbbreviator(game['a']['title']),
                               int(game['goals']['h']), int(game['goals']['a'])])
        with open('all_results.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['HomeTeam', 'AwayTeam', 'HomeGoals', 'AwayGoals'])
            for row in games_list:
                writer.writerow(row)


def update_scores():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_results())
    up2date = CSV_reader('all_results.csv')
    outofdate = CSV_reader('all_fixtures.csv')
    extra = []
    if len(up2date) != len(outofdate):
        for i in range(len(outofdate), len(up2date)):
            extra.append(up2date[i])
    for i in range(len(extra)):
        recordFixture(extra[i][0] + ' (A)', extra[i][1] + ' (H)', int(extra[i][2]), int(extra[i][3]))
    with open('all_fixtures.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        for i in range(len(extra)):
            writer.writerow(extra[i])


def listJoiner(lis):
    x = ''
    for i in lis:
        try:
            l = int(i)
            x += '   ' + str(i)
        except (TypeError, ValueError):
            x += str(i) + ' '
    return x


def update_scores_2():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_results())
    up2date = CSV_reader('all_results.csv')
    outofdate = CSV_reader('all_fixtures.csv')
    extra = []
    if len(up2date) != len(outofdate):
        for i in range(len(outofdate), len(up2date)):
            extra.append(up2date[i])
    headers = ['        ', '         OVR    ', '        DEF    ', '           ATT    ', '  Score']
    col1 = ''
    col2 = ''
    col3 = ''
    col4 = ''
    col5 = ''
    fatcol = ''
    for i in range(len(extra)):
        x = recordFixture_2(extra[i][0] + ' (A)', extra[i][1] + ' (H)', int(extra[i][2]), int(extra[i][3]))
        col1 += headers[0] + '\n' + x[0][0] + '\n' + x[1][0] + '\n\n'
        col2 += headers[1] + '\n' + x[0][1] + '\n' + x[1][1] + '\n\n'
        col3 += headers[2] + '\n' + x[0][2] + '\n' + x[1][2] + '\n\n'
        col4 += headers[3] + '\n' + x[0][3] + '\n' + x[1][3] + '\n\n'
        col5 += headers[4] + '\n' + x[0][4] + '\n' + x[1][4] + '\n\n'
        fatcol += listJoiner(headers) + '\n' + listJoiner(x[0]) + '\n' + listJoiner(x[1]) + '\n\n'
    fatcol += '[color=#00FF00]Up to date[color=#FFFFFF]'
    with open('all_fixtures.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        for i in range(len(extra)):
            writer.writerow(extra[i])
    # return [col1, col2, col3, col4, col5]
    return fatcol


if __name__ == '__main__':
    update_diff_lists_2('ATT')
    update_diff_lists_2('DEF')
    update_diff_table()
