# Création d'une IA pour le Poker - Projet informatique ENSAE 2020

## Pour pouvoir jouer contre une des IA implémentées pour le Kuhn Poker, la manipulation est la suivante :

1. Placez vous au niveau du dossier "KuhnPoker"
2. Lancez les commandes suivantes :

from game.master import start_game

start_game()

## Si vous souhaitez connaître les arbres de probabilités pour les différentes IA implémentées pour le Kuhn Poker, la manipulation est la suivante :

1. Placez vous au niveau du dossier "KuhnPoker"
2. Lancez les commandes suivantes : 

from kuhn.kuhnpoker import NoeudChance  
from strategies.strategy import lightCRM_model, CRM_model, opt_espgain_model, random_model  
from common import constants as c  

arbre = NoeudChance(c.COMBINAISONS_CARTES)  
lightCRM = lightCRM_model(arbre)  
CRM = CRM_model(arbre)  
Random = random_model(arbre)  
opt_espgain = opt_espgain_model(arbre)  

lightCRM_tree = lightCRM.run(10000)  
CRM_tree = CRM.run(10000)  
Random_tree = Random.run()  
opt_espgain_tree = opt_espgain.run()  

## Les différents travaux sur les clusters et les fonctions annexes pour le Texas Holdem sont présents dans les différents sous-dossiers de "TexasHoldem"

## Auteurs

* Eléonore Blanchard
* Yannick Ly

