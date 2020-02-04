from CSV_reader import CSV_reader
from tabulate import tabulate
from colorama import init, Fore

init(autoreset=True)


def FPL_fixture_difficulty(start, finish, detail_level, type):
    """
    Extracts difficulties of upcoming fixtures for each team. Sums these difficulties, and sorts from lowest to highest.
    :param start: Which gameweek to begin analysis from
    :param finish: Which gameweek to end analysis at
    :param detail_level: Select 'detailed' to view second best team in each category too. Else, view only first.
    :param type: Select from 'OVR' or 'DEF' or 'ATT'
    :return: None
    """
    sheet = CSV_reader('FPL_Fixtures.csv')  # all good
    GWs = finish - start + 1
    if type == 'OVR':
        data = CSV_reader('FPL_Fixtures_numbered.csv')
    elif type == 'DEF':
        data = CSV_reader('FPL_Fixtures_numbered_def.csv')
    elif type == 'ATT':
        data = CSV_reader('FPL_Fixtures_numbered_att.csv')

    teams = ['ARS', 'AVL', 'BOU', 'BHA', 'BUR', 'CHE', 'CRY', 'EVE', 'LEI', 'LIV', 'MCI', 'MUN', 'NEW', 'NOR', 'SHU',
             'SOU', 'TOT', 'WAT', 'WHU', 'WOL']
    diffs_summed = []
    for j in range(20):
        sum_diffs = 0
        for i in range(start, finish + 1):
            sum_diffs += int(data[i][j])
        diffs_summed.append(round((sum_diffs - 100 * GWs) / (GWs * 200), 1))

    array = []
    for i in range(20):
        array.append((teams[i], diffs_summed[i]))

    def sortSecond(val):
        return val[1]

    array.sort(key=sortSecond)
    teams_sorted = []
    ratings_sorted = []
    for i in range(20):
        teams_sorted.append(array[i][0])
        ratings_sorted.append(array[i][1])
    if type == 'OVR':
        print('Teams most likely to win:')
    elif type == 'DEF':
        print('Buy ' + Fore.GREEN + 'attackers' + Fore.RESET + ' from:')
    elif type == 'ATT':
        print('Buy ' + Fore.GREEN + 'defenders' + Fore.RESET + ' from:')
    if detail_level == 'detailed':
        print(tabulate([teams_sorted, ratings_sorted], tablefmt='orgtbl'))

    first_best = teams_sorted[0]
    if detail_level == 'detailed':
        second_best = teams_sorted[1]

    first_fxt = ''
    if detail_level == 'detailed':
        second_fxt = ''
    for ind in range(start, finish + 1):
        first_fxt += sheet[ind][teams.index(first_best)]
        if detail_level == 'detailed':
            second_fxt += sheet[ind][teams.index(second_best)]
        if ind < finish:
            first_fxt += ', '
            if detail_level == 'detailed':
                second_fxt += ', '
    print(Fore.RED + first_best + Fore.RESET + ' play ' + first_fxt)
    if detail_level == 'detailed':
        print(Fore.RED + second_best + Fore.RESET + ' play ' + second_fxt)


def FPL_fixture_difficulty_2(start, finish, detail_level, type):
    """
    Extracts difficulties of upcoming fixtures for each team. Sums these difficulties, and sorts from lowest to highest.
    :param start: Which gameweek to begin analysis from
    :param finish: Which gameweek to end analysis at
    :param detail_level: Select 'detailed' to view second best team in each category too. Else, view only first.
    :param type: Select from 'OVR' or 'DEF' or 'ATT'
    :return: None
    """
    ret_val = []
    sheet = CSV_reader('FPL_Fixtures.csv')  # all good
    GWs = finish - start + 1
    if type == 'OVR':
        data = CSV_reader('FPL_Fixtures_numbered.csv')
    elif type == 'DEF':
        data = CSV_reader('FPL_Fixtures_numbered_def.csv')
    elif type == 'ATT':
        data = CSV_reader('FPL_Fixtures_numbered_att.csv')

    teams = ['ARS', 'AVL', 'BOU', 'BHA', 'BUR', 'CHE', 'CRY', 'EVE', 'LEI', 'LIV', 'MCI', 'MUN', 'NEW', 'NOR', 'SHU',
             'SOU', 'TOT', 'WAT', 'WHU', 'WOL']
    diffs_summed = []
    for j in range(20):
        sum_diffs = 0
        for i in range(start, finish + 1):
            sum_diffs += int(data[i][j])
        diffs_summed.append(sum_diffs // GWs)
    print(diffs_summed)

    array = []
    for i in range(20):
        array.append((teams[i], diffs_summed[i]))

    def sortSecond(val):
        return val[1]

    array.sort(key=sortSecond)
    total_array = array[:10]
    if type == 'DEF':
        ret_val.append('Buy [color=#FF00FF]attackers[color=#FFFFFF] from:')
    elif type == 'ATT':
        ret_val.append('Buy [color=#FF00FF]defenders[color=#FFFFFF] from:')
    if detail_level == 'detailed':
        ret_val.append(tabulate(total_array, tablefmt='plain'))

    first_best = total_array[0][0]
    second_best = []
    if detail_level == 'detailed':
        second_best = total_array[1][0]

    first_fxt = ''
    second_fxt = ''
    for ind in range(start, finish + 1):
        first_fxt += sheet[ind][teams.index(first_best)]
        if detail_level == 'detailed':
            second_fxt += sheet[ind][teams.index(second_best)]
        if ind < finish:
            first_fxt += ', '
            if detail_level == 'detailed':
                second_fxt += ', '
    if detail_level == 'detailed':
        ret_val.append(['[color=#00FF00]' + first_best + '[color=#FFFFFF] play ' + first_fxt,
                        '[color=#00FF00]' + second_best + '[color=#FFFFFF] play ' + second_fxt])
    else:
        ret_val.append('[color=#00FF00]' + first_best + '[color=#FFFFFF] play ' + first_fxt)
    return ret_val
