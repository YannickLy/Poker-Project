from TexasHoldem.common.main import main

class gagnant:
    
    def __init__(self, j1, j2, riviere):
        self.j1 = main(j1, riviere)
        self.j2 = main(j2, riviere)
        self.score_j1 = self.j1.get_score()
        self.score_j2 = self.j2.get_score()
        self.winner = ''
    
    def __compare_tie(self):
        self.winner = 'tie'
        for i in range(len(self.j1.liste_tie_break)):
            if self.j1.liste_tie_break[i] > self.j2.liste_tie_break[i]:
                self.winner = 1
                break
            elif self.j1.liste_tie_break[i] < self.j2.liste_tie_break[i]:
                self.winner = -1
                break
    
    def get_winner(self):       
        if self.score_j1 > self.score_j2:
            self.winner = 1
        elif self.score_j1 < self.score_j2:
            self.winner = -1
        else:
            self.__compare_tie()