from kuhn.kuhnpoker import NoeudChance
from common import constants as c
from strategies.strategy import lightCRM_model, CRM_model, random_model
import random
import pandas as pd

def compare_strat(stratIA_1, stratIA_2, name_stratIA_1, name_stratIA_2, iterations = 10000):

    compare = {c.J1:{'nb_victoire':0, 'payoff':0}, c.J2:{'nb_victoire':0, 'payoff':0}}
    
    for _ in range(iterations):
        
        qui_commence = random.randrange(2)
        J = c.J1 if qui_commence == 0 else c.J2
        etat = arbre.sample_one()
        
        while etat.enfants != {}:
            inf_set = etat.information_set()
            qui_joue = stratIA_1[inf_set] if J == c.J1 else stratIA_2[inf_set]
            rand = random.uniform(0, 1)
            [key1, key2] = qui_joue.keys()
            if rand <= qui_joue[key1]:
                strat = key1
            else:
                strat = key2
            etat = etat.enfants[strat]
            J = -J
        
        if etat.historique_actions[-1] == 'CHECK' and etat.historique_actions[-2] == 'CHECK':
            winner = c.GAGNANT[etat.cartes] if qui_commence == 0 else -c.GAGNANT[etat.cartes]
            pot = 2
        elif etat.historique_actions[-1] == 'CALL' and etat.historique_actions[-2] == 'BET':
            winner = c.GAGNANT[etat.cartes] if qui_commence == 0 else -c.GAGNANT[etat.cartes]
            pot = 4
        elif etat.historique_actions[-1] == 'FOLD':
            pot = 3
            if (len(etat.historique_actions) == 2 and qui_commence == 0) or (len(etat.historique_actions) == 3 and qui_commence == 1):
                winner = c.J1
            else:
                winner = c.J2        
        
        compare[winner]['nb_victoire'] += 1
        compare[winner]['payoff'] += pot
        compare[-winner]['payoff'] -= pot

    compare[name_stratIA_1] = compare[c.J1]
    compare[name_stratIA_2] = compare[c.J2]
    del compare[c.J1]
    del compare[c.J2]
        
    return compare

arbre = NoeudChance(c.COMBINAISONS_CARTES)

lightCRM = lightCRM_model(arbre)
CRM = CRM_model(arbre)
lightCRM_1000 = lightCRM.run(1000)
CRM_1000 = CRM.run(1000)
compare_lightCRM_CRM_1000 = compare_strat(lightCRM_1000, CRM_1000, 'lightCRM_1000', 'CRM_1000')
lightCRM_5000 = lightCRM.run(5000)
CRM_5000 = CRM.run(5000)
compare_lightCRM_CRM_5000 = compare_strat(lightCRM_5000, CRM_5000, 'lightCRM_5000', 'CRM_5000')
lightCRM_10000 = lightCRM.run(10000)
CRM_10000 = CRM.run(10000)
compare_lightCRM_CRM_10000 = compare_strat(lightCRM_10000, CRM_10000, 'lightCRM_10000', 'CRM_10000')
df_payoff = pd.DataFrame(index = [1000, 5000, 10000], columns = ['lightCRM', 'CRM'])
df_payoff.loc[1000] = [compare_lightCRM_CRM_1000['lightCRM_1000']['payoff'], compare_lightCRM_CRM_1000['CRM_1000']['payoff']]
df_payoff.loc[5000] = [compare_lightCRM_CRM_5000['lightCRM_5000']['payoff'], compare_lightCRM_CRM_5000['CRM_5000']['payoff']]
df_payoff.loc[10000] = [compare_lightCRM_CRM_10000['lightCRM_10000']['payoff'], compare_lightCRM_CRM_10000['CRM_10000']['payoff']]
df_victoires = pd.DataFrame(index = [1000, 5000, 10000], columns = ['lightCRM', 'CRM'])
df_victoires.loc[1000] = [compare_lightCRM_CRM_1000['lightCRM_1000']['nb_victoire'], compare_lightCRM_CRM_1000['CRM_1000']['nb_victoire']]
df_victoires.loc[5000] = [compare_lightCRM_CRM_5000['lightCRM_5000']['nb_victoire'], compare_lightCRM_CRM_5000['CRM_5000']['nb_victoire']]
df_victoires.loc[10000] = [compare_lightCRM_CRM_10000['lightCRM_10000']['nb_victoire'], compare_lightCRM_CRM_10000['CRM_10000']['nb_victoire']]
print(df_payoff)
print(df_victoires)

Random = random_model(arbre)
Random_tree = Random.run()
compare_lightCRM_Random_1000 = compare_strat(lightCRM_1000, Random_tree, 'lightCRM_1000', 'Random')
Random_tree = Random.run()
compare_lightCRM_Random_5000 = compare_strat(lightCRM_5000, Random_tree, 'lightCRM_5000', 'Random')
Random_tree = Random.run()
compare_lightCRM_Random_10000 = compare_strat(lightCRM_10000, Random_tree, 'lightCRM_10000', 'Random')
df_payoff = pd.DataFrame(index = [1000, 5000, 10000], columns = ['lightCRM', 'Random'])
df_payoff.loc[1000] = [compare_lightCRM_Random_1000['lightCRM_1000']['payoff'], compare_lightCRM_Random_1000['Random']['payoff']]
df_payoff.loc[5000] = [compare_lightCRM_Random_5000['lightCRM_5000']['payoff'], compare_lightCRM_Random_5000['Random']['payoff']]
df_payoff.loc[10000] = [compare_lightCRM_Random_10000['lightCRM_10000']['payoff'], compare_lightCRM_Random_10000['Random']['payoff']]
df_victoires = pd.DataFrame(index = [1000, 5000, 10000], columns = ['lightCRM', 'Random'])
df_victoires.loc[1000] = [compare_lightCRM_Random_1000['lightCRM_1000']['nb_victoire'], compare_lightCRM_Random_1000['Random']['nb_victoire']]
df_victoires.loc[5000] = [compare_lightCRM_Random_5000['lightCRM_5000']['nb_victoire'], compare_lightCRM_Random_5000['Random']['nb_victoire']]
df_victoires.loc[10000] = [compare_lightCRM_Random_10000['lightCRM_10000']['nb_victoire'], compare_lightCRM_Random_10000['Random']['nb_victoire']]
print(df_payoff)
print(df_victoires)

