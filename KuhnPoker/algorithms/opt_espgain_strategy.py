from algorithms.CRM import CRM

def opt_espgain_strategy(arbre):
    model = CRM(arbre)
    model.run(1)
    model.compute_equilibre_nash()
    return model.information_set_equilibre_nash