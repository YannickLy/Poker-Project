import seaborn as sns
from matplotlib import pyplot as plt
import random
import pandas as pd
import numpy as np

from scipy import stats
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import scipy.spatial.distance as ssd

from common import constantes as c
from texasholdem.gagnant import gagnant
from texasholdem.main import main
from common.timer import timer

# Test de la fonction pour déterminer le gagnant
J1 =  ['4S', '4C']
J2 = ['3D', '9H']
riviere = ['5S', '6S', 'TS', 'AS', 'JS']

jeu = gagnant(J1, J2, riviere)
jeu.get_winner()
print(jeu.winner)

# Histogramme : test pour les paires (4S, 4C) et (JS, TS)
NB_SIMUL_RIVIERE = 500
NB_SIMUL_J2 = 500
def compute_hist(combinaison):
    
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
    return probWinJ1

t = timer()
t.start()

combinaisons = [['4S', '4C'], ['JS', 'TS']]
df = pd.DataFrame()
for comb in combinaisons:
    df[str(comb)] = compute_hist(comb)
    
t.stop()
print(t.total_run_time())

f, axes = plt.subplots(1, 2)
sns.distplot(axlabel = "Force de la main", a = df.iloc[:,0], bins = 20, kde = False, ax = axes[0]).set_title('Distribution : 4S4C')
sns.distplot(axlabel = "Force de la main", a = df.iloc[:,1], bins = 20, kde = False, ax = axes[1]).set_title('Distribution : JSTS')
f.savefig('clustering/hist_4S4C_JSTS.png')

