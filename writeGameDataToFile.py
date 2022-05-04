import csv

from locpath import PATH_NAME

def writeGameDataToCSV(game_data):
    csv_file = PATH_NAME
    csv_columns = game_data[0].keys()

    print('game data: ', type(game_data[0]))

    with open(csv_file, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for row in game_data:
            writer.writerow(row)


