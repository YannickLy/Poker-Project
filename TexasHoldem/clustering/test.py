from common import constantes as c
from texasholdem.gagnant import gagnant

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
            p = gagnant(combinaison, J2, riviere)
            p.get_winner()
            if p.winner == 1: count_wins_J1 += 1
            j += 1
        probWinJ1.append(count_wins_J1 / c.NB_SIMUL_J2)
        i += 1
        
    HistWin = np.histogram(probWinJ1, bins = 10)
    L.append([combinaison, HistWin[0] / c.NB_SIMUL_RIVIERE])

if __name__ == "__main__": 
    
   test_combinaisons_J1 = [['4S', '4C'], ['JS', 'TS'], ['2D', '3H']]
   L = multiprocessing.Manager().list()
   pool = multiprocessing.Pool(multiprocessing.cpu_count() - 1)
   [pool.apply_async(func, args = [n, L]) for n in test_combinaisons_J1]
   pool.close()
   pool.join()
   print(L)
   
