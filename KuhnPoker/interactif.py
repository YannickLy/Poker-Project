from KuhnPoker.game.kuhnpoker import NoeudChance
from KuhnPoker.common import constantes as c
from KuhnPoker.algorithms.CRM import CRM, lightCRM
from KuhnPoker.algorithms.random_strategy import random_strategy
import numpy as np
from random import randrange

arbre = NoeudChance(c.COMBINAISONS_CARTES)

random_strategy = random_strategy(arbre)

lightCRM = lightCRM(arbre)
lightCRM.run(10000)
lightCRM.compute_equilibre_nash()

CRM = CRM(arbre)
CRM.run(10000)
CRM.compute_equilibre_nash()

def compare_strat(strat_IA, iterations = 1):
    victoires = {c.J1:{'nb':0, 'gain':0}, c.J2:{'nb':0, 'gain':0}}
    qui_commence = randrange(2)
    bot = c.J1 if qui_commence == 1 else c.J2
    joueur = c.J1 if qui_commence == 0 else c.J2
    
    for _ in range(iterations):
        pot_init = 0.5*2
        
        etat = arbre.sample_one()
        
        J = c.J1
        
        print('Vous avez tiré la carte {}.'.format(etat.cartes[qui_commence])) 
        
        while etat.enfants != {}:
            inf_set = etat.information_set()
            Equilibre_Nash = strat_IA[inf_set]
            [key1, key2] = Equilibre_Nash.keys()
            if J == bot:
                rand = np.random.uniform()
                if rand <= Equilibre_Nash[key1]:
                    strat = key1
                else:
                    strat = key2
                print("L'adversaire a {}.".format(strat))
            else:
                strat = input('Souhaitez-vous {0} ou {1} ? '.format(key1, key2)).upper()
            etat = etat.enfants[strat]
            J = -J
            
        if etat.historique_actions[-1] == 'CHECK' and etat.historique_actions[-2] == 'CHECK':
            winner = c.GAGNANT[etat.cartes]
            pot = pot_init
            print('Carte du bot : {}'.format(etat.cartes[1-qui_commence]))
            print('Carte du joueur : {}'.format(etat.carttes[qui_commence]))
            if winner == bot: 
                print("Gagnant : Bot")
            else:
                print("Gagnant : Joueur")
            print('Pot : {}'.format(pot))
#                print("L'adversaire a gagné ({0}) car il avait la carte {1}.".format(pot, etat.cartes[-qui_commence]))
#            else:
#                print("Vous avez gagné ({0}) car l'adversaire avait la carte {1}.".format(pot, etat.cartes[-qui_commence])))
        elif etat.historique_actions[-1] == 'CALL' and etat.historique_actions[-2] == 'BET':
            winner = c.GAGNANT[etat.cartes]
            pot = pot_init * 2
            print('Carte du bot : {}'.format(etat.cartes[1-qui_commence]))
            print('Carte du joueur : {}'.format(etat.cartes[qui_commence]))
            
            if winner == bot: 
                print("Gagnant : Bot")
            else:
                print("Gagnant : Joueur")
            print('Pot : {}'.format(pot))
#                print("L'adversaire a gagné ({0}) car il avait la carte {1}.".format(pot, etat.cartes[-qui_commence]))
#            else:
#                print("Vous avez gagné ({0}) car l'adversaire avait la carte {1}.".format(pot, etat.cartes[-qui_commence])))           
            
        elif etat.historique_actions[-1] == 'FOLD':
            pot = pot_init * 1.5
            
            if len(etat.historique_actions) == 2:
                winner = c.J1
            else:
                winner = c.J2
            
            if winner == bot:
                print("S'est couché : Joueur")
                print("Gagnant : Bot")
            else: 
                print("S'est couché : Bot")
                print("Gagnant : Joueur")
               
            print('Pot : {}'.format(pot))

#                print("L'adversaire a gagné ({}) car vous vous êtes couché.".format(pot))
#            else:
#                print("Vous avez gagné ({}) car l'adversaire s'est couché.".format(pot))

        victoires[winner]['nb'] += 1
        victoires[winner]['gain'] += pot
    return victoires

histo = compare_strat(lightCRM.information_set_equilibre_nash)