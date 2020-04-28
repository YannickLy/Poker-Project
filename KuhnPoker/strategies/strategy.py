from algorithms.CRM import CRM, lightCRM
from algorithms.random_strategy import random_strategy

class Strategy:

    def __init__(self, arbre):
        self.arbre = arbre
    
    def lightCRM(self, simulations = 1):
        strategy = lightCRM(self.arbre)
        strategy.run(simulations)
        strategy.compute_equilibre_nash()
        return strategy.information_set_equilibre_nash

    def CRM(self, simulations = 1):
        strategy = lightCRM(self.arbre)
        strategy.run(simulations)
        strategy.compute_equilibre_nash()
        return strategy.information_set_equilibre_nash

    def Random(self):
        return random_strategy(self.arbre)
