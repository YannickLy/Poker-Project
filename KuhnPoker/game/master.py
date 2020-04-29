from kuhn.kuhnpoker import NoeudChance
from common import constants as c
from strategies.strategy import lightCRM_model, CRM_model, opt_espgain_model, random_model
import random

def start_game():

    arbre = NoeudChance(c.COMBINAISONS_CARTES)
    lightCRM = lightCRM_model(arbre)
    CRM = CRM_model(arbre)
    Random = random_model(arbre)
    opt_esp = opt_espgain_model(arbre)

    print('**************************************************')
    print('Les IA disponibles sont : ')
    print(' 1/ lightCRM')
    print(' 2/ CRM')
    print(' 3/ Optimal Esperance Gain')
    print(' 4/ random')
    choix = input('Contre quelle IA souahaitez-vous jouer ? ')
    print('**************************************************')
    if choix == '1':
        strat_IA = lightCRM.run(10000)
        print("Vous avez fait le choix de jouer contre l'IA lightCRM.")
    elif choix == '2':
        strat_IA = CRM.run(10000)
        print("Vous avez fait le choix de jouer contre l'IA CRM.")
    elif choix == '3':
        strat_IA = opt_esp.run()
        print("Vous avez fait le choix de jouer contre l'IA Optimal Esperance Gain.")
    elif choix == '4':
        strat_IA = Random.run()
        print("Vous avez fait le choix de jouer contre l'IA random.")
    
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

start_game()