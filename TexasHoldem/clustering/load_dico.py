from common.timer import timer
import pickle

t = timer()
t.start()
with open('clustering/dico_preflop.pickle', 'rb') as handle:
    preflop = pickle.load(handle)
t.stop()

print(t.total_run_time())
print(preflop)
