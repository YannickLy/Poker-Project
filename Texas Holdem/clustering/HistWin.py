import Constantes as c
import random
import numpy as np

from Poker import poker

class histwin:
    
    def __init__(self, J1):
        self.J1 = J1
        
    def at_preflop(self):
        cartes_tmp = [x for x in c.CARTES if x not in self.J1]
        ProbWinJ1 = []
        
        i = 0
        while i < c.NB_SIMUL_RIVIERE:
            count_wins_J1 = 0
            riviere = random.sample(cartes_tmp, k = 5)
            cartes_tmp_bis = [x for x in cartes_tmp if x not in riviere]
            
            j = 0
            while j < c.NB_SIMUL_J2:
                J2 = random.sample(cartes_tmp_bis, k = 2)
                p = poker(self.J1, J2, riviere)
                p.get_winner()
                if p.winner == 'joueur 1': count_wins_J1 += 1
                j += 1
            
            ProbWinJ1.append(count_wins_J1 / c.NB_SIMUL_J2)
            i += 1
        
        HistWin = np.histogram(ProbWinJ1, bins = 10)
        
        return (HistWin[0] / c.NB_SIMUL_RIVIERE)
    
    
    def at_flop(self):
        
        return
    
    def at_turn(self):
        
        return
    
    def at_river(self):
        
        return
        
        
        