from common.timer import timer
import pickle

t = timer()
t.start()
with open('clustering/dico_preflop.pickle', 'rb') as handle:
    preflop = pickle.load(handle)
t.stop()

print(t.total_run_time())
print(preflop)

##################

from common import constantes as c
import pandas as pd
import numpy as np
import pprint

cartes =[]
cartes[:0] = c.VALEURS
matrice = np.zeros([len(cartes), len(cartes)])

for key in preflop.keys():
    val1 = key[2]
    col1 = key[3]
    val2 = key[8]
    col2 = key[9]

    if col1 == col2:
        matrice[c.VALEURS.find(val1)][c.VALEURS.find(val2)] = preflop[key]  #suited
    else:
        matrice[c.VALEURS.find(val2)][c.VALEURS.find(val1)] = preflop[key]  #unsuited
     
df = pd.DataFrame(matrice, columns = cartes)
df['cartes'] = cartes
df.set_index(['cartes'], inplace=True)