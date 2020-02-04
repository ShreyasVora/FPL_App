# Requirements:
# numpy, math, csv, kivy, asyncio, aiohttp, understat, tabulate, colorama, pandas, statsmodels, scipy, tqdm, pickle, urllib, json

import asyncio
import math
import csv
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from CSV_reader import CSV_reader
from FPL_future import scorePredictor, colourNumbers_2, roundPredictor_2
from FPL_past import fixtureFinder
from fixture_difficulty_calculator import FPL_fixture_difficulty_2
from fixture_run_diff import fixture_run_difficulty_2
from goal_extractor import update_goalscorers, list_goalscorers_2, list_assisters_2
from myPlan import editPlan_2
from myTeam import Team, teamEditor_2_view, teamEditor_2_transfer, alternativeFinder_2
from pointsPredictor_2 import runPredictor_2
from update_xlsx_files import update_diff_lists_2, update_scores_2, update_diff_table


def listJoiner(lis):
    x = ''
    for i in lis:
        x += str(i) + '\n'
    return x


class MainWindow(Screen):
    def helpbutton(self):
        show_menu_help()


def show_menu_help():
    show = main_menu_help()
    popupWindow = Popup(title='', separator_height=0, content=show, size_hint=(0.8, 0.8))
    popupWindow.open()


class main_menu_help(FloatLayout):
    pass


class Set_Team(Screen):
    pn1 = ObjectProperty(None)
    tn1 = ObjectProperty(None)
    ps1 = ObjectProperty(None)
    pn2 = ObjectProperty(None)
    tn2 = ObjectProperty(None)
    ps2 = ObjectProperty(None)
    pn3 = ObjectProperty(None)
    tn3 = ObjectProperty(None)
    ps3 = ObjectProperty(None)
    pn4 = ObjectProperty(None)
    tn4 = ObjectProperty(None)
    ps4 = ObjectProperty(None)
    pn5 = ObjectProperty(None)
    tn5 = ObjectProperty(None)
    ps5 = ObjectProperty(None)
    pn6 = ObjectProperty(None)
    tn6 = ObjectProperty(None)
    ps6 = ObjectProperty(None)
    pn7 = ObjectProperty(None)
    tn7 = ObjectProperty(None)
    ps7 = ObjectProperty(None)
    pn8 = ObjectProperty(None)
    tn8 = ObjectProperty(None)
    ps8 = ObjectProperty(None)
    pn9 = ObjectProperty(None)
    tn9 = ObjectProperty(None)
    ps9 = ObjectProperty(None)
    pn10 = ObjectProperty(None)
    tn10 = ObjectProperty(None)
    ps10 = ObjectProperty(None)
    pn11 = ObjectProperty(None)
    tn11 = ObjectProperty(None)
    ps11 = ObjectProperty(None)
    pn12 = ObjectProperty(None)
    tn12 = ObjectProperty(None)
    ps12 = ObjectProperty(None)
    pn13 = ObjectProperty(None)
    tn13 = ObjectProperty(None)
    ps13 = ObjectProperty(None)
    pn14 = ObjectProperty(None)
    tn14 = ObjectProperty(None)
    ps14 = ObjectProperty(None)
    pn15 = ObjectProperty(None)
    tn15 = ObjectProperty(None)
    ps15 = ObjectProperty(None)

    def write_team(self):
        data = [[self.pn1.text.upper(), self.tn1.text.upper(), self.ps1.text.upper()],
                [self.pn2.text.upper(), self.tn2.text.upper(), self.ps2.text.upper()],
                [self.pn3.text.upper(), self.tn3.text.upper(), self.ps3.text.upper()],
                [self.pn4.text.upper(), self.tn4.text.upper(), self.ps4.text.upper()],
                [self.pn5.text.upper(), self.tn5.text.upper(), self.ps5.text.upper()],
                [self.pn6.text.upper(), self.tn6.text.upper(), self.ps6.text.upper()],
                [self.pn7.text.upper(), self.tn7.text.upper(), self.ps7.text.upper()],
                [self.pn8.text.upper(), self.tn8.text.upper(), self.ps8.text.upper()],
                [self.pn9.text.upper(), self.tn9.text.upper(), self.ps9.text.upper()],
                [self.pn10.text.upper(), self.tn10.text.upper(), self.ps10.text.upper()],
                [self.pn11.text.upper(), self.tn11.text.upper(), self.ps11.text.upper()],
                [self.pn12.text.upper(), self.tn12.text.upper(), self.ps12.text.upper()],
                [self.pn13.text.upper(), self.tn13.text.upper(), self.ps13.text.upper()],
                [self.pn14.text.upper(), self.tn14.text.upper(), self.ps14.text.upper()],
                [self.pn15.text.upper(), self.tn15.text.upper(), self.ps15.text.upper()]]
        if self.pn1.text == '' or self.pn2.text == '' or self.pn3.text == '' or self.pn4.text == '' or self.pn5.text == '' or self.pn6.text == '' or self.pn7.text == '' or self.pn8.text == '' or self.pn9.text == '' or self.pn10.text == '' or self.pn11.text == '' or self.pn12.text == '' or self.pn13.text == '' or self.pn14.text == '' or self.pn15.text == '' or self.tn1.text == '' or self.tn2.text == '' or self.tn3.text == '' or self.tn4.text == '' or self.tn5.text == '' or self.tn6.text == '' or self.tn7.text == '' or self.tn8.text == '' or self.tn9.text == '' or self.tn10.text == '' or self.tn11.text == '' or self.tn12.text == '' or self.tn13.text == '' or self.tn14.text == '' or self.tn15.text == '' or self.ps1.text == '' or self.ps2.text == '' or self.ps3.text == '' or self.ps4.text == '' or self.ps5.text == '' or self.ps6.text == '' or self.ps7.text == '' or self.ps8.text == '' or self.ps9.text == '' or self.ps10.text == '' or self.ps11.text == '' or self.ps12.text == '' or self.ps13.text == '' or self.ps14.text == '' or self.ps15.text == '':
            show_error_popup()
        else:
            with open('myTeam.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                for row in data:
                    writer.writerow(row)
            show_done_popup()


def show_done_popup():
    show = done_popup()
    popupWindow = Popup(title='Done', content=show, size_hint=(0.5, 0.2))
    popupWindow.open()


class done_popup(FloatLayout):
    pass


class FixtureDiffs(Screen):
    def viewTables(self):
        data = update_diff_lists_2('DEF')
        def_table_h = data[2]
        def_table_h.insert(0, '[color=#FFFF00]Home[color=#FFFFFF]')
        def_table_a = data[1]
        def_table_a.insert(0, '[color=#FFFF00]Away[color=#FFFFFF]')
        teams = ['', 'ARS', 'AVL', 'BHA', 'BOU', 'BUR', 'CHE', 'CRY', 'EVE', 'LEI', 'LIV', 'MCI', 'MUN', 'NEW', 'NOR',
                 'SHU', 'SOU', 'TOT', 'WAT', 'WHU', 'WOL']
        data = update_diff_lists_2('ATT')
        att_table_h = data[2]
        att_table_h.insert(0, '[color=#FFFF00]Home[color=#FFFFFF]')
        att_table_a = data[1]
        att_table_a.insert(0, '[color=#FFFF00]Away[color=#FFFFFF]')
        update_diff_table()
        show_popup_1_4(def_table_h, def_table_a, teams, att_table_h, att_table_a)


class Screen1_1(Screen):
    gw_start = ObjectProperty(None)
    gw_end = ObjectProperty(None)

    def runFixDiffCalc(self):
        try:
            if int(self.gw_start.text) > int(self.gw_end.text):
                show_error_popup()
            else:
                data1 = FPL_fixture_difficulty_2(int(self.gw_start.text), int(self.gw_end.text), 'detailed', 'DEF')
                data2 = FPL_fixture_difficulty_2(int(self.gw_start.text), int(self.gw_end.text), 'detailed', 'ATT')
                show_popup_1_1(data1, data2)
        except (ValueError, IndexError):
            show_error_popup()


class Screen1_2(Screen):
    gw_start = ObjectProperty(None)

    def runGeneralCalc(self):
        try:
            y = ''
            for finish in range(int(self.gw_start.text), int(self.gw_start.text) + 6):
                y += '\nOver the course of ' + str(finish - int(self.gw_start.text) + 1) + ' gameweeks:\n'
                x1 = FPL_fixture_difficulty_2(int(self.gw_start.text), finish, 'none', 'DEF')
                x2 = FPL_fixture_difficulty_2(int(self.gw_start.text), finish, 'none', 'ATT')
                y += x1[0] + ' ' + x1[1] + '\n' + x2[0] + ' ' + x2[1] + '\n'
            show_popup_1_2(y)
        except (ValueError, IndexError):
            show_error_popup()


class Screen1_3(Screen):
    gw_start = ObjectProperty(None)
    gw_end = ObjectProperty(None)
    team_name = ObjectProperty(None)

    def runTeamCalc(self):
        try:
            def_ratings = fixture_run_difficulty_2(int(self.gw_start.text), int(self.gw_end.text),
                                                   self.team_name.text.upper(), 'DEF')
            att_ratings = fixture_run_difficulty_2(int(self.gw_start.text), int(self.gw_end.text),
                                                   self.team_name.text.upper(), 'ATT')
            def_table_h = def_ratings[0][0]
            def_table_h.insert(0, def_ratings[2][0])
            def_table_a = def_ratings[0][1]
            def_table_a.insert(0, def_ratings[2][1])
            def_table_fixtures = def_ratings[1]
            def_table_fixtures.insert(0, self.team_name.text.upper())
            att_table_h = att_ratings[0][0]
            att_table_h.insert(0, att_ratings[2][0])
            att_table_a = att_ratings[0][1]
            att_table_a.insert(0, att_ratings[2][1])
            show_popup_1_3(def_table_h, def_table_a, def_table_fixtures, att_table_h, att_table_a)
        except (ValueError, IndexError):
            show_error_popup()


class popup_1_1(FloatLayout):
    def __init__(self, data1, data2, **kwargs):
        super().__init__(**kwargs)
        self.ids.table1.text = str(data1[0] + '\n' + data1[1] + '\n' + data1[2][0] + '\n' + data1[2][1])
        self.ids.table2.text = str(data2[0] + '\n' + data2[1] + '\n' + data2[2][0] + '\n' + data2[2][1])


class popup_1_2(FloatLayout):
    def __init__(self, string, **kwargs):
        super().__init__(**kwargs)
        self.ids.summary.text = string


class popup_1_3(FloatLayout):
    def __init__(self, def_table_h, def_table_a, def_table_fixtures, att_table_h, att_table_a, **kwargs):
        super().__init__(**kwargs)
        self.ids.HDtab.text = listJoiner(def_table_h)
        self.ids.ADtab.text = listJoiner(def_table_a)
        self.ids.Df.text = listJoiner(def_table_fixtures)
        self.ids.HAtab.text = listJoiner(att_table_h)
        self.ids.AAtab.text = listJoiner(att_table_a)


class popup_1_4(FloatLayout):
    def __init__(self, def_table_h, def_table_a, teams, att_table_h, att_table_a, **kwargs):
        super().__init__(**kwargs)
        self.ids.HDtab.text = listJoiner(def_table_h)
        self.ids.ADtab.text = listJoiner(def_table_a)
        self.ids.Df.text = listJoiner(teams)
        self.ids.HAtab.text = listJoiner(att_table_h)
        self.ids.AAtab.text = listJoiner(att_table_a)


def show_popup_1_1(data1, data2):
    show = popup_1_1(data1, data2)
    popupWindow = Popup(title='Fixture Difficulty Sums', content=show, size_hint=(0.8, 0.8))
    popupWindow.open()


def show_popup_1_2(string):
    show = popup_1_2(string)
    popupWindow = Popup(title='Best Fixture Runs', content=show, size_hint=(0.8, 0.8))
    popupWindow.open()


def show_popup_1_3(def_table_h, def_table_a, def_table_fixtures, att_table_h, att_table_a):
    show = popup_1_3(def_table_h, def_table_a, def_table_fixtures, att_table_h, att_table_a)
    popupWindow = Popup(title='Team Upcoming Fixture List', content=show, size_hint=(0.96, 0.7))
    popupWindow.open()


def show_popup_1_4(def_table_h, def_table_a, teams, att_table_h, att_table_a):
    show = popup_1_4(def_table_h, def_table_a, teams, att_table_h, att_table_a)
    popupWindow = Popup(title='Team Difficulty Ratings ', content=show, size_hint=(0.8, 0.8))
    popupWindow.open()


class UpdateFiles(Screen):
    def updateScoresPopup(self):
        show_popup_2_1(update_scores_2())

    def goalscorers(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(update_goalscorers())


class Screen2_2(Screen):
    def topGS(self):
        data = list_goalscorers_2()
        col1 = '[color=#FFFF00]Name[color=#FFFFFF]'
        col2 = '[color=#FFFF00]Goals[color=#FFFFFF]'
        col3 = '[color=#FFFF00]Assists[color=#FFFFFF]'
        for i in range(len(data)):
            col1 += '\n' + str(data[i][0])
            col2 += '\n' + str(data[i][1])
            col3 += '\n' + str(data[i][2])
        show_popup_2_2_g(col1, col2, col3)

    def topA(self):
        data = list_assisters_2()
        col1 = '[color=#FFFF00]Name[color=#FFFFFF]'
        col2 = '[color=#FFFF00]Goals[color=#FFFFFF]'
        col3 = '[color=#FFFF00]Assists[color=#FFFFFF]'
        for i in range(len(data)):
            col1 += '\n' + str(data[i][0])
            col2 += '\n' + str(data[i][1])
            col3 += '\n' + str(data[i][2])
        show_popup_2_2_a(col1, col2, col3)


class popup_2_1(FloatLayout):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.ids.HDtab.text = data


class popup_2_2_g(FloatLayout):
    def __init__(self, col1, col2, col3, **kwargs):
        super().__init__(**kwargs)
        self.ids.col1.text = col1
        self.ids.col2.text = col2
        self.ids.col3.text = col3


class popup_2_2_a(FloatLayout):
    def __init__(self, col1, col2, col3, **kwargs):
        super().__init__(**kwargs)
        self.ids.col1.text = col1
        self.ids.col2.text = col2
        self.ids.col3.text = col3


def show_popup_2_1(info):
    show = popup_2_1(info)
    popupWindow = Popup(title='Latest Scores + Rating changes', content=show, size_hint=(0.96, 0.7))
    popupWindow.open()


def show_popup_2_2_g(col1, col2, col3):
    show = popup_2_2_g(col1, col2, col3)
    popupWindow = Popup(title='Top Goalscorers', content=show, size_hint=(0.8, 0.8))
    popupWindow.open()


def show_popup_2_2_a(col1, col2, col3):
    show = popup_2_2_a(col1, col2, col3)
    popupWindow = Popup(title='Top Assisters', content=show, size_hint=(0.8, 0.8))
    popupWindow.open()


class PredictFixture(Screen):
    h_team = ObjectProperty(None)
    a_team = ObjectProperty(None)

    def scorepred(self):
        teams_fff = ['ARS', 'AVL', 'BOU', 'BHA', 'BUR', 'CHE', 'CRY', 'EVE', 'LEI', 'LIV', 'MCI', 'MUN', 'NEW', 'NOR',
                     'SHU',
                     'SOU', 'TOT', 'WAT', 'WHU', 'WOL']
        if self.h_team.text.upper() in teams_fff and self.a_team.text.upper() in teams_fff:
            data = scorePredictor(self.h_team.text.upper(), self.a_team.text.upper())
            array = [self.h_team.text.upper(), str(round(data[0], 2)), str(round(data[1], 2)), self.a_team.text.upper()]
            show_popup_3_1(array)
        else:
            show_error_popup()

    def cspred(self):
        teams_fff = ['ARS', 'AVL', 'BOU', 'BHA', 'BUR', 'CHE', 'CRY', 'EVE', 'LEI', 'LIV', 'MCI', 'MUN', 'NEW', 'NOR',
                     'SHU',
                     'SOU', 'TOT', 'WAT', 'WHU', 'WOL']
        if self.h_team.text.upper() in teams_fff and self.a_team.text.upper() in teams_fff:
            data = scorePredictor(self.h_team.text.upper(), self.a_team.text.upper())
            z = [round(data[0], 2), round(data[1], 2)]
            y = [0, 0]
            y[0] = 100 * math.exp(- z[0])
            y[1] = 100 * math.exp(- z[1])
            z[1] = round(y[0], 1 - int(math.floor(math.log10(abs(y[0])))))
            z[0] = round(y[1], 1 - int(math.floor(math.log10(abs(y[1])))))
            array = [self.h_team.text.upper(), colourNumbers_2(z[0]), colourNumbers_2(z[1]), self.a_team.text.upper()]
            show_popup_3_2(array)
        else:
            show_error_popup()


class popup_3_1(FloatLayout):
    def __init__(self, info, **kwargs):
        super().__init__(**kwargs)
        self.ids.hname.text = info[0]
        self.ids.hgoals.text = info[1]
        self.ids.agoals.text = info[2]
        self.ids.aname.text = info[3]


class popup_3_2(FloatLayout):
    def __init__(self, info, **kwargs):
        super().__init__(**kwargs)
        self.ids.hname.text = info[0]
        self.ids.hpct.text = info[1]
        self.ids.apct.text = info[2]
        self.ids.aname.text = info[3]


def show_popup_3_1(info):
    show = popup_3_1(info)
    popupWindow = Popup(title=info[0] + ' vs ' + info[3] + ' prediction', content=show, size_hint=(0.6, 0.2))
    popupWindow.open()


def show_popup_3_2(info):
    show = popup_3_1(info)
    popupWindow = Popup(title='Clean Sheet Probabilities', content=show, size_hint=(0.6, 0.2))
    popupWindow.open()


class PredictRound(Screen):
    gw = ObjectProperty(None)

    def scorepred(self):
        try:
            if int(self.gw.text) < 1:
                show_error_popup()
            else:
                data = roundPredictor_2(int(self.gw.text), cs=False)
                show_popup_4_1(data, int(self.gw.text))
        except (ValueError, IndexError):
            show_error_popup()

    def cspred(self):
        try:
            if int(self.gw.text) < 1:
                show_error_popup()
            else:
                data = roundPredictor_2(int(self.gw.text), cs=True)
                show_popup_4_2(data, int(self.gw.text))
        except (ValueError, IndexError):
            show_error_popup()


class popup_4_1(FloatLayout):
    def __init__(self, info, **kwargs):
        super().__init__(**kwargs)
        self.ids.hname.text = info[0]
        self.ids.hgoals.text = info[1]
        self.ids.agoals.text = info[2]
        self.ids.aname.text = info[3]


class popup_4_2(FloatLayout):
    def __init__(self, info, **kwargs):
        super().__init__(**kwargs)
        self.ids.hname.text = info[0]
        self.ids.hpct.text = info[1]
        self.ids.apct.text = info[2]
        self.ids.aname.text = info[3]


def show_popup_4_1(info, gw):
    show = popup_4_1(info)
    popupWindow = Popup(title='GW' + str(gw) + ' score prediction', content=show, size_hint=(0.6, 0.5))
    popupWindow.open()


def show_popup_4_2(info, gw):
    show = popup_4_2(info)
    popupWindow = Popup(title='GW' + str(gw) + ' clean sheet probabilities', content=show, size_hint=(0.6, 0.5))
    popupWindow.open()


class PredictTopPoints(Screen):
    specific_team = ObjectProperty(None)
    def runpred_this(self):
        try:
            data = runPredictor_2(this_or_next='this', specific_team=self.specific_team.text.upper(), view_top_N=25)
            show_popup_5(data, 'This')
        except (ValueError, IndexError):
            show_error_popup()
    def runpred_next(self):
        try:
            data = runPredictor_2(this_or_next='next', specific_team=self.specific_team.text.upper(), view_top_N=25)
            show_popup_5(data, 'Next')
        except (ValueError, IndexError):
            show_error_popup()

class popup_5(FloatLayout):
    def __init__(self, info, **kwargs):
        super().__init__(**kwargs)
        self.ids.names.text = info[0]
        self.ids.xP.text = info[1]


def show_popup_5(info, gw):
    show = popup_5(info)
    popupWindow = Popup(title= gw + ' gameweek points prediction', content=show, size_hint=(0.7, 0.8))
    popupWindow.open()


class ViewPastResults(Screen):
    def resultsH(self):
        teams_fff = ['ARS', 'AVL', 'BOU', 'BHA', 'BUR', 'CHE', 'CRY', 'EVE', 'LEI', 'LIV', 'MCI', 'MUN', 'NEW', 'NOR',
                     'SHU', 'SOU', 'TOT', 'WAT', 'WHU', 'WOL']
        if self.tname.text.upper() in teams_fff:
            x = fixtureFinder(self.tname.text.upper(), 'H')
            results = listJoiner(x[0])
            show_popup_6_I(results, x[1], self.tname.text.upper(), 'Home')
        else:
            show_error_popup()

    def resultsA(self):
        teams_fff = ['ARS', 'AVL', 'BOU', 'BHA', 'BUR', 'CHE', 'CRY', 'EVE', 'LEI', 'LIV', 'MCI', 'MUN', 'NEW', 'NOR',
                     'SHU', 'SOU', 'TOT', 'WAT', 'WHU', 'WOL']
        if self.tname.text.upper() in teams_fff:
            x = fixtureFinder(self.tname.text.upper(), 'A')
            results = listJoiner(x[0])
            show_popup_6_I(results, x[1], self.tname.text.upper(), 'Away')
        else:
            show_error_popup()

    def resultsO(self):
        teams_fff = ['ARS', 'AVL', 'BOU', 'BHA', 'BUR', 'CHE', 'CRY', 'EVE', 'LEI', 'LIV', 'MCI', 'MUN', 'NEW', 'NOR',
                     'SHU', 'SOU', 'TOT', 'WAT', 'WHU', 'WOL']
        if self.tname.text.upper() in teams_fff:
            x = fixtureFinder(self.tname.text.upper(), 'E')
            hresults = listJoiner(x[0])
            aresults = listJoiner(x[1])
            show_popup_6_O(hresults, aresults, x[2], x[3], self.tname.text.upper(), 'Season')
        else:
            show_error_popup()


class popup_6_I(FloatLayout):
    def __init__(self, data, table, **kwargs):
        super().__init__(**kwargs)
        self.ids.results.text = data
        self.ids.table1.text = 'P\n' + str(table[0])
        self.ids.table2.text = 'W\n' + str(table[1])
        self.ids.table3.text = 'D\n' + str(table[2])
        self.ids.table4.text = 'L\n' + str(table[3])
        self.ids.table5.text = 'GF\n' + str(table[4])
        self.ids.table6.text = 'GA\n' + str(table[5])
        self.ids.table7.text = 'GD\n' + str(table[6])
        self.ids.table8.text = 'Pts\n' + str(table[7])


class popup_6_O(FloatLayout):
    def __init__(self, hgames, agames, htable, atable, **kwargs):
        super().__init__(**kwargs)
        self.ids.hresults.text = hgames
        self.ids.aresults.text = agames
        self.ids.table0.text = '\nHome\nAway'
        self.ids.table1.text = 'P\n' + str(htable[0]) + '\n' + str(atable[0])
        self.ids.table2.text = 'W\n' + str(htable[1]) + '\n' + str(atable[1])
        self.ids.table3.text = 'D\n' + str(htable[2]) + '\n' + str(atable[2])
        self.ids.table4.text = 'L\n' + str(htable[3]) + '\n' + str(atable[3])
        self.ids.table5.text = 'GF\n' + str(htable[4]) + '\n' + str(atable[4])
        self.ids.table6.text = 'GA\n' + str(htable[5]) + '\n' + str(atable[5])
        self.ids.table7.text = 'GD\n' + str(htable[6]) + '\n' + str(atable[6])
        self.ids.table8.text = 'Pts\n' + str(htable[7]) + '\n' + str(atable[7])


def show_popup_6_I(results, table, name, place):
    show = popup_6_I(results, table)
    popupWindow = Popup(title=name + ' ' + place + ' results', content=show, size_hint=(0.9, 0.8))
    popupWindow.open()


def show_popup_6_O(hresults, aresults, htable, atable, name, place):
    show = popup_6_O(hresults, aresults, htable, atable)
    popupWindow = Popup(title=name + ' ' + place + ' results', content=show, size_hint=(0.9, 0.8))
    popupWindow.open()


class ViewTables(Screen):
    def tablesH(self):
        teams = ['ARS', 'AVL', 'BOU', 'BHA', 'BUR', 'CHE', 'CRY', 'EVE', 'LEI', 'LIV', 'MCI', 'MUN', 'NEW', 'NOR',
                 'SHU', 'SOU', 'TOT', 'WAT', 'WHU', 'WOL']
        table = []
        for team_name in teams:
            output = fixtureFinder(team_name, 'H')
            results = output[1]
            results = [str(x) for x in results]
            results.insert(0, team_name)
            results[8] = int(results[8])
            table.append(results)
        table.sort(key=lambda x: x[8], reverse=True)
        for i in range(20):
            table[i][0] = str(i + 1) + ' ' + table[i][0]
        table.insert(0, ['#', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'])
        data = []
        for i in range(9):
            data.append([row[i] for row in table])
        show_popup_7(data, 'Home')

    def tablesA(self):
        teams = ['ARS', 'AVL', 'BOU', 'BHA', 'BUR', 'CHE', 'CRY', 'EVE', 'LEI', 'LIV', 'MCI', 'MUN', 'NEW', 'NOR',
                 'SHU', 'SOU', 'TOT', 'WAT', 'WHU', 'WOL']
        table = []
        for team_name in teams:
            output = fixtureFinder(team_name, 'A')
            results = output[1]
            results = [str(x) for x in results]
            results.insert(0, team_name)
            results[8] = int(results[8])
            table.append(results)
        table.sort(key=lambda x: x[8], reverse=True)
        for i in range(20):
            table[i][0] = str(i + 1) + ' ' + table[i][0]
        table.insert(0, ['#', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'])
        data = []
        for i in range(9):
            data.append([row[i] for row in table])
        show_popup_7(data, 'Away')

    def tablesO(self):
        teams = ['ARS', 'AVL', 'BOU', 'BHA', 'BUR', 'CHE', 'CRY', 'EVE', 'LEI', 'LIV', 'MCI', 'MUN', 'NEW', 'NOR',
                 'SHU', 'SOU', 'TOT', 'WAT', 'WHU', 'WOL']
        table = []
        for team_name in teams:
            output = fixtureFinder(team_name, 'E')
            results = output[2].__add__(output[3])
            results = [str(x) for x in results]
            results.insert(0, team_name)
            results[8] = int(results[8])
            table.append(results)
        table.sort(key=lambda x: x[8], reverse=True)
        for i in range(20):
            table[i][0] = str(i + 1) + ' ' + table[i][0]
        table.insert(0, ['#', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts'])
        data = []
        for i in range(9):
            data.append([row[i] for row in table])
        show_popup_7(data, 'Overall')


class popup_7(FloatLayout):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.ids.col0.text = listJoiner(data[0])
        self.ids.col1.text = listJoiner(data[1])
        self.ids.col2.text = listJoiner(data[2])
        self.ids.col3.text = listJoiner(data[3])
        self.ids.col4.text = listJoiner(data[4])
        self.ids.col5.text = listJoiner(data[5])
        self.ids.col6.text = listJoiner(data[6])
        self.ids.col7.text = listJoiner(data[7])
        self.ids.col8.text = listJoiner(data[8])


def show_popup_7(data, place):
    show = popup_7(data)
    popupWindow = Popup(title='EPL table (' + place + ')', content=show, size_hint=(0.8, 0.6))
    popupWindow.open()


class FPLPlan(Screen):
    gmwk = ObjectProperty(None)
    plin = ObjectProperty(None)
    plout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.callback)

    def callback(self, dt):
        data = CSV_reader('plan.csv')
        col1 = [row[0] for row in data]
        col2 = [row[1].replace('&', ', ') for row in data]
        col3 = [row[2].replace('&', ', ') for row in data]
        self.ids.gw.text = '[color=#FFFF00]GW[color=#FFFFFF]\n' + listJoiner(col1)
        self.ids.tin.text = '[color=#FFFF00]Transfers In[color=#FFFFFF]\n' + listJoiner(col2)
        self.ids.tout.text = '[color=#FFFF00]Transfers Out[color=#FFFFFF]\n' + listJoiner(col3)

    def addTransfer(self):
        try:
            editPlan_2(1, GW_no=int(self.gmwk.text), player_in=self.plin.text, player_out=self.plout.text)
            self.callback(1)
        except (ValueError, IndexError):
            show_error_popup()

    def removeTransfer(self):
        try:
            editPlan_2(2, GW_no=int(self.gmwk.text), player_in=self.plin.text, player_out=self.plout.text)
            self.callback(1)
        except (ValueError, IndexError):
            show_error_popup()

    def deleteGW(self):
        try:
            editPlan_2(3, GW_no=int(self.gmwk.text))
            self.callback(1)
        except (ValueError, IndexError):
            show_error_popup()


class FPLTeam(Screen):
    pos_var = ObjectProperty(None)
    teams_var = ObjectProperty(None)
    nums_var = ObjectProperty(None)
    gw = ObjectProperty(None)
    plout = ObjectProperty(None)
    plinN = ObjectProperty(None)
    plinT = ObjectProperty(None)
    gw_start = ObjectProperty(None)
    gw_end = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initialiser = True
        self.teams = []
        Clock.schedule_once(self.callback)

    def callback(self, gmwk):
        if self.initialiser:
            gmwk = 1
            self.initialiser = False
        elif self.gw.text == '':
            gmwk = 1
        implementation = Team()
        data = CSV_reader('myTeam.csv')
        for i in range(len(data)):
            implementation.addPlayer(data[i][0], data[i][1], data[i][2])
        data = teamEditor_2_view(gmwk)
        self.ids.col1.text = data[0]
        self.ids.col2.text = data[1]
        self.ids.col3.text = data[2]
        self.ids.col4.text = data[3]
        self.ids.col5.text = data[4]
        self.ids.currentgw.text = 'GW' + str(gmwk) + ' Team'

    def updateteam(self):
        try:
            if int(self.gw.text) < 1 or int(self.gw.text) > 38:
                show_error_popup()
            else:
                self.callback(int(self.gw.text))
        except (ValueError, IndexError):
            show_error_popup()

    def maketransfer(self):
        try:
            if self.plinN.text == '' or self.plinT.text == '' or self.plout.text == '':
                show_error_popup()
            else:
                teamEditor_2_transfer(self.plout.text.upper(), self.plinN.text.upper(), self.plinT.text.upper())
        except (IndexError, ValueError):
            show_error_popup()

    def alternates(self):
        try:
            teams = []
            for team in self.teams_var.text.split(','):
                teams.append(team.upper())
            self.teams = teams
            if self.pos_var.text.upper() == 'G':
                nums = 2 - int(self.nums_var.text[2])
            elif self.pos_var.text.upper() == 'D':
                nums = 5 - int(self.nums_var.text[2])
            elif self.pos_var.text.upper() == 'M':
                nums = 5 - int(self.nums_var.text[2])
            elif self.pos_var.text.upper() == 'A':
                nums = 3 - int(self.nums_var.text[2])
            else:
                nums = int('a')
            data = alternativeFinder_2(self.teams, self.pos_var.text.upper(), int(self.gw_start.text),
                                       int(self.gw_end.text), int(self.nums_var.text[0]), int(self.nums_var.text[2]))
            show_popup_9(nums, data)
        except (ValueError, IndexError):
            show_error_popup()

    def helpbutton(self):
        show_popup_9_help()


class popup_9(FloatLayout):
    def __init__(self, nums, data, **kwargs):
        super().__init__(**kwargs)
        self.ids.col1.text = data[0]
        self.ids.col2.text = data[1]
        self.ids.col3.text = data[2]
        if nums > 2:
            self.ids.col4.text = data[3]
        else:
            self.ids.col4.text = ''
        if nums > 3:
            self.ids.col5.text = data[4]
        else:
            self.ids.col5.text = ''
        if nums > 4:
            self.ids.col6.text = data[5]
        else:
            self.ids.col6.text = ''


class popup_9_help(FloatLayout):
    pass


def show_popup_9(nums, data):
    show = popup_9(nums, data)
    popupWindow = Popup(title='Best Alternative Picks', content=show, size_hint=(0.6, 0.8))
    popupWindow.open()


def show_popup_9_help():
    show = popup_9_help()
    popupWindow = Popup(title='Help', content=show, size_hint=(0.8, 0.8))
    popupWindow.open()


class Settings1(Screen):
    setting1 = ObjectProperty(None)
    setting2 = ObjectProperty(None)
    setting3 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        data = CSV_reader('code_settings.csv')
        self.setting_1 = compilelistFn(data[0])
        self.setting_2 = compilelistFn(data[1])
        self.setting_3 = compilelistFn(data[2])

    def update_settings(self):
        data_keep = CSV_reader('code_settings.csv')
        with open('code_settings.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.setting1.text)
            writer.writerow(self.setting2.text.split(','))
            writer.writerow(self.setting3.text.split(','))
            writer.writerow(data_keep[3])
            writer.writerow(data_keep[4])
            writer.writerow(data_keep[5])
            writer.writerow(data_keep[6])

    def helpbutton(self):
        show_settings_help()


class UsablePlayers(Screen):
    data = CSV_reader('code_settings.csv')
    validG = data[3]
    validD = data[4]
    validM = data[5]
    validF = data[6]
    ARSG = BooleanProperty('ARS' in validG)
    AVLG = BooleanProperty('AVL' in validG)
    BHAG = BooleanProperty('BHA' in validG)
    BOUG = BooleanProperty('BOU' in validG)
    BURG = BooleanProperty('BUR' in validG)
    CHEG = BooleanProperty('CHE' in validG)
    CRYG = BooleanProperty('CRY' in validG)
    EVEG = BooleanProperty('EVE' in validG)
    LEIG = BooleanProperty('LEI' in validG)
    LIVG = BooleanProperty('LIV' in validG)
    MCIG = BooleanProperty('MCI' in validG)
    MUNG = BooleanProperty('MUN' in validG)
    NEWG = BooleanProperty('NEW' in validG)
    NORG = BooleanProperty('NOR' in validG)
    SHUG = BooleanProperty('SHU' in validG)
    SOUG = BooleanProperty('SOU' in validG)
    TOTG = BooleanProperty('TOT' in validG)
    WATG = BooleanProperty('WAT' in validG)
    WHUG = BooleanProperty('WHU' in validG)
    WOLG = BooleanProperty('WOL' in validG)
    ARSD = BooleanProperty('ARS' in validD)
    AVLD = BooleanProperty('AVL' in validD)
    BHAD = BooleanProperty('BHA' in validD)
    BOUD = BooleanProperty('BOU' in validD)
    BURD = BooleanProperty('BUR' in validD)
    CHED = BooleanProperty('CHE' in validD)
    CRYD = BooleanProperty('CRY' in validD)
    EVED = BooleanProperty('EVE' in validD)
    LEID = BooleanProperty('LEI' in validD)
    LIVD = BooleanProperty('LIV' in validD)
    MCID = BooleanProperty('MCI' in validD)
    MUND = BooleanProperty('MUN' in validD)
    NEWD = BooleanProperty('NEW' in validD)
    NORD = BooleanProperty('NOR' in validD)
    SHUD = BooleanProperty('SHU' in validD)
    SOUD = BooleanProperty('SOU' in validD)
    TOTD = BooleanProperty('TOT' in validD)
    WATD = BooleanProperty('WAT' in validD)
    WHUD = BooleanProperty('WHU' in validD)
    WOLD = BooleanProperty('WOL' in validD)
    ARSM = BooleanProperty('ARS' in validM)
    AVLM = BooleanProperty('AVL' in validM)
    BHAM = BooleanProperty('BHA' in validM)
    BOUM = BooleanProperty('BOU' in validM)
    BURM = BooleanProperty('BUR' in validM)
    CHEM = BooleanProperty('CHE' in validM)
    CRYM = BooleanProperty('CRY' in validM)
    EVEM = BooleanProperty('EVE' in validM)
    LEIM = BooleanProperty('LEI' in validM)
    LIVM = BooleanProperty('LIV' in validM)
    MCIM = BooleanProperty('MCI' in validM)
    MUNM = BooleanProperty('MUN' in validM)
    NEWM = BooleanProperty('NEW' in validM)
    NORM = BooleanProperty('NOR' in validM)
    SHUM = BooleanProperty('SHU' in validM)
    SOUM = BooleanProperty('SOU' in validM)
    TOTM = BooleanProperty('TOT' in validM)
    WATM = BooleanProperty('WAT' in validM)
    WHUM = BooleanProperty('WHU' in validM)
    WOLM = BooleanProperty('WOL' in validM)
    ARSF = BooleanProperty('ARS' in validF)
    AVLF = BooleanProperty('AVL' in validF)
    BHAF = BooleanProperty('BHA' in validF)
    BOUF = BooleanProperty('BOU' in validF)
    BURF = BooleanProperty('BUR' in validF)
    CHEF = BooleanProperty('CHE' in validF)
    CRYF = BooleanProperty('CRY' in validF)
    EVEF = BooleanProperty('EVE' in validF)
    LEIF = BooleanProperty('LEI' in validF)
    LIVF = BooleanProperty('LIV' in validF)
    MCIF = BooleanProperty('MCI' in validF)
    MUNF = BooleanProperty('MUN' in validF)
    NEWF = BooleanProperty('NEW' in validF)
    NORF = BooleanProperty('NOR' in validF)
    SHUF = BooleanProperty('SHU' in validF)
    SOUF = BooleanProperty('SOU' in validF)
    TOTF = BooleanProperty('TOT' in validF)
    WATF = BooleanProperty('WAT' in validF)
    WHUF = BooleanProperty('WHU' in validF)
    WOLF = BooleanProperty('WOL' in validF)

    def updateFile(self):
        data = CSV_reader('code_settings.csv')
        validG = []
        validD = []
        validM = []
        validF = []
        if self.ids.arsg.active:
            validG.append('ARS')
        if self.ids.avlg.active:
            validG.append('AVL')
        if self.ids.bhag.active:
            validG.append('BHA')
        if self.ids.boug.active:
            validG.append('BOU')
        if self.ids.burg.active:
            validG.append('BUR')
        if self.ids.cheg.active:
            validG.append('CHE')
        if self.ids.cryg.active:
            validG.append('CRY')
        if self.ids.eveg.active:
            validG.append('EVE')
        if self.ids.leig.active:
            validG.append('LEI')
        if self.ids.livg.active:
            validG.append('LIV')
        if self.ids.mcig.active:
            validG.append('MCI')
        if self.ids.mung.active:
            validG.append('MUN')
        if self.ids.newg.active:
            validG.append('NEW')
        if self.ids.norg.active:
            validG.append('NOR')
        if self.ids.shug.active:
            validG.append('SHU')
        if self.ids.soug.active:
            validG.append('SOU')
        if self.ids.totg.active:
            validG.append('TOT')
        if self.ids.watg.active:
            validG.append('WAT')
        if self.ids.whug.active:
            validG.append('WHU')
        if self.ids.wolg.active:
            validG.append('WOL')
        if self.ids.arsd.active:
            validD.append('ARS')
        if self.ids.avld.active:
            validD.append('AVL')
        if self.ids.bhad.active:
            validD.append('BHA')
        if self.ids.boud.active:
            validD.append('BOU')
        if self.ids.burd.active:
            validD.append('BUR')
        if self.ids.ched.active:
            validD.append('CHE')
        if self.ids.cryd.active:
            validD.append('CRY')
        if self.ids.eved.active:
            validD.append('EVE')
        if self.ids.leid.active:
            validD.append('LEI')
        if self.ids.livd.active:
            validD.append('LIV')
        if self.ids.mcid.active:
            validD.append('MCI')
        if self.ids.mund.active:
            validD.append('MUN')
        if self.ids.newd.active:
            validD.append('NEW')
        if self.ids.nord.active:
            validD.append('NOR')
        if self.ids.shud.active:
            validD.append('SHU')
        if self.ids.soud.active:
            validD.append('SOU')
        if self.ids.totd.active:
            validD.append('TOT')
        if self.ids.watd.active:
            validD.append('WAT')
        if self.ids.whud.active:
            validD.append('WHU')
        if self.ids.wold.active:
            validD.append('WOL')
        if self.ids.arsm.active:
            validM.append('ARS')
        if self.ids.avlm.active:
            validM.append('AVL')
        if self.ids.bham.active:
            validM.append('BHA')
        if self.ids.boum.active:
            validM.append('BOU')
        if self.ids.burm.active:
            validM.append('BUR')
        if self.ids.chem.active:
            validM.append('CHE')
        if self.ids.crym.active:
            validM.append('CRY')
        if self.ids.evem.active:
            validM.append('EVE')
        if self.ids.leim.active:
            validM.append('LEI')
        if self.ids.livm.active:
            validM.append('LIV')
        if self.ids.mcim.active:
            validM.append('MCI')
        if self.ids.munm.active:
            validM.append('MUN')
        if self.ids.newm.active:
            validM.append('NEW')
        if self.ids.norm.active:
            validM.append('NOR')
        if self.ids.shum.active:
            validM.append('SHU')
        if self.ids.soum.active:
            validM.append('SOU')
        if self.ids.totm.active:
            validM.append('TOT')
        if self.ids.watm.active:
            validM.append('WAT')
        if self.ids.whum.active:
            validM.append('WHU')
        if self.ids.wolm.active:
            validM.append('WOL')
        if self.ids.arsf.active:
            validF.append('ARS')
        if self.ids.avlf.active:
            validF.append('AVL')
        if self.ids.bhaf.active:
            validF.append('BHA')
        if self.ids.bouf.active:
            validF.append('BOU')
        if self.ids.burf.active:
            validF.append('BUR')
        if self.ids.chef.active:
            validF.append('CHE')
        if self.ids.cryf.active:
            validF.append('CRY')
        if self.ids.evef.active:
            validF.append('EVE')
        if self.ids.leif.active:
            validF.append('LEI')
        if self.ids.livf.active:
            validF.append('LIV')
        if self.ids.mcif.active:
            validF.append('MCI')
        if self.ids.munf.active:
            validF.append('MUN')
        if self.ids.newf.active:
            validF.append('NEW')
        if self.ids.norf.active:
            validF.append('NOR')
        if self.ids.shuf.active:
            validF.append('SHU')
        if self.ids.souf.active:
            validF.append('SOU')
        if self.ids.totf.active:
            validF.append('TOT')
        if self.ids.watf.active:
            validF.append('WAT')
        if self.ids.whuf.active:
            validF.append('WHU')
        if self.ids.wolf.active:
            validF.append('WOL')
        with open('code_settings.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data[0])
            writer.writerow(data[1])
            writer.writerow(data[2])
            writer.writerow(validG)
            writer.writerow(validD)
            writer.writerow(validM)
            writer.writerow(validF)


def show_settings_help():
    show = settings_help()
    popupWindow = Popup(title='Help', content=show, size_hint=(0.8, 0.8))
    popupWindow.open()


class settings_help(FloatLayout):
    pass


def compilelistFn(lis):
    x = ''
    for element in lis:
        x = x + element
        if not lis.index(element) == len(lis) - 1:
            x = x + ','
    return x


def show_error_popup():
    show = error_popup()
    popupWindow = Popup(title='ERROR', content=show, size_hint=(0.6, 0.2))
    popupWindow.open()


class error_popup(FloatLayout):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file('my.kv')


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    MyMainApp().run()
