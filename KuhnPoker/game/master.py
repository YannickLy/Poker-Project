from kuhn.kuhnpoker import NoeudChance
from common import constants as c
from strategies.strategy import Strategy
import random

def start_game(strat_IA):

    qui_commence = random.randrange(2)
    bot = c.J1 if qui_commence == 1 else c.J2
    joueur = c.J1 if qui_commence == 0 else c.J2
    
    etat = arbre.sample_one()
    J = c.J1
    
    print('La blinde initiale est de 1€ par joueur.')
    print('Vous avez tiré la carte {}.'.format(etat.cartes[qui_commence])) 
    while etat.enfants != {}:
        inf_set = etat.information_set()
        qui_joue = strat_IA[inf_set]
        [key1, key2] = qui_joue.keys()
        if J == bot:
            rand = random.uniform(0, 1)
            if rand <= qui_joue[key1]:
                strat = key1
            else:
                strat = key2
            print("Le bot a {}.".format(strat))
        else:
            strat = input('Souhaitez-vous {0} ou {1} ? '.format(key1, key2)).upper()
        etat = etat.enfants[strat]
        J = -J
    
    if etat.historique_actions[-1] == 'CHECK' and etat.historique_actions[-2] == 'CHECK':
        winner = c.GAGNANT[etat.cartes]
        pot = 2
        print('Carte du bot : {}'.format(etat.cartes[1-qui_commence]))
        print('Votre carte : {}'.format(etat.cartes[qui_commence]))
        if winner == bot: 
            print("Le bot a gagné.")
        else:
            print("Vous avez gagné !")
        print('Pot : {}€'.format(pot))
    elif etat.historique_actions[-1] == 'CALL' and etat.historique_actions[-2] == 'BET':
        winner = c.GAGNANT[etat.cartes]
        pot = 4
        print('Carte du bot : {}'.format(etat.cartes[1-qui_commence]))
        print('Votre carte : {}'.format(etat.cartes[qui_commence]))
        if winner == bot: 
            print("Le bot a gagné.")
        else:
            print("Vous avez gagné !")
        print('Pot : {}€'.format(pot))        
    elif etat.historique_actions[-1] == 'FOLD':
        pot = 3
        if len(etat.historique_actions) == 2:
            winner = c.J1
        else:
            winner = c.J2
        if winner == bot:
            print("Vous vous êtes couché.")
            print("Le bot a gagné.")
        else: 
            print("Le bot s'est couché.")
            print("Vous avez gagné !")            
        print('Pot : {}€'.format(pot))

arbre = NoeudChance(c.COMBINAISONS_CARTES)
s = Strategy(arbre)

Random = s.Random()
CRM = s.CRM(10000)
lightCRM = s.lightCRM(10000)

start_game(CRM)