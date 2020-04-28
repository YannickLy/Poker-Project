def init_information_set_proba(noeud):
    output = dict()
    def recursive(noeud):
        if not noeud.is_terminal():
            output[noeud.information_set()] = {action: 1. / len(noeud.actions) for action in noeud.actions}
            for k in noeud.enfants:
                recursive(noeud.enfants[k])
    recursive(noeud)
    return output

def init_information_set_vide(noeud):
    output = dict()
    def recursive(noeud):
        if not noeud.is_terminal():
            output[noeud.information_set()] = {action: 0. for action in noeud.actions}
            for k in noeud.enfants:
                recursive(noeud.enfants[k])
    recursive(noeud)
    return output
