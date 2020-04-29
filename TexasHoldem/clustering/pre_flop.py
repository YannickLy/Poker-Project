from common import constantes as c
from texasholdem.gagnant import gagnant
from common.timer import timer

import multiprocessing
import random
import numpy as np
import pandas as pd
from scipy import stats
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from matplotlib import pyplot as plt
import scipy.spatial.distance as ssd

NB_SIMUL_RIVIERE = 500
NB_SIMUL_J2 = 500

def compute_cluster_preflop(combinaison, L):
    
    cartes_tmp = [x for x in c.CARTES if x not in combinaison]
    probWinJ1 = []
    i = 0
    while i < NB_SIMUL_RIVIERE:
        count_wins_J1 = 0
        riviere = random.sample(cartes_tmp, k = 5)
        cartes_tmp_bis = [x for x in cartes_tmp if x not in riviere]
        j = 0
        while j < NB_SIMUL_J2:
            J2 = random.sample(cartes_tmp_bis, k = 2)
            p = gagnant(combinaison, J2, riviere)
            p.get_winner()
            if p.winner == 1: count_wins_J1 += 1
            j += 1
        probWinJ1.append(count_wins_J1 / NB_SIMUL_J2)
        i += 1
    HistWin = np.histogram(probWinJ1, bins = 10)
    L.append([combinaison, HistWin[0] / NB_SIMUL_RIVIERE])

if __name__ == "__main__": 
    
    t = timer()
    t.start()

    all_combinaisons_preflop = []
    for i in range(0, 13):
        for j in range(i, 13):
            if i != j:
                all_combinaisons_preflop.append([c.VALEURS[i] + 'H', c.VALEURS[j] + 'H'])
            all_combinaisons_preflop.append([c.VALEURS[i]  + 'H', c.VALEURS[j]  + 'D'])
    
    L = multiprocessing.Manager().list()
    pool = multiprocessing.Pool(multiprocessing.cpu_count() - 1)
    [pool.apply_async(compute_cluster_preflop, args = [n, L]) for n in all_combinaisons_preflop]
    pool.close()
    pool.join()

    df = pd.DataFrame()
    for e in L:
        df[str(e[0])] = e[1]

    n = len(all_combinaisons_preflop)
    M = np.zeros((n,n))
    bin_locations = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for i in range(n):
        for j in range(i+1, n):
            M[i,j] = stats.wasserstein_distance(bin_locations, bin_locations, df.iloc[:,i], df.iloc[:,j])
            M[j,i] = M[i,j]
    
    distArray = ssd.squareform(M)  
    Z = linkage(distArray, 'ward')
    
    plt.figure(figsize=(50, 50))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('sample index')
    plt.ylabel('distance')
    dendrogram(
        Z,
        leaf_rotation=90.,
        leaf_font_size=8.)
    plt.savefig('test.png')
    
    clusters = fcluster(Z, 1.8, criterion = 'distance') # avec une distance maximale de 1.8, nous réduisons le nombre de cluster à 8.
    print(clusters)
    t.stop()
    print(t.total_run_time())
   