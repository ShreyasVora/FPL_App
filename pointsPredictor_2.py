import json
from urllib.request import urlopen, Request


def runPredictor_2(this_or_next, specific_team, **kwargs):
    filter_by_team = not ((specific_team is None) or (specific_team == ''))
    when = 'ep_' + this_or_next
    N = kwargs.get('view_top_N', 10)
    site = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    myDict = json.load(urlopen(Request(str(site), headers={'User-Agent': 'Mozilla/5.0'})))
    teams = ['ARS', 'AVL', 'BOU', 'BHA', 'BUR', 'CHE', 'CRY', 'EVE', 'LEI', 'LIV', 'MCI', 'MUN', 'NEW', 'NOR', 'SHU',
             'SOU', 'TOT', 'WAT', 'WHU', 'WOL']
    points_list = []
    for player in myDict['elements']:
        if player[when] is None:
            player[when] = 0
        if filter_by_team:
            if teams[player['team'] - 1] == specific_team:
                points_list.append([player['second_name'].split(' ')[len(player['second_name'].split(' ')) - 1], float((player[when]))])
        else:
            points_list.append([player['second_name'].split(' ')[len(player['second_name'].split(' ')) - 1], float((player[when]))])
    points_list.sort(key=lambda x: x[1], reverse=True)
    points_list = points_list[:N]
    col1 = '[color=#FFFF00]Name[color=#FFFFFF]'
    col2 = '[color=#FFFF00]xPts[color=#FFFFFF]'
    for i in range(len(points_list)):
        col1 += '\n' + points_list[i][0]
        col2 += '\n' + str(points_list[i][1])
    return [col1, col2]
