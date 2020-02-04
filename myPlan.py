import csv
from tabulate import tabulate
from CSV_reader import CSV_reader
from colorama import init, Fore

init(autoreset=True)


class FPL_Plan:
    """
    A class to represent my plans
    """

    def __init__(self):
        """
        Sets initial list format of gameweeks
        """
        self.gameweeks = []

    def createGW(self, gameweek):
        """
        Used to create a gameweek
        :param gameweek: type: gameweek, created by class GW()
        """
        self.gameweeks.append(gameweek)

    def addTransfer(self, GW, player, direction):
        """
        Adds to the trans_in/out field of the variable gameweek
        :param GW: gameweek identifier to identify which trans_in/out to edit
        :param player: type: string, which player is being transferred
        :param direction: either 'in' or 'out'. direction of transfer
        """
        for gameweek in self.gameweeks:
            if gameweek.number == GW:
                if direction == 'in' and gameweek.trans_in != '':
                    gameweek.trans_in = gameweek.trans_in + '&' + player
                    print(player + ' added successfully')
                elif direction == 'in' and gameweek.trans_in == '':
                    gameweek.trans_in = player
                    print(player + ' added successfully')
                elif direction == 'out' and gameweek.trans_out != '':
                    gameweek.trans_out = gameweek.trans_out + '&' + player
                    print(player + ' added successfully')
                elif direction == 'out' and gameweek.trans_out == '':
                    gameweek.trans_out = player
                    print(player + ' added successfully')
                else:
                    print('error in FPL_Plan.addTransfer()')

    def removeTransfer(self, GW, player, direction):
        """
        Removes from the trans_in/out field of the variable gameweek
        :param GW: gameweek identifier to identify which trans_in/out to edit
        :param player: type: string, which player is being transferred
        :param direction: either 'in' or 'out'. direction of transfer
        """
        for gameweek in self.gameweeks:
            if gameweek.number == GW:
                if direction == 'in':
                    if '&' + player in gameweek.trans_in and player != '':
                        gameweek.trans_in = gameweek.trans_in.replace('&' + player, '')
                        print(player + ' removed successfully')
                    elif player + '&' in gameweek.trans_in and player != '':
                        gameweek.trans_in = gameweek.trans_in.replace(player + '&', '')
                        print(player + ' removed successfully')
                    else:
                        gameweek.trans_in = gameweek.trans_in.replace(player, '')
                        print(player + ' removed successfully')
                elif direction == 'out':
                    if '&' + player in gameweek.trans_out and player != '':
                        gameweek.trans_out = gameweek.trans_out.replace('&' + player, '')
                        print(player + ' removed successfully')
                    elif player + '&' in gameweek.trans_out and player != '':
                        gameweek.trans_out = gameweek.trans_out.replace(player + '&', '')
                        print(player + ' removed successfully')
                    else:
                        gameweek.trans_out = gameweek.trans_out.replace(player, '')
                        print(player + ' removed successfully')
                else:
                    print('error in FPL_Plan.removeTransfer()')

    def getGameweek(self, number):
        """
        Retrieve a saved gameweek
        :param number: gameweek identifier to identify which gameweek to retrieve
        :return: gameweek if it is saved. otherwise, returns None
        """
        for gameweek in self.gameweeks:
            if gameweek.number == number:
                return gameweek
        return None

    def removeGW(self, number):
        new_Gameweeks = []
        for gameweek in self.gameweeks:
            if not gameweek.number == number:
                new_Gameweeks.append(gameweek)
        self.gameweeks = new_Gameweeks


class GW:
    """
    A class to represent a gameweek in the FPL Plan
    """
    def __init__(self, number, moves_in, moves_out):
        """
        Runs at initialisation of class object
        :param number: a gameweek identifier (1-38)
        :param moves_in: TODO
        :param moves_out: TODO
        """
        self.number = number
        self.trans_in = moves_in
        self.trans_out = moves_out


def editPlan():
    plan = FPL_Plan()
    data = CSV_reader('plan.csv')
    for row in data:
        gameweek = GW(int(row[0]), row[1], row[2])
        plan.createGW(gameweek)

    choice = ''

    print(Fore.LIGHTCYAN_EX + 'FPL_Plan Menu\n1. Add transfer\n2. Remove transfer\n3. View plan\n0. Exit FPL_Plan')

    while choice != 0:

        choice = int(input('Enter FPL_Plan choice: '))
        if choice == 1:
            GW_no = int(input('In which gameweek would you like to make this transfer? '))
            player_in = input('Which player would you like to transfer in? ')
            player_out = input('Which player would you like to transfer out? ')
            gameweek = GW(GW_no, player_in, player_out)
            found = False
            for stuff in plan.gameweeks:
                if stuff.number == GW_no:
                    if player_in != '':
                        plan.addTransfer(GW_no, player_in, 'in')
                    if player_out != '':
                        plan.addTransfer(GW_no, player_out, 'out')
                    found = True
            if not found:
                plan.createGW(gameweek)
            # gameweek = plan.getGameweek(GW_no)
            # row = [gameweek.number, gameweek.trans_in, gameweek.trans_out]
            with open('plan.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                rows = []
                for gameweek in plan.gameweeks:
                    rows.append([gameweek.number, gameweek.trans_in, gameweek.trans_out])
                for i in range(1, 39):
                    for j in range(len(rows)):
                        if rows[j][0] == i or rows[j][0] == str(i):
                            writer.writerow(rows[j])

        elif choice == 2:
            GW_no = int(input('In which gameweek does this transfer occur? '))
            player_in = input('Which transfer in would you like to cancel? ')
            player_out = input('Which transfer out would you like to cancel? ')
            for gameweek in plan.gameweeks:
                if gameweek.number == GW_no:
                    plan.removeTransfer(GW_no, player_in, 'in')
                    plan.removeTransfer(GW_no, player_out, 'out')
            with open('plan.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                rows = []
                for gameweek in plan.gameweeks:
                    rows.append([gameweek.number, gameweek.trans_in, gameweek.trans_out])
                for i in range(1, 39):
                    for j in range(len(rows)):
                        if rows[j][0] == i or rows[j][0] == str(i):
                            writer.writerow(rows[j])

        elif choice == 3:
            big_array = []
            for gameweek in plan.gameweeks:
                row = [gameweek.number, gameweek.trans_in.replace('&', ',\n'), gameweek.trans_out.replace('&', ',\n')]
                big_array.append(row)
            print(tabulate(sorted(big_array), ['GW', 'In', 'Out', 'Comments'], tablefmt='orgtbl'))


def editPlan_2(choice, **kwargs):
    GW_no = kwargs.get('GW_no', None)
    player_in = kwargs.get('player_in', None)
    player_out = kwargs.get('player_out', None)
    plan = FPL_Plan()
    data = CSV_reader('plan.csv')
    for row in data:
        gameweek = GW(int(row[0]), row[1], row[2])
        plan.createGW(gameweek)
    if choice == 1:
        gameweek = GW(GW_no, player_in, player_out)
        found = False
        for stuff in plan.gameweeks:
            if stuff.number == GW_no:
                if player_in != '':
                    plan.addTransfer(GW_no, player_in, 'in')
                if player_out != '':
                    plan.addTransfer(GW_no, player_out, 'out')
                found = True
        if not found:
            plan.createGW(gameweek)
        # gameweek = plan.getGameweek(GW_no)
        # row = [gameweek.number, gameweek.trans_in, gameweek.trans_out]
    elif choice == 2:
        for gameweek in plan.gameweeks:
            if gameweek.number == GW_no:
                plan.removeTransfer(GW_no, player_in, 'in')
                plan.removeTransfer(GW_no, player_out, 'out')
    elif choice == 3:
        plan.removeGW(GW_no)
    with open('plan.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        rows = []
        for gameweek in plan.gameweeks:
            rows.append([gameweek.number, gameweek.trans_in, gameweek.trans_out])
        for i in range(1, 39):
            for j in range(len(rows)):
                if rows[j][0] == i or rows[j][0] == str(i):
                    writer.writerow(rows[j])
