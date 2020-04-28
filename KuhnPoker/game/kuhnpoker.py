from KuhnPoker.common import constantes as c
import random

class Noeud:

    def __init__(self, parent, qui_joue, actions):
        self.parent = parent
        self.qui_joue = qui_joue
        self.actions = actions

    def play(self, action):
        return self.enfants[action]

    def is_chance(self):
        return self.qui_joue == c.CHANCE

    def information_set(self):
        return

class NoeudChance(Noeud):

    def __init__(self, actions):
        super().__init__(parent = None, qui_joue = c.CHANCE, actions = actions)
        self.enfants = {
            cartes: NoeudDecision(
                self, c.J1, [],  cartes, [c.BET, c.CHECK]
            ) for cartes in self.actions
        }
        self._chance_proba = 1. / len(self.enfants)

    def is_terminal(self):
        return False

    def information_set(self):
        return "."

    def chance_proba(self):
        return self._chance_proba

    def sample_one(self):
        return random.choice(list(self.enfants.values()))

class NoeudDecision(Noeud):

    def __init__(self, parent, qui_joue, historique_actions, cartes, actions):
        super().__init__(parent = parent, qui_joue = qui_joue, actions = actions)

        self.historique_actions = historique_actions
        self.cartes = cartes
        self.enfants = {
            action : NoeudDecision(
                self,
                -qui_joue,
                self.historique_actions + [action],
                cartes,
                self.__get_actions_prochain_tour(action)
            ) for action in self.actions
        }

        carte_joueur = self.cartes[0] if self.qui_joue == c.J1 else self.cartes[1]
        if not self.is_terminal(): self._information_set = ".{0}.{1}".format(carte_joueur, ".".join(self.historique_actions))

    def __get_actions_prochain_tour(self, action):
        if len(self.historique_actions) == 0 and action == c.BET:
            return [c.FOLD, c.CALL]
        elif len(self.historique_actions) == 0 and action == c.CHECK:
            return [c.BET, c.CHECK]
        elif self.historique_actions[-1] == c.CHECK and action == c.BET:
            return [c.CALL, c.FOLD]
        elif action == c.CALL or action == c.FOLD or (self.historique_actions[-1] == c.CHECK and action == c.CHECK):
            return []

    def information_set(self):
        return self._information_set

    def is_terminal(self):
        return self.actions == []

    def evaluation(self):
        if self.historique_actions[-1] == c.CHECK and self.historique_actions[-2] == c.CHECK:
            return c.GAGNANT[self.cartes] * 1 
        if self.historique_actions[-2] == c.BET and self.historique_actions[-1] == c.CALL:
            return c.GAGNANT[self.cartes] * 2
        if self.historique_actions[-2] == c.BET and self.historique_actions[-1] == c.FOLD:
            return self.qui_joue * 1
