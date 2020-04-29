from kuhn.kuhnpoker import NoeudChance
from common import constants as c
from strategies.strategy import lightCRM_model, CRM_model, opt_espgain_model, random_model
from common.timer import timer
import random
import pandas as pd

def compare_strat(stratIA_1, stratIA_2, name_stratIA_1, name_stratIA_2, iterations = 100000):

    compare = {c.J1:{'nb_victoire':0, 'payoff':0}, c.J2:{'nb_victoire':0, 'payoff':0}}
    arbre = NoeudChance(c.COMBINAISONS_CARTES)
    
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

def compare_strat_only_J(stratIA_1, stratIA_2, name_stratIA_1, name_stratIA_2, iterations = 100000):

    compare = {c.J1:{'nb_victoire':0, 'payoff':0}, c.J2:{'nb_victoire':0, 'payoff':0}}
    arbre = NoeudChance(c.COMBINAISONS_CARTES)
    
    for _ in range(iterations):
        
        qui_commence = random.randrange(2)
        J = c.J1 if qui_commence == 0 else c.J2
        etat = arbre.enfants[random.choice(['JK', 'JQ'])] if J == c.J1 else arbre.enfants[random.choice(['KJ', 'QJ'])]
        
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

def compare_strat_only_K(stratIA_1, stratIA_2, name_stratIA_1, name_stratIA_2, iterations = 100000):

    compare = {c.J1:{'nb_victoire':0, 'payoff':0}, c.J2:{'nb_victoire':0, 'payoff':0}}
    arbre = NoeudChance(c.COMBINAISONS_CARTES)
    
    for _ in range(iterations):
        
        qui_commence = random.randrange(2)
        J = c.J1 if qui_commence == 0 else c.J2
        etat = arbre.enfants[random.choice(['KJ', 'KQ'])] if J == c.J1 else arbre.enfants[random.choice(['JK', 'QK'])]
        
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

def compare_strat_only_Q(stratIA_1, stratIA_2, name_stratIA_1, name_stratIA_2, iterations = 100000):

    compare = {c.J1:{'nb_victoire':0, 'payoff':0}, c.J2:{'nb_victoire':0, 'payoff':0}}
    arbre = NoeudChance(c.COMBINAISONS_CARTES)
    
    for _ in range(iterations):
        
        qui_commence = random.randrange(2)
        J = c.J1 if qui_commence == 0 else c.J2
        etat = arbre.enfants[random.choice(['QJ', 'QK'])] if J == c.J1 else arbre.enfants[random.choice(['KQ', 'JQ'])]
        
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
t = timer()

### lightCRM VS. CRM
lightCRM = lightCRM_model(arbre)
CRM = CRM_model(arbre)

t.start()
lightCRM_1000 = lightCRM.run(1000)
t.stop()
t_lightCRM_1000 = t.total_run_time()
t.start()
CRM_1000 = CRM.run(1000)
t.stop()
t_CRM_1000 = t.total_run_time()

t.start()
lightCRM_5000 = lightCRM.run(5000)
t.stop()
t_lightCRM_5000 = t.total_run_time()
t.start()
CRM_5000 = CRM.run(5000)
t.stop()
t_CRM_5000 = t.total_run_time()

t.start()
lightCRM_10000 = lightCRM.run(10000)
t.stop()
t_lightCRM_10000 = t.total_run_time()
t.start()
CRM_10000 = CRM.run(10000)
t.stop()
t_CRM_10000 = t.total_run_time()

t.start()
lightCRM_100000 = lightCRM.run(100000)
t.stop()
t_lightCRM_100000 = t.total_run_time()
t.start()
CRM_100000 = CRM.run(100000)
t.stop()
t_CRM_100000 = t.total_run_time()

compare_lightCRM_CRM_1000 = compare_strat(lightCRM_1000, CRM_1000, 'lightCRM_1000', 'CRM_1000')
compare_lightCRM_CRM_5000 = compare_strat(lightCRM_5000, CRM_5000, 'lightCRM_5000', 'CRM_5000')
compare_lightCRM_CRM_10000 = compare_strat(lightCRM_10000, CRM_10000, 'lightCRM_10000', 'CRM_10000')
compare_lightCRM_CRM_100000 = compare_strat(lightCRM_100000, CRM_100000, 'lightCRM_100000', 'CRM_100000')

df_payoff = pd.DataFrame(index = [1000, 5000, 10000, 100000], columns = ['lightCRM', 'CRM'])
df_payoff.loc[1000] = [compare_lightCRM_CRM_1000['lightCRM_1000']['payoff'], compare_lightCRM_CRM_1000['CRM_1000']['payoff']]
df_payoff.loc[5000] = [compare_lightCRM_CRM_5000['lightCRM_5000']['payoff'], compare_lightCRM_CRM_5000['CRM_5000']['payoff']]
df_payoff.loc[10000] = [compare_lightCRM_CRM_10000['lightCRM_10000']['payoff'], compare_lightCRM_CRM_10000['CRM_10000']['payoff']]
df_payoff.loc[100000] = [compare_lightCRM_CRM_100000['lightCRM_100000']['payoff'], compare_lightCRM_CRM_100000['CRM_100000']['payoff']]
print(df_payoff)

df_victoires = pd.DataFrame(index = [1000, 5000, 10000, 100000], columns = ['lightCRM', 'CRM'])
df_victoires.loc[1000] = [compare_lightCRM_CRM_1000['lightCRM_1000']['nb_victoire'], compare_lightCRM_CRM_1000['CRM_1000']['nb_victoire']]
df_victoires.loc[5000] = [compare_lightCRM_CRM_5000['lightCRM_5000']['nb_victoire'], compare_lightCRM_CRM_5000['CRM_5000']['nb_victoire']]
df_victoires.loc[10000] = [compare_lightCRM_CRM_10000['lightCRM_10000']['nb_victoire'], compare_lightCRM_CRM_10000['CRM_10000']['nb_victoire']]
df_victoires.loc[100000] = [compare_lightCRM_CRM_100000['lightCRM_100000']['nb_victoire'], compare_lightCRM_CRM_100000['CRM_100000']['nb_victoire']]
print(df_victoires)

df_tempsexec = pd.DataFrame(index = [1000, 5000, 10000, 100000], columns = ['lightCRM', 'CRM'])
df_tempsexec.loc[1000] = [t_lightCRM_1000, t_CRM_1000]
df_tempsexec.loc[5000] = [t_lightCRM_5000, t_CRM_5000]
df_tempsexec.loc[10000] = [t_lightCRM_10000, t_CRM_10000]
df_tempsexec.loc[100000] = [t_lightCRM_100000, t_CRM_100000]
print(df_tempsexec)

### lightCRM VS. OptEspGain
opt_espgain = opt_espgain_model(arbre)
opt_espgain_tree = opt_espgain.run()

compare_lightCRM_optespgain_1000 = compare_strat(lightCRM_1000, opt_espgain_tree, 'lightCRM_1000', 'Opt_EspGain')
compare_lightCRM_optespgain_5000 = compare_strat(lightCRM_5000, opt_espgain_tree, 'lightCRM_5000', 'Opt_EspGain')
compare_lightCRM_optespgain_10000 = compare_strat(lightCRM_10000, opt_espgain_tree, 'lightCRM_10000', 'Opt_EspGain')
compare_lightCRM_optespgain_100000 = compare_strat(lightCRM_100000, opt_espgain_tree, 'lightCRM_100000', 'Opt_EspGain')

df_payoff = pd.DataFrame(index = [1000, 5000, 10000, 100000], columns = ['lightCRM', 'Opt_EspGain'])
df_payoff.loc[1000] = [compare_lightCRM_optespgain_1000['lightCRM_1000']['payoff'], compare_lightCRM_optespgain_1000['Opt_EspGain']['payoff']]
df_payoff.loc[5000] = [compare_lightCRM_optespgain_5000['lightCRM_5000']['payoff'], compare_lightCRM_optespgain_5000['Opt_EspGain']['payoff']]
df_payoff.loc[10000] = [compare_lightCRM_optespgain_10000['lightCRM_10000']['payoff'], compare_lightCRM_optespgain_10000['Opt_EspGain']['payoff']]
df_payoff.loc[100000] = [compare_lightCRM_optespgain_100000['lightCRM_100000']['payoff'], compare_lightCRM_optespgain_100000['Opt_EspGain']['payoff']]
print(df_payoff)

df_victoires = pd.DataFrame(index = [1000, 5000, 10000, 100000], columns = ['lightCRM', 'Opt_EspGain'])
df_victoires.loc[1000] = [compare_lightCRM_optespgain_1000['lightCRM_1000']['nb_victoire'], compare_lightCRM_optespgain_1000['Opt_EspGain']['nb_victoire']]
df_victoires.loc[5000] = [compare_lightCRM_optespgain_5000['lightCRM_5000']['nb_victoire'], compare_lightCRM_optespgain_5000['Opt_EspGain']['nb_victoire']]
df_victoires.loc[10000] = [compare_lightCRM_optespgain_10000['lightCRM_10000']['nb_victoire'], compare_lightCRM_optespgain_10000['Opt_EspGain']['nb_victoire']]
df_victoires.loc[100000] = [compare_lightCRM_optespgain_100000['lightCRM_100000']['nb_victoire'], compare_lightCRM_optespgain_100000['Opt_EspGain']['nb_victoire']]
print(df_victoires)

### lightCRM VS. Random
Random = random_model(arbre)

Random_tree = Random.run()
compare_lightCRM_Random_1000 = compare_strat(lightCRM_1000, Random_tree, 'lightCRM_1000', 'Random')
Random_tree = Random.run()
compare_lightCRM_Random_5000 = compare_strat(lightCRM_5000, Random_tree, 'lightCRM_5000', 'Random')
Random_tree = Random.run()
compare_lightCRM_Random_10000 = compare_strat(lightCRM_10000, Random_tree, 'lightCRM_10000', 'Random')
Random_tree = Random.run()
compare_lightCRM_Random_100000 = compare_strat(lightCRM_100000, Random_tree, 'lightCRM_100000', 'Random')

df_payoff = pd.DataFrame(index = [1000, 5000, 10000, 100000], columns = ['lightCRM', 'Random'])
df_payoff.loc[1000] = [compare_lightCRM_Random_1000['lightCRM_1000']['payoff'], compare_lightCRM_Random_1000['Random']['payoff']]
df_payoff.loc[5000] = [compare_lightCRM_Random_5000['lightCRM_5000']['payoff'], compare_lightCRM_Random_5000['Random']['payoff']]
df_payoff.loc[10000] = [compare_lightCRM_Random_10000['lightCRM_10000']['payoff'], compare_lightCRM_Random_10000['Random']['payoff']]
df_payoff.loc[100000] = [compare_lightCRM_Random_100000['lightCRM_100000']['payoff'], compare_lightCRM_Random_100000['Random']['payoff']]
print(df_payoff)

df_victoires = pd.DataFrame(index = [1000, 5000, 10000, 100000], columns = ['lightCRM', 'Random'])
df_victoires.loc[1000] = [compare_lightCRM_Random_1000['lightCRM_1000']['nb_victoire'], compare_lightCRM_Random_1000['Random']['nb_victoire']]
df_victoires.loc[5000] = [compare_lightCRM_Random_5000['lightCRM_5000']['nb_victoire'], compare_lightCRM_Random_5000['Random']['nb_victoire']]
df_victoires.loc[10000] = [compare_lightCRM_Random_10000['lightCRM_10000']['nb_victoire'], compare_lightCRM_Random_10000['Random']['nb_victoire']]
df_victoires.loc[100000] = [compare_lightCRM_Random_100000['lightCRM_100000']['nb_victoire'], compare_lightCRM_Random_100000['Random']['nb_victoire']]
print(df_victoires)

### OptEspGain VS. Random
compare_OptEspGain_Random = compare_strat(opt_espgain_tree, Random_tree, 'Opt_EspGain', 'Random')

df_compare = pd.DataFrame(index = ['Payoff', 'Victoire'], columns = ['Opt_EspGain', 'Random'])
df_compare.loc['Payoff'] = [compare_OptEspGain_Random['Opt_EspGain']['payoff'], compare_OptEspGain_Random['Random']['payoff']]
df_compare.loc['Victoire'] = [compare_OptEspGain_Random['Opt_EspGain']['nb_victoire'], compare_OptEspGain_Random['Random']['nb_victoire']]
print(df_compare)

Random = random_model(arbre)
Random_tree = Random.run()
opt_espgain = opt_espgain_model(arbre)
opt_espgain_tree = opt_espgain.run()

### lightCRM VS. Random avec seulement la carte roi pour lightCRM
compare_lightCRM_Random_K = compare_strat_only_K(lightCRM_100000, Random_tree, 'lightCRM_100000', 'Random')
df_compare = pd.DataFrame(index = ['Payoff', 'Victoire'], columns = ['lightCRM_100000', 'Random'])
df_compare.loc['Payoff'] = [compare_lightCRM_Random_K['lightCRM_100000']['payoff'], compare_lightCRM_Random_K['Random']['payoff']]
df_compare.loc['Victoire'] = [compare_lightCRM_Random_K['lightCRM_100000']['nb_victoire'], compare_lightCRM_Random_K['Random']['nb_victoire']]
print(df_compare)

### lightCRM VS. Random avec seulement la carte reine pour lightCRM
compare_lightCRM_Random_Q = compare_strat_only_Q(lightCRM_100000, Random_tree, 'lightCRM_100000', 'Random')
df_compare = pd.DataFrame(index = ['Payoff', 'Victoire'], columns = ['lightCRM_100000', 'Random'])
df_compare.loc['Payoff'] = [compare_lightCRM_Random_Q['lightCRM_100000']['payoff'], compare_lightCRM_Random_Q['Random']['payoff']]
df_compare.loc['Victoire'] = [compare_lightCRM_Random_Q['lightCRM_100000']['nb_victoire'], compare_lightCRM_Random_Q['Random']['nb_victoire']]
print(df_compare)

### lightCRM VS. OptEspGain avec seulement la carte valet pour lightCRM
compare_lightCRM_Random_J = compare_strat_only_J(lightCRM_100000, Random_tree, 'lightCRM_100000', 'Random')
df_compare = pd.DataFrame(index = ['Payoff', 'Victoire'], columns = ['lightCRM_100000', 'Random'])
df_compare.loc['Payoff'] = [compare_lightCRM_Random_J['lightCRM_100000']['payoff'], compare_lightCRM_Random_J['Random']['payoff']]
df_compare.loc['Victoire'] = [compare_lightCRM_Random_J['lightCRM_100000']['nb_victoire'], compare_lightCRM_Random_J['Random']['nb_victoire']]
print(df_compare)

### OptEspGain VS. Random avec seulement la carte roi pour OptEspGain
compare_OptEspGain_Random_K = compare_strat_only_K(opt_espgain_tree, Random_tree, 'Opt_EspGain', 'Random')
df_compare = pd.DataFrame(index = ['Payoff', 'Victoire'], columns = ['Opt_EspGain', 'Random'])
df_compare.loc['Payoff'] = [compare_OptEspGain_Random_K['Opt_EspGain']['payoff'], compare_OptEspGain_Random_K['Random']['payoff']]
df_compare.loc['Victoire'] = [compare_OptEspGain_Random_K['Opt_EspGain']['nb_victoire'], compare_OptEspGain_Random_K['Random']['nb_victoire']]
print(df_compare)

### OptEspGain VS. Random avec seulement la carte reine pour OptEspGain
compare_OptEspGain_Random_Q = compare_strat_only_Q(opt_espgain_tree, Random_tree, 'Opt_EspGain', 'Random')
df_compare = pd.DataFrame(index = ['Payoff', 'Victoire'], columns = ['Opt_EspGain', 'Random'])
df_compare.loc['Payoff'] = [compare_OptEspGain_Random_Q['Opt_EspGain']['payoff'], compare_OptEspGain_Random_Q['Random']['payoff']]
df_compare.loc['Victoire'] = [compare_OptEspGain_Random_Q['Opt_EspGain']['nb_victoire'], compare_OptEspGain_Random_Q['Random']['nb_victoire']]
print(df_compare)

### OptEspGain VS. Random avec seulement la carte valet pour OptEspGain
compare_OptEspGain_Random_J = compare_strat_only_J(opt_espgain_tree, Random_tree, 'Opt_EspGain', 'Random')
df_compare = pd.DataFrame(index = ['Payoff', 'Victoire'], columns = ['Opt_EspGain', 'Random'])
df_compare.loc['Payoff'] = [compare_OptEspGain_Random_J['Opt_EspGain']['payoff'], compare_OptEspGain_Random_J['Random']['payoff']]
df_compare.loc['Victoire'] = [compare_OptEspGain_Random_J['Opt_EspGain']['nb_victoire'], compare_OptEspGain_Random_J['Random']['nb_victoire']]
print(df_compare)

