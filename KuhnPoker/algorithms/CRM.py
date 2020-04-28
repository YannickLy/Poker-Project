from common import constants as c
from common.func import init_information_set_proba, init_information_set_vide
import copy

class CounterfactualRegretMinimization:

    def __init__(self, arbre, sampling):
        self.arbre = arbre
        self.information_set_proba = init_information_set_proba(arbre)
        self.information_set_regrets_cumul = init_information_set_vide(arbre)
        self.information_set_equilibre_nash = init_information_set_vide(arbre)
        self.sampling = sampling
        self.strategies = {}

    def __update_proba(self, inf_set):
        somme_regrets = sum(filter(lambda x : x > 0, self.information_set_regrets_cumul[inf_set].values()))
        for action in self.information_set_regrets_cumul[inf_set]:
            self.information_set_proba[inf_set][action] = max(self.information_set_regrets_cumul[inf_set][action], 0.) / somme_regrets if somme_regrets > 0 else 1. / len(self.information_set_regrets_cumul[inf_set].keys())

    def __update_proba_recurs(self, noeud):
        if noeud.is_terminal():
            return
        if not noeud.is_chance():
            self.__update_proba(noeud.information_set())
        for k in noeud.enfants:
            self.__update_proba_recurs(noeud.enfants[k])

    def __compute_regrets_cumul(self, inf_set, action, regret):
        self.information_set_regrets_cumul[inf_set][action] += regret

    def __compute_CRM(self, noeud, reach_J1, reach_J2):
        noeuds_enfants_utilites = {}
        if noeud.is_terminal():
            return noeud.evaluation()
        if noeud.is_chance():
            if self.sampling:
                return self.__compute_CRM(noeud.sample_one(), reach_J1, reach_J2)
            else:
                noeud_chance_outcome = {noeud.play(action) for action in noeud.actions}
                return noeud.chance_proba() * sum([self.__compute_CRM(outcome, reach_J1, reach_J2) for outcome in noeud_chance_outcome])
        esp_gain = 0.
        for action in noeud.actions:
            enfant_reach_J1 = reach_J1 * (self.information_set_proba[noeud.information_set()][action] if noeud.qui_joue == c.J1 else 1)
            enfant_reach_J2 = reach_J2 * (self.information_set_proba[noeud.information_set()][action] if noeud.qui_joue == c.J2 else 1)
            noeud_enfant_utilite = self.__compute_CRM(noeud.play(action), enfant_reach_J1, enfant_reach_J2)
            esp_gain +=  self.information_set_proba[noeud.information_set()][action] * noeud_enfant_utilite
            noeuds_enfants_utilites[action] = noeud_enfant_utilite
        cfr_reach = reach_J2 if noeud.qui_joue == c.J1 else reach_J1
        for action in noeud.actions:
            regret_action = noeud.qui_joue * cfr_reach * (noeuds_enfants_utilites[action] - esp_gain)
            self.__compute_regrets_cumul(noeud.information_set(), action, regret_action)
        return esp_gain

    def run(self, iterations = 1):
        for _ in range(0, iterations):
            self.__compute_CRM(self.arbre, 1, 1)
            self.__update_proba_recurs(self.arbre)
            self.strategies[_] = copy.deepcopy(self.information_set_proba)

    def compute_equilibre_nash(self):
        for k1 in self.information_set_equilibre_nash.keys():
            for k2 in self.information_set_equilibre_nash[k1].keys():
                somme = 0.
                for k3 in self.strategies.keys():
                    somme += self.strategies[k3][k1][k2]
                self.information_set_equilibre_nash[k1][k2] = somme / len(self.strategies)

class CRM(CounterfactualRegretMinimization):
    def __init__(self, arbre):
        super().__init__(arbre = arbre, sampling = False)

class lightCRM(CounterfactualRegretMinimization):
    def __init__(self, arbre):
        super().__init__(arbre = arbre, sampling = True)
