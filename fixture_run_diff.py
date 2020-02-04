from CSV_reader import CSV_reader
from colorama import init, Fore

init(autoreset=True)


def fixture_run_difficulty(start, finish, team, mode):
    sheet = CSV_reader('FPL_Fixtures.csv')  # all good
    if mode == 'DEF':
        file = 'FPL_Fixtures_numbered_def.csv'
        file2 = 'attack_difficulty_table.csv'
    elif mode == 'ATT':
        file = 'FPL_Fixtures_numbered_att.csv'
        file2 = 'defence_difficulty_table.csv'
    elif mode == 'OVR':
        file = 'FPL_Fixtures_numbered.csv'
        file2 = 'fixture_difficulty_table.csv'
    else:
        print('error in fixture_run_difficulty()')
        return None
    data = CSV_reader(file)
    data2 = CSV_reader(file2)
    teams = data[0]
    team_index = teams.index(team)
    difficulties = [data2[1][team_index], data2[2][team_index]]  # strength of the chosen team, home and away, in the
    # chosen field
    diffs = []
    opponents = []
    for i in range(start, finish + 1):
        row = data[i]
        if team not in row:
            opponents.append(sheet[i][team_index])
            diffs.append(colourDiffs(int(row[team_index]), opponents[len(opponents) - 1], difficulties))
            #if mode == 'ATT':
            #    diffs.append(colourDiffs(round((int(row[team_index]) / 132) - 2.5, 2), opponents[len(opponents) - 1], difficulties))
            #elif mode == 'DEF':
            #    diffs.append(colourDiffs(round((int(row[team_index]) / 99) - 3.5, 2), opponents[len(opponents) - 1], difficulties))
            #else:
            #    diffs.append(colourDiffs(round(int(row[team_index]) / 200, 2), opponents[len(opponents) - 1], difficulties))
    h_diffs = []
    a_diffs = []
    for i in range(len(opponents)):
        if '(H)' in opponents[i]:
            h_diffs.append(diffs[i])
            a_diffs.append('')
        elif '(A)' in opponents[i]:
            h_diffs.append('')
            a_diffs.append(diffs[i])
    return [[h_diffs, a_diffs], opponents, difficulties]


def fixture_run_difficulty_2(start, finish, team, mode):
    sheet = CSV_reader('FPL_Fixtures.csv')  # all good
    if mode == 'DEF':
        file = 'FPL_Fixtures_numbered_def.csv'
        file2 = 'attack_difficulty_table.csv'
    elif mode == 'ATT':
        file = 'FPL_Fixtures_numbered_att.csv'
        file2 = 'defence_difficulty_table.csv'
    elif mode == 'OVR':
        file = 'FPL_Fixtures_numbered.csv'
        file2 = 'fixture_difficulty_table.csv'
    else:
        print('error in fixture_run_difficulty()')
        return None
    data = CSV_reader(file)
    data2 = CSV_reader(file2)
    teams = data[0]
    team_index = teams.index(team)
    difficulties = [data2[1][team_index], data2[2][team_index]]
    diffs = []
    opponents = []
    for i in range(start, finish + 1):
        row = data[i]
        if team not in row:
            opponents.append(sheet[i][team_index])
            diffs.append(colourDiffs_2(int(row[team_index]), opponents[len(opponents) - 1], difficulties))
            #if mode == 'ATT':
            #    diffs.append(colourDiffs_2(round((int(row[team_index]) / 132) - 2.5, 2), opponents[len(opponents) - 1], difficulties))
            #elif mode == 'DEF':
            #    diffs.append(colourDiffs_2(round((int(row[team_index]) / 99) - 3.5, 2), opponents[len(opponents) - 1], difficulties))
            #else:
            #    diffs.append(colourDiffs_2(round(int(row[team_index]) / 200, 2), opponents[len(opponents) - 1], difficulties))
    h_diffs = []
    a_diffs = []
    for i in range(2):
        difficulties[i] = '[color=#FF00FF]' + difficulties[i] + '[color=#FFFFFF]'
    for i in range(len(opponents)):
        if '(H)' in opponents[i]:
            h_diffs.append(diffs[i])
            a_diffs.append('')
        elif '(A)' in opponents[i]:
            h_diffs.append('')
            a_diffs.append(diffs[i])
        else:
            h_diffs.append('')
            a_diffs.append('')
    return [[h_diffs, a_diffs], opponents, difficulties]


def colourDiffs(num, game, strengths):
    if '(H)' in game:
        if num > float(strengths[0]):
            return Fore.RED + str(num) + Fore.RESET
        elif num < float(strengths[0]):
            return Fore.GREEN + str(num) + Fore.RESET
        else:
            return Fore.YELLOW + str(num) + Fore.RESET
    elif '(A)' in game:
        if num > float(strengths[1]):
            return Fore.RED + str(num) + Fore.RESET
        elif num < float(strengths[1]):
            return Fore.GREEN + str(num) + Fore.RESET
        else:
            return Fore.YELLOW + str(num) + Fore.RESET


def colourDiffs_2(num, game, strengths):
    if '(H)' in game:
        if num > float(strengths[0]):
            return '[color=#FF0000]' + str(num) + '[color=#FFFFFF]'
        elif num < float(strengths[0]):
            return '[color=#00FF00]' + str(num) + '[color=#FFFFFF]'
        else:
            return '[color=#FFFF00]' + str(num) + '[color=#FFFFFF]'
    elif '(A)' in game:
        if num > float(strengths[1]):
            return '[color=#FF0000]' + str(num) + '[color=#FFFFFF]'
        elif num < float(strengths[1]):
            return '[color=#00FF00]' + str(num) + '[color=#FFFFFF]'
        else:
            return '[color=#FFFF00]' + str(num) + '[color=#FFFFFF]'
    else:  # This takes care of BGWs
        return '[color=#FF0000]6[color=#FFFFFF]'
