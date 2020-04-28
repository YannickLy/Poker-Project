import numpy as np
from common import constantes as c

class main:
    
    def __init__(self, main, riviere):
        self.dict_couleurs = {c.COEUR: 0, c.CARREAU: 0, c.PIQUE: 0, c.TREFLE: 0} 
        self.liste_suite = [0, 0]
        self.dict_suites_couleurs = {c.COEUR: [0, 0], c.CARREAU: [0, 0], c.PIQUE: [0, 0], c.TREFLE: [0, 0]}
        self.liste_singletons = []
        self.liste_doubles = []
        self.liste_triples = []
        self.liste_quadruple = []
        self.liste_tie_break = []
        
        self.liste_carte = main + riviere
        self.liste_carte_valeurs = [c.VALEURS.find(v) for v, _ in self.liste_carte]
        self.liste_carte_couleurs = [c.COULEURS.find(v) for _, v in self.liste_carte]
        
    def __sort(self):
        idx = np.argsort(self.liste_carte_valeurs)
        self.liste_carte_valeurs.sort()
        self.liste_carte_couleurs = [self.liste_carte_couleurs[i] for i in idx]
    
    def __get_carac(self):
        self.__sort()
        
        for i in range(7):
            v = self.liste_carte_valeurs[i]           
            if v in self.liste_singletons:
                self.liste_doubles.append(v)
                self.liste_singletons.remove(v)
            elif v in self.liste_doubles:
                self.liste_triples.append(v)
                self.liste_doubles.remove(v)
            elif v in self.liste_triples:
                self.liste_quadruple.append(v)
                self.liste_triples.remove(v)
            else:
                self.liste_singletons.append(v)
            
            r = str(self.liste_carte_couleurs[i])
            self.dict_couleurs[r]+=1
            
            if self.liste_suite[1] == 0:
                self.liste_suite[0] = v
                self.liste_suite[1] = 1
            elif self.liste_suite[0] == v-1:
                self.liste_suite[0] = v
                self.liste_suite[1] += 1
            elif self.liste_suite[1] < 5:
                self.liste_suite[0] = v
                self.liste_suite[1] = 1
            
            if self.dict_suites_couleurs[r][1] == 0:
                self.dict_suites_couleurs[r][0] = v
                self.dict_suites_couleurs[r][1] = 1
            elif self.dict_suites_couleurs[r][0] == v-1:
                self.dict_suites_couleurs[r][0] = v
                self.dict_suites_couleurs[r][1] += 1
            elif self.dict_suites_couleurs[r][1] < 5:
                self.dict_suites_couleurs[r][0] = v
                self.dict_suites_couleurs[r][1] = 1
                
    def __is_quinte_flush_royale(self):
        for val in self.dict_suites_couleurs.values():
            if (val[0] == 12) & (val[1] >= 5):
                return True
        return False

    def __is_quinte_flush(self):
        for val in self.dict_suites_couleurs.values():
            if val[1] >= 5:
                self.liste_tie_break = [val[0]]
                return True
        return False

    def __is_carre(self):
        if len(self.liste_quadruple) != 0:
            if self.liste_carte_valeurs[6] != self.liste_quadruple:
                acolyte = self.liste_carte_valeurs[6]
            elif self.liste_carte_valeurs[5] != self.liste_quadruple:
                acolyte = self.liste_carte_valeurs[5]
            elif self.liste_carte_valeurs[4] != self.liste_quadruple:
                acolyte = self.liste_carte_valeurs[4]
            elif self.liste_carte_valeurs[3] != self.liste_quadruple:
                acolyte = self.liste_carte_valeurs[3]
            else:
                acolyte = self.liste_carte_valeurs[2]
            self.liste_tie_break = self.liste_quadruple
            self.liste_tie_break.append(acolyte)
            return True
        return False
    
    def __is_full(self):
        if (len(self.liste_triples) > 0) & (len(self.liste_doubles) > 0):
            self.liste_tie_break = [self.liste_triples[len(self.liste_triples)-1], self.liste_doubles[len(self.liste_doubles)-1]]
            return True
        return False
    
    def __is_couleur(self):
        for k in self.dict_couleurs.keys():
            if self.dict_couleurs[k] >= 5:
                for i in range(6, -1, -1):
                    if (self.liste_carte_couleurs[i] == int(k)) & (len(self.liste_tie_break) < 5) :
                        self.liste_tie_break.append(self.liste_carte_valeurs[i])
                return True
        return False
    
    def __is_quinte(self):
        if self.liste_suite[1] >= 5:
            self.liste_tie_break.append(self.liste_suite[0])
            return True
        return False
    
    def __is_brelan(self):
        if len(self.liste_triples) > 0:
            kickers = []
            i = 6
            while i >= 0 and len(kickers) <= 1:
                if self.liste_carte_valeurs[i] != self.liste_triples[len(self.liste_triples)-1]:
                    kickers.append(self.liste_carte_valeurs[i])
                i-=1
            self.liste_tie_break = [self.liste_triples[len(self.liste_triples)-1]] + kickers
            return True
        return False

    def __is_double_paire(self):
        if len(self.liste_doubles) >= 2:
            for i in range(6, -1, -1):
                if (self.liste_carte_valeurs[i] != self.liste_doubles[len(self.liste_doubles)-1]) & (self.liste_carte_valeurs[i] != self.liste_doubles[len(self.liste_doubles)-2]):
                    acolyte = self.liste_carte_valeurs[i]
                    self.liste_tie_break = [self.liste_doubles[len(self.liste_doubles)-1], self.liste_doubles[len(self.liste_doubles)-2], acolyte]
                    return True
        return False
    
    def __is_paire(self):
        if len(self.liste_doubles) == 1:
            i = 6
            kickers = []
            while (i >= 0) & (len(kickers) < 3):
                if self.liste_carte_valeurs[i] != self.liste_doubles[len(self.liste_doubles)-1]:
                    kickers.append(self.liste_carte_valeurs[i])
                i-=1
            self.liste_tie_break = [self.liste_doubles[0]] + kickers
            return True
        return False
    
    def __is_carte_haute(self):
        for i in range(6, -1, -1):
            self.liste_tie_break.append(self.liste_carte_valeurs[i])

    def get_score(self):
        self.__get_carac()
        if self.__is_quinte_flush_royale(): return c.SCORE_QUINTE_FLUSH_ROYALE
        elif self.__is_quinte_flush(): return c.SCORE_QUINTE_FLUSH
        elif self.__is_carre(): return c.SCORE_CARRE
        elif self.__is_full(): return c.SCORE_FULL
        elif self.__is_couleur(): return c.SCORE_COULEUR
        elif self.__is_quinte(): return c.SCORE_QUINTE
        elif self.__is_brelan(): return c.SCORE_BRELAN
        elif self.__is_double_paire(): return c.SCORE_DOUBLE_PAIRE
        elif self.__is_paire(): return c.SCORE_PAIRE
        else: return c.SCORE_HAUTEUR