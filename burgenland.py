from math import ceil
import csv
import re

lookup_files = {
    'dealer_ron': './tables/dealer_ron.csv',
    'dealer_tsumo': './tables/dealer_tsumo.csv',
    'non_dealer_ron': './tables/non_dealer_ron.csv',
    'non_dealer_tsumo': './tables/non_dealer_tsumo.csv'
}


def selection(question, options):
    options_string = ', '.join(options)
    while True:
        answer = input(f'{question} ({options_string}) ').lower()
        if answer not in options:
            print(f'Möglichkeiten: {options_string}')
        else:
            return answer


def setup() -> dict:
    players_string = input('Spieler in Spielreihenfolge: ')
    players = re.split(r'[ ]+', players_string)

    points = dict()
    for player in players:
        points[player] = 25000
    return players, points


def rotate_players(players):
    new_players = []
    new_players.append(players[len(players) - 1])
    for i in range(len(players) - 1):
        new_players.append(players[i])
    return new_players


def lookup_value(fu, han, is_ron, is_dealer):
    if is_dealer:
        file_name = 'dealer'
    else:
        file_name = 'non_dealer'
    if is_ron:
        file_name += '_ron.csv'
    else:
        file_name += '_tsumo.csv'
    with open(f'./tables/{file_name}', 'r') as f:
        reader = csv.DictReader(f, delimiter=';')
        han_count = 1
        for row in reader:
            if han_count == han:
                value = row[str(fu)]
                if ',' in value:
                    return tuple(map(int, value.split(',')))
                else:
                    return int(value)
            han_count += 1


def main():
    # game setup
    players, points = setup()
    og_player1 = players[0]
    full_rotations = 0

    while True:
        print(players)
        winner = selection('Wer hat gewonnen?', players)
        type_of_win = selection('Art von Gewinn?', ['ron', 'tsumo'])

        loser_list = set(players) - {winner}

        if type_of_win == 'ron':
            loser = selection('Von wem wurde gewonnen?', loser_list)

        han = int(input('Han? '))
        if han < 5:
            fu = int(input('Fu? '))
        else:
            fu = -1  # TODO

        is_ron = type_of_win == 'ron'
        is_dealer = winner == players[0]
        value = lookup_value(fu, han, is_ron, is_dealer)

        if type_of_win == 'ron':
            points[winner] += value
            points[loser] -= value
        elif type_of_win == 'tsumo':
            if winner == players[0]:
                points[winner] += value * 3
                for loser in loser_list:
                    points[loser] -= value
            else:
                value1, value2 = value
                points[winner] += value1 * 2 + value2
                for loser in loser_list:
                    if loser == players[0]:
                        points[loser] -= value2
                    else:
                        points[loser] -= value1

        print(points)

        for player in players:
            if points[player] < 0:
                print(f"Spieler {player} hat unter Null Punkte.")
                break

        if winner != players[0]:
            players = rotate_players(players)
            if players[0] == og_player1:
                full_rotations += 1
                if full_rotations == 2:
                    print("Fertig")
                    break


if __name__ == '__main__':
    main()
