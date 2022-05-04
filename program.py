from classes import *
from print_handling import *
from writeGameDataToFile import writeGameDataToCSV

def program(discard_rate, player_num=3, allow_print=True):

    if allow_print:
        enablePrint()
    else:
        blockPrint()


        print('------- Welcome to Hanabi -------')
    pl_num = player_num
    game = Game(pl_num)

    while len(game.deck.cards) != 0 and game.is_finished() != 1: # != 0 must accept each player adding one more card later
        game.player_action(discard_rate, True)


    action_list = game.finish_game()

    print('Final board')
    score = game.print_score()
    print('The final score is: ', game.calc_score())


    # save game data
    # writeGameDataToCSV(action_list)

    return score