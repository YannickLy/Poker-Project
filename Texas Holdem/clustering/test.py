import Constantes as c
from Poker import poker

import multiprocessing
import random
import numpy as np

def func(combinaison, L):
    
    cartes_tmp = [x for x in c.CARTES if x not in combinaison]
    probWinJ1 = []
        
    i = 0
    while i < c.NB_SIMUL_RIVIERE:
        count_wins_J1 = 0
        riviere = random.sample(cartes_tmp, k = 5)
        cartes_tmp_bis = [x for x in cartes_tmp if x not in riviere]
        
        j = 0
        while j < c.NB_SIMUL_J2:
            J2 = random.sample(cartes_tmp_bis, k = 2)
            p = poker(combinaison, J2, riviere)
            p.get_winner()
            if p.winner == 'joueur 1': count_wins_J1 += 1
            j += 1
        probWinJ1.append(count_wins_J1 / c.NB_SIMUL_J2)
        i += 1
        
    HistWin = np.histogram(probWinJ1, bins = 10)
    L.append(HistWin[0] / c.NB_SIMUL_RIVIERE)

#a = func(test_combinaisons_J1)

if __name__ == "__main__": 
    
#    test_combinaisons_J1 = [['4S', '4C'], ['JS', 'TS'], ['2D', '3H']]
#    L = multiprocessing.Manager().list()
#    pool = multiprocessing.Pool(6)
#    [pool.apply_async(func, args = [n, L]) for n in test_combinaisons_J1]
#    pool.close()
#    pool.join()
#    print(L)
#    
    test_combinaisons_J1 = [['4S', '4C'], ['JS', 'TS'], ['2D', '3H']]
    L = multiprocessing.Manager().list()
    for i in range(3):
        p = multiprocessing.Process(target = func, args=([['4S', '4C']], L))
        p.start()
        p.join()
    print(L)

   
#import multiprocessing
#manager = multiprocessing.Manager()
#shared_list = manager.list()
#
#def worker1(l):
#    l.append(1)
#
#def worker2(l):
#    l.append(2)
#
#process1 = multiprocessing.Process(
#    target=worker1, args=(shared_list))
#process2 = multiprocessing.Process(
#    target=worker2, args=(shared_list))
#
#process1.start()
#process2.start()
#process1.join()
#process2.join()
#
#print(shared_list)