import seaborn as sns
import random
import pandas as pd
import numpy as np

# clustering
from scipy import stats
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from matplotlib import pyplot as plt
import scipy.spatial.distance as ssd

from TexasHoldem.common import constantes as c
from TexasHoldem.common.gagnant import gagnant
from TexasHoldem.common.main import main
from TexasHoldem.common import timer

# Test de la fonction principale
J1 =  ['4S', '4C']
J2 = ['3D', '9H']
riviere = ['5S', '6S', 'TS', 'AS', 'JS']

jeu = gagnant(J1, J2, riviere)
jeu.get_winner()
print(jeu.winner)

## Histogramme : test pour la paire (4S, 4C)
J1 = ['4S', '4C']

t = timer()
t.start()

cartes_tmp = [x for x in c.CARTES if x not in J1]
ProbWinJ1 = []

i = 0
while i < c.NB_SIMUL_RIVIERE:
    
    count_wins_J1 = 0
    riviere = random.sample(cartes_tmp, k = 5)
    cartes_tmp_bis = [x for x in cartes_tmp if x not in riviere]
    
    j = 0
    while j < c.NB_SIMUL_J2:
        
        J2 = random.sample(cartes_tmp_bis, k = 2)
        p = poker(J1, J2, riviere)
        p.get_winner()
        if p.winner == 'joueur 1': count_wins_J1 += 1
        j += 1
    
    ProbWinJ1.append(count_wins_J1 / c.NB_SIMUL_J2)
    i += 1

t.stop()
T1 = t.total_run_time()
sns.distplot(ProbWinJ1, bins = 10, kde = False)

# ######### DICO PRE-FLOP #########
all_combinaisons_J1 = []
for i in range(0, 13):
    for j in range(i, 13):
        if i != j:
            all_combinaisons_J1.append([c.VALEURS[i] + 'H', c.VALEURS[j] + 'H'])
        all_combinaisons_J1.append([c.VALEURS[i]  + 'H', c.VALEURS[j]  + 'D'])

test_combinaisons_J1 = [['4S', '4C'], ['JS', 'TS'], ['2D', '3H']]
combinaisons_hist = pd.DataFrame()

t = timer()
t.start()

for k in test_combinaisons_J1:
    
    h = histwin(k)
    combinaisons_hist[str(k)] = h.at_preflop()
    
t.stop()
T2 = t.total_run_time()

n = len(test_combinaisons_J1)
M = np.zeros((n,n))
bin_locations = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for i in range(n):
    for j in range(i+1, n):
        M[i,j] = stats.wasserstein_distance(bin_locations, bin_locations, combinaisons_hist.iloc[:,i], combinaisons_hist.iloc[:,j])
        M[j,i] = M[i,j]

distArray = ssd.squareform(M)  
Z = linkage(distArray, 'ward')
 
plt.figure(figsize=(25, 10))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
dendrogram(
    Z,
    leaf_rotation=90.,
    leaf_font_size=8., 
)
plt.show()
 
max_d = 3
res=clusters = fcluster(Z, max_d, criterion='distance')
print(res)




