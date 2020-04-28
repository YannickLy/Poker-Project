VALEURS = '23456789TJQKA' # T = 10, J = Valet, Q = Reine, K = Roi, A = As
COULEURS = 'HDSC' # H = Coeur, D = Carreau, S = Pique, C = Trèfle
COEUR = '0'
CARREAU = '1'
PIQUE = '2'
TREFLE = '3'

SCORE_QUINTE_FLUSH_ROYALE = 10
SCORE_QUINTE_FLUSH = 9
SCORE_CARRE = 8
SCORE_FULL = 7
SCORE_COULEUR = 6
SCORE_QUINTE = 5
SCORE_BRELAN = 4
SCORE_DOUBLE_PAIRE = 3
SCORE_PAIRE = 2
SCORE_HAUTEUR = 1

CARTES = [v+s for s in ['H', 'D', 'S', 'C'] for v in [str(i) for i in range(2, 10)] + list("TJKQA")]

