from KuhnPoker.game.kuhnpoker import NoeudChance
from KuhnPoker.common import constantes as c
from KuhnPoker.algorithms.CRM import CRM, lightCRM
from KuhnPoker.algorithms.random_strategy import random_strategy

arbre = NoeudChance(c.COMBINAISONS_CARTES)

random_strategy = random_strategy(arbre)

lightCRM = lightCRM(arbre)
lightCRM.run(10000)
lightCRM.compute_equilibre_nash()

CRM = CRM(arbre)
CRM.run(10000)
CRM.compute_equilibre_nash()

print('')

