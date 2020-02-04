import math
import numpy as np
import csv
from scipy.special import comb
from CSV_reader import CSV_reader
from colorama import init, Fore
from tqdm import tqdm


init(autoreset=True)


def stretchFn(list_num):
    soln = []
    for i in range(len(list_num)):
        if list_num[i] > 3.1:
            soln.append(round(2 * list_num[i] - 3.1, 1))
        else:
            soln.append(round(2 * list_num[i] - 3.1, 1))
    return soln


def fixtureFinder(team):
    sheet = CSV_reader('FPL_Fixtures.csv')  # all good
    fixtures = []
    att_difficulties = []
    def_difficulties = []
    teams = ['ARS', 'AVL', 'BOU', 'BHA', 'BUR', 'CHE', 'CRY', 'EVE', 'LEI', 'LIV', 'MCI', 'MUN', 'NEW', 'NOR', 'SHU',
             'SOU', 'TOT', 'WAT', 'WHU', 'WOL']
    team_index = teams.index(team)
    length = len(sheet)
    att_data = CSV_reader('FPL_Fixtures_numbered_att.csv')
    def_data = CSV_reader('FPL_Fixtures_numbered_def.csv')
    for i in range(1, length):
        att_difficulties.append(round(int(att_data[i][team_index]) / 220, 1))
        def_difficulties.append(round(int(def_data[i][team_index]) / 220, 1))
        fixtures.append(sheet[i][team_index])
    return [fixtures, stretchFn(att_difficulties), stretchFn(def_difficulties)]


class Player:

    def __init__(self, name, team, position):
        self.name = name
        self.team = team
        self.position = position


class Team:

    def __init__(self):
        self.players = []

    def addPlayer(self, name, team, position):

        self.players.append(Player(name, team, position))

    def removePlayer(self, name):

        with open('myTeam.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = []
            for row in reader:
                if not name in row:
                    data.append(row)
        try:
            print(data[14])
        except IndexError:
            pass
        with open('myTeam.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            for row in data:
                writer.writerow(row)

    def viewTeam(self, gameweek):

        player_list = []
        fixture_list = []
        difficulty_list = []

        for player in self.players:
            if player.position == 'G':
                fixtures = fixtureFinder(player.team)
                player_list.append(player.name)
                fixture_list.append(fixtures[0][gameweek - 1])
                difficulty_list.append(fixtures[1][gameweek - 1])

        for player in self.players:
            if player.position == 'D':
                fixtures = fixtureFinder(player.team)
                player_list.append(player.name)
                fixture_list.append(fixtures[0][gameweek - 1])
                difficulty_list.append(fixtures[1][gameweek - 1])

        for player in self.players:
            if player.position == 'M':
                fixtures = fixtureFinder(player.team)
                player_list.append(player.name)
                fixture_list.append(fixtures[0][gameweek - 1])
                difficulty_list.append(fixtures[2][gameweek - 1])

        for player in self.players:
            if player.position == 'A':
                fixtures = fixtureFinder(player.team)
                player_list.append(player.name)
                fixture_list.append(fixtures[0][gameweek - 1])
                difficulty_list.append(fixtures[2][gameweek - 1])

        return [player_list, fixture_list, difficulty_list]


def transfer_in(implementation, name, team, position):
    implementation.addPlayer(name, team, position)
    with open('myTeam.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, team, position])


def transfer_out(implementation):
    player = input('Player out name: ')
    position_out = None
    for players in implementation.players:
        if players.name == player:
            position_out = players.position
    implementation.removePlayer(player)
    return position_out


def transfer_out_2(implementation, plout_name):
    position_out = None
    for players in implementation.players:
        if players.name == plout_name:
            position_out = players.position
    implementation.removePlayer(plout_name)
    return position_out


def similar(integer, set):
    x = True
    if len(set) < 2:
        return False
    if integer in range(2, 7):
        for i in set:
            if i in range(2, 7):
                x = x and True
            else:
                x = x and False
        return x
    elif integer in range(7, 12):
        return False
    elif integer in range(12, 15):
        for i in set:
            if i in range(12, 15):
                x = x and True
            else:
                x = x and False
        return x


def teamPrinter(names, games):
    string = ''
    for name in names:
        string = ''.join([string, name])
        for j in range(13 - len(name)):
            string = ''.join([string, ' '])
    string2 = ''
    for game in games:
        string2 = ''.join([string2, game])
        for j in range(13 - len(game)):
            string2 = ''.join([string2, ' '])
    print(Fore.LIGHTMAGENTA_EX + string)
    print(Fore.GREEN + string2)


def benchPrinter(names, games):
    string = ''
    for name in names:
        string = ''.join([string, name])
        for j in range(13 - len(name)):
            string = ''.join([string, ' '])
    string2 = ''
    for game in games:
        string2 = ''.join([string2, game])
        for j in range(13 - len(game)):
            string2 = ''.join([string2, ' '])
    print(Fore.RED + string)
    print(Fore.RED + string2)


def teamEditor():
    choice = ''
    while choice != '0':
        implementation = Team()
        data = CSV_reader('myTeam.csv')
        for i in range(len(data)):
            implementation.addPlayer(data[i][0], data[i][1], data[i][2])

        choice = input('Make transfer or view team? (T / V) ')

        if choice == 'V' or choice == 'v':
            gameweek = int(input('Gameweek: '))
            output = implementation.viewTeam(gameweek)
            fodder_lower = CSV_reader('code_settings.csv')[2]
            nailed_lower = CSV_reader('code_settings.csv')[1]
            fodder = []
            nailed = []
            for i in range(len(fodder_lower)):
                fodder.append(fodder_lower[i].upper())
            for i in range(len(nailed_lower)):
                nailed.append(nailed_lower[i].upper())
            gk_list = []
            def_list = []
            mid_list = []
            fwd_list = []
            bench = []
            indices = []
            for j in range(3):
                max_diff = 0
                for i in range(2, 15):
                    if output[0][i] in fodder and i not in indices and not similar(i, indices):
                        maxv = i
                    elif output[2][i] > max_diff and i not in indices and output[0][i] not in nailed and not similar(i,
                                                                                                                     indices):
                        maxv = i
                        max_diff = output[2][i]
                indices.append(maxv)
            for i in range(2):
                player = [output[0][i], output[1][i], output[2][i]]
                gk_list.append(player)
            for i in range(2, 7):
                if i not in indices:
                    player = [output[0][i], output[1][i], output[2][i]]
                    def_list.append(player)
            for i in range(7, 12):
                if i not in indices:
                    player = [output[0][i], output[1][i], output[2][i]]
                    mid_list.append(player)
            for i in range(12, 15):
                if i not in indices:
                    player = [output[0][i], output[1][i], output[2][i]]
                    fwd_list.append(player)
            for i in range(3):
                bench.append([output[0][indices[i]], output[1][indices[i]], output[2][indices[i]]])
            gk_list.sort(key=lambda x: x[2])
            if gk_list[0][0] in fodder or gk_list[1][0] in nailed:
                bench.append(gk_list[0])
                gk_list = [gk_list[1]]
            else:
                bench.append(gk_list[1])
                gk_list = [gk_list[0]]
            def_list.sort(key=lambda x: x[2])
            mid_list.sort(key=lambda x: x[2])
            fwd_list.sort(key=lambda x: x[2])
            bench.sort(key=lambda x: x[2])
            print('')
            names = []
            games = []
            for i in range(len(gk_list)):
                names.append(gk_list[i][0])
                games.append(str(gk_list[i][1]) + ' ' + str(gk_list[i][2]))
            teamPrinter(names, games)
            print('')
            names = []
            games = []
            for i in range(len(def_list)):
                names.append(def_list[i][0])
                games.append(str(def_list[i][1]) + ' ' + str(def_list[i][2]))
            teamPrinter(names, games)
            print('')
            names = []
            games = []
            for i in range(len(mid_list)):
                names.append(mid_list[i][0])
                games.append(str(mid_list[i][1]) + ' ' + str(mid_list[i][2]))
            teamPrinter(names, games)
            print('')
            names = []
            games = []
            for i in range(len(fwd_list)):
                names.append(fwd_list[i][0])
                games.append(str(fwd_list[i][1]) + ' ' + str(fwd_list[i][2]))
            teamPrinter(names, games)
            print('')
            names = []
            games = []
            for i in range(len(bench)):
                names.append(bench[i][0])
                games.append(str(bench[i][1]) + ' ' + str(bench[i][2]))
            benchPrinter(names, games)

        elif choice == 'T' or choice == 't':
            pos_out = transfer_out(implementation)
            print('Player in:')
            name = input('Name: ')
            team = input('Team: ')
            transfer_in(implementation, name, team, pos_out)


def combinations_with_replacement(iterable, r):
    # combinations_with_replacement('ABC', 2) --> AA AB AC BB BC CC
    pool = tuple(iterable)
    n = len(pool)
    if not n and r:
        return
    indices = [0] * r
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != n - 1:
                break
        else:
            return
        indices[i:] = [indices[i] + 1] * (r - i)
        yield tuple(pool[i] for i in indices)


def alternativeFinder(current_list, pos, start_gw, stop_gw, no_to_rotate, fodder_positions):
    total_size = 0
    if pos == 'G':
        total_size = 2 - fodder_positions
    elif pos == 'D' or pos == 'M':
        total_size = 5 - fodder_positions
    elif pos == 'A':
        total_size = 3 - fodder_positions
    slots = total_size - len(current_list)
    if pos == 'G':
        teams = ['AVL', 'BOU', 'BHA', 'BUR', 'CRY', 'NEW', 'SHU', 'TOT', 'WOL']
    elif pos == 'D':
        teams = ['AVL', 'BOU', 'CRY', 'LEI', 'LIV', 'NEW', 'SHU', 'TOT']
    elif pos == 'M':
        teams = ['AVL', 'BHA', 'CHE', 'CRY', 'EVE', 'LEI', 'LIV', 'MCI', 'MUN', 'NOR', 'SHU', 'TOT']
    elif pos == 'A':
        teams = ['ARS', 'BHA', 'BOU', 'CHE', 'LEI', 'MCI', 'MUN', 'NOR', 'SOU', 'TOT', 'WOL']
    n = len(teams)
    all_combs = combinations_with_replacement(teams, slots)
    combs = []
    y = []
    total_combs = int(comb(slots + n - 1, slots))
    total_sec = round(total_combs * 0.15, 0)
    total_min = math.floor(total_sec / 60)
    total_sec = int(total_sec % 60)
    print(Fore.RED + 'Total number to check: ' + str(total_combs) + '. Est time: ' + str(total_min) + 'm ' + str(total_sec) + 's')
    for a_combo in tqdm(all_combs):
        a_combo = list(a_combo)
        for team in current_list:
            a_combo.append(team)
        combs.append(a_combo)
        diffs_for_each_team_in_combo = []
        for team in a_combo:
            if pos == 'G' or pos == 'D':
                diffs_for_each_team_in_combo.append(fixtureFinder(team)[1][start_gw:stop_gw])
            else:
                diffs_for_each_team_in_combo.append(fixtureFinder(team)[2][start_gw:stop_gw])
        diffs_per_gw = np.transpose(diffs_for_each_team_in_combo)
        best_pick_per_gw = []
        for gw_diff in diffs_per_gw:
            if pos == 'G':
                best_pick_per_gw.append(round(min(gw_diff), 1))
            else:
                best_pick_per_gw.append(round(np.mean([np.median(sorted(gw_diff)[:no_to_rotate]), np.mean(sorted(gw_diff)[:no_to_rotate])]), 1))
        max_required_pick = round(np.mean(sorted(best_pick_per_gw, reverse=True)[:min(3, stop_gw - start_gw + 1)]), 2)
        y.append(max_required_pick)
    table = []
    for i in range(len(combs)):
        x = combs[i]
        x.append(y[i])
        table.append(x)
    table.sort(key=lambda x: x[total_size])
    for i in range(min(15, len(table))):
        string_new_teams = ''
        string_old_teams = ''
        for j in range(slots):
            string_new_teams = ''.join([string_new_teams, table[i][j]])
            string_new_teams = ''.join([string_new_teams, '  '])
        for j in range(slots, total_size):
            string_old_teams = ''.join([string_old_teams, table[i][j]])
            string_old_teams = ''.join([string_old_teams, '  '])
        print(Fore.MAGENTA + string_new_teams + Fore.RESET + string_old_teams + str(table[i][len(table[0]) - 1]))


def teamPrinter_2(lis, idx, bench):
    if idx > len(lis) - 1:
        return '\n\n\n\n'
    elif not bench:
        return '[color=#FF00FF]'+lis[idx][0]+'[color=#00FF00]\n'+lis[idx][1]+'\n'+str(lis[idx][2])+'\n\n[color=#FFFFFF]'
    else:
        return '[color=#FF0000]'+lis[idx][0]+'\n'+lis[idx][1]+'\n'+str(lis[idx][2])+'\n\n[color=#FFFFFF]'


def teamEditor_2_view(gameweek):
    implementation = Team()
    data = CSV_reader('myTeam.csv')
    for i in range(len(data)):
        implementation.addPlayer(data[i][0], data[i][1], data[i][2])
    output = implementation.viewTeam(gameweek)
    fodder_lower = CSV_reader('code_settings.csv')[2]
    nailed_lower = CSV_reader('code_settings.csv')[1]
    fodder = []
    nailed = []
    for i in range(len(fodder_lower)):
        fodder.append(fodder_lower[i].upper())
    for i in range(len(nailed_lower)):
        nailed.append(nailed_lower[i].upper())
    gk_list = []
    def_list = []
    mid_list = []
    fwd_list = []
    bench = []
    indices = []
    for j in range(3):
        max_diff = 0
        bench_spot_filled = False
        i = 14
        maxv = 14
        while not bench_spot_filled:
            if output[1][i] == 'None' and i not in indices and not similar(i, indices):
                maxv = i
                bench_spot_filled = True
            elif output[0][i] in fodder and i not in indices and not similar(i, indices):
                maxv = i
                bench_spot_filled = True
            elif output[2][i] > max_diff and i not in indices and output[0][i] not in nailed and not similar(i,
                                                                                                             indices):
                maxv = i
                max_diff = output[2][i]
            if i == 2:
                bench_spot_filled = True
            else:
                i -= 1
        indices.append(maxv)
    for i in range(2):
        player = [output[0][i], output[1][i], output[2][i]]
        gk_list.append(player)
    for i in range(2, 7):
        if i not in indices:
            player = [output[0][i], output[1][i], output[2][i]]
            def_list.append(player)
    for i in range(7, 12):
        if i not in indices:
            player = [output[0][i], output[1][i], output[2][i]]
            mid_list.append(player)
    for i in range(12, 15):
        if i not in indices:
            player = [output[0][i], output[1][i], output[2][i]]
            fwd_list.append(player)
    for i in range(3):
        bench.append([output[0][indices[i]], output[1][indices[i]], output[2][indices[i]]])
    gk_list.sort(key=lambda x: x[2])
    if gk_list[0][0] in fodder or gk_list[1][0] == 'None' or gk_list[0][1] in nailed:
        bench.append(gk_list[0])
        gk_list = [gk_list[1]]
    else:
        bench.append(gk_list[1])
        gk_list = [gk_list[0]]
    def_list.sort(key=lambda x: x[2])
    mid_list.sort(key=lambda x: x[2])
    fwd_list.sort(key=lambda x: x[2])
    bench.sort(key=lambda x: x[2])
    col1 = teamPrinter_2(gk_list, 0, False)+teamPrinter_2(def_list, 0, False)+teamPrinter_2(mid_list, 0, False)+teamPrinter_2(fwd_list, 0, False)+teamPrinter_2(bench, 0, True)
    col2 = teamPrinter_2(gk_list, 1, False)+teamPrinter_2(def_list, 1, False)+teamPrinter_2(mid_list, 1, False)+teamPrinter_2(fwd_list, 1, False)+teamPrinter_2(bench, 1, True)
    col3 = teamPrinter_2(gk_list, 2, False)+teamPrinter_2(def_list, 2, False)+teamPrinter_2(mid_list, 2, False)+teamPrinter_2(fwd_list, 2, False)+teamPrinter_2(bench, 2, True)
    col4 = teamPrinter_2(gk_list, 3, False)+teamPrinter_2(def_list, 3, False)+teamPrinter_2(mid_list, 3, False)+teamPrinter_2(fwd_list, 3, False)+teamPrinter_2(bench, 3, True)
    col5 = teamPrinter_2(gk_list, 4, False)+teamPrinter_2(def_list, 4, False)+teamPrinter_2(mid_list, 4, False)+teamPrinter_2(fwd_list, 4, False)+teamPrinter_2(bench, 4, True)
    return [col1, col2, col3, col4, col5]


def teamEditor_2_transfer(player_out, player_in_name, player_in_team):
    implementation = Team()
    data = CSV_reader('myTeam.csv')
    for i in range(len(data)):
        implementation.addPlayer(data[i][0], data[i][1], data[i][2])
    pos_out = transfer_out_2(implementation, player_out)
    transfer_in(implementation, player_in_name, player_in_team, pos_out)


def alternativeFinder_2(current_list, pos, start_gw, stop_gw, no_to_rotate, fodder_positions):
    total_size = 0
    if pos == 'G':
        total_size = 2 - fodder_positions
    elif pos == 'D' or pos == 'M':
        total_size = 5 - fodder_positions
    elif pos == 'A':
        total_size = 3 - fodder_positions
    slots = total_size - len(current_list)
    allowed = CSV_reader('code_settings.csv')
    if pos == 'G':
        teams = allowed[3]
    elif pos == 'D':
        teams = allowed[4]
    elif pos == 'M':
        teams = allowed[5]
    elif pos == 'A':
        teams = allowed[6]
    else:
        print(pos)
        raise ValueError()
    n = len(teams)
    all_combs = combinations_with_replacement(teams, slots)
    combs = []
    y = []
    for a_combo in all_combs:
        a_combo = list(a_combo)
        for team in current_list:
            a_combo.append(team)
        combs.append(a_combo)
        diffs_for_each_team_in_combo = []
        for team in a_combo:
            if pos == 'G' or pos == 'D':
                diffs_for_each_team_in_combo.append(fixtureFinder(team)[1][start_gw:stop_gw])
            else:
                diffs_for_each_team_in_combo.append(fixtureFinder(team)[2][start_gw:stop_gw])
        diffs_per_gw = np.transpose(diffs_for_each_team_in_combo)
        best_pick_per_gw = []
        for gw_diff in diffs_per_gw:
            if pos == 'G':
                best_pick_per_gw.append(round(min(gw_diff), 1))
            else:
                best_pick_per_gw.append(round(np.mean([np.median(sorted(gw_diff)[:no_to_rotate]), np.mean(sorted(gw_diff)[:no_to_rotate])]), 1))
        max_required_pick = round(np.mean(sorted(best_pick_per_gw, reverse=True)[:min(3, stop_gw - start_gw + 1)]), 2)
        y.append(max_required_pick)
    table = []
    for i in range(len(combs)):
        x = combs[i]
        x.append(y[i])
        table.append(x)
    table.sort(key=lambda x: x[total_size])
    output = []
    for j in range(slots):
        col = ''
        for i in range(min(15, len(table))):
            col += table[i][j] + '\n'
        output.append(col)
    for j in range(slots, total_size + 1):
        col = ''
        for i in range(min(15, len(table))):
            col += str(table[i][j]) + '\n'
        output.append(col)
    return output


if __name__ == 'main':
    teamEditor()


