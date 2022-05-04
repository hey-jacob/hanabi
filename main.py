from program import *
import time
from print_handling import *
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


def main(discard_rate, allow_print):

    max_iterations = 5 # ca 200 i sekundet, 1000 per 5 sekunder, ca 10 000 i minuttet, 600 000 i timen
    iteration = 0
    score = 0
    score_list = []
    time_x = time.time()
    best_score = 0
    while iteration < max_iterations:
        result = program(discard_rate, player_num = 5, allow_print=False)
        score += result
        score_list.append(result)
        iteration += 1
        enablePrint()
        if result > best_score:
            best_score  = result
        if iteration%1000 == 0:
            print('On iteration ', iteration, 'with time elapsed:', round(time.time()-time1,2), 'seconds', 'and previous interval on', round(time.time()-time_x,2), 'seconds', 'and moving average on ', round(iteration/round(time.time()-time1, 2),2), 'iterations/ second')
            time_x = time.time()

    return score, best_score, score/max_iterations, score_list, max_iterations

if __name__ == '__main__':
    time1 = time.time()
    dr = 0.08
    score, best_score, score_avg, score_list, max_it = main(discard_rate=dr, allow_print=True)

    counter = Counter(score_list)
    enablePrint()


    for key in range(0, 26):
        print(key, ":", counter[key], end='\n')

    for key in range(0, 26):
        print(key, ":", round((counter[key]/max_it)*100,2), "% ", end="\n")

    time2 = time.time()

    print(round(max_it/(time2-time1),2), 'games/seconds')
    print('Total time elapsed: ', round(time2-time1,2), 'seconds')

    print('best score:', best_score)
    print('avg_score: ', round(score_avg,2))