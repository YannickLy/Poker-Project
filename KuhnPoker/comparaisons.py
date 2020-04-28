from KuhnPoker.game.kuhnpoker import NoeudChance
from KuhnPoker.common import constantes as c
from KuhnPoker.algorithms.CRM import CRM, lightCRM
from KuhnPoker.algorithms.random_strategy import random_strategy
import numpy as np

arbre = NoeudChance(c.COMBINAISONS_CARTES)

random_strategy = random_strategy(arbre)

lightCRM = lightCRM(arbre)
lightCRM.run(10000)
lightCRM.compute_equilibre_nash()

CRM = CRM(arbre)
CRM.run(10000)
CRM.compute_equilibre_nash()

def compare_strat(strat_joueur1, strat_joueur2, iterations=10000):
    victoires = {c.J1:{'nb':0, 'gain':0}, c.J2:{'nb':0, 'gain':0}}
    
    for _ in range(iterations):
        pot_init = 0.5*2
        
        etat = arbre.sample_one()
        
        J = c.J1
        
        while etat.enfants != {}:
            inf_set = etat.information_set()
            Equilibre_Nash = strat_joueur1[inf_set] if J == c.J1 else strat_joueur2[inf_set]
            
            rand = np.random.uniform()
            
            [key1, key2] = Equilibre_Nash.keys()
            if rand <= Equilibre_Nash[key1]:
                strat = key1
            else:
                strat = key2
            etat = etat.enfants[strat]
            J = -J
        
        if etat.historique_actions[-1] == 'CHECK' and etat.historique_actions[-2] == 'CHECK':
            winner = c.GAGNANT[etat.cartes]
            pot = pot_init
        elif etat.historique_actions[-1] == 'CALL' and etat.historique_actions[-2] == 'BET':
            winner = c.GAGNANT[etat.cartes]
            pot = pot_init * 2
        elif etat.historique_actions[-1] == 'FOLD':
            pot = pot_init * 1.5
            winner = c.J1 if len(etat.historique_actions) == 2 else c.J2
    
        victoires[winner]['nb'] += 1
        victoires[winner]['gain'] += pot
        
    return victoires

compare_light_CRM = compare_strat(lightCRM.information_set_equilibre_nash, CRM.information_set_equilibre_nash)
compare_CRM_light = compare_strat(CRM.information_set_equilibre_nash, lightCRM.information_set_equilibre_nash)
compare_light_random = compare_strat(lightCRM.information_set_equilibre_nash, random_strategy)
compare_random_light = compare_strat(random_strategy, lightCRM.information_set_equilibre_nash)
compare_CRM_random = compare_strat(CRM.information_set_equilibre_nash, random_strategy)
compare_random_CRM = compare_strat(random_strategy, CRM.information_set_equilibre_nash)
