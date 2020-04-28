from KuhnPoker.algorithms.func import init_information_set_vide
import random

def random_strategy(arbre):
    information_set_random = init_information_set_vide(arbre)
    for k1 in information_set_random.keys():
        if k1 == '.':
            for k2 in information_set_random[k1].keys():
                information_set_random[k1][k2] = 1. / len(information_set_random[k1])
        else:
            nb_aleatoire = random.uniform(0, 1)
            for k2 in information_set_random[k1].keys():
                if (k2 == 'BET') or (k2 == 'CALL'):
                    information_set_random[k1][k2] = nb_aleatoire
                else:
                    information_set_random[k1][k2] = 1 - nb_aleatoire
    return information_set_random