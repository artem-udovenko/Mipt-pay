similar_names = [["Account", "DebitAccount", "DepositAccount", "CreditAccount"],
                 ["Plan", "DebitPlan", "DepositPlan", "CreditPlan"]]

gods = ["DataOperator", "Admin", "Adaptor"]


""" A module that represents a tool for creating strict privacy of certain methods. """


def available_from(me, *valid: str):
    dep = me.f_back.f_locals["self"].__class__.__qualname__
    self = me.f_locals["self"].__class__.__qualname__
    with_similar = [] + gods
    for i in valid:
        flag = False
        for j in similar_names:
            if i in j:
                flag = True
                with_similar += j
        if not flag:
            with_similar.append(i)
    flag = False
    for j in similar_names:
        if self in j:
            flag = True
            with_similar += j
    if not flag:
        with_similar.append(self)
    if dep not in with_similar:
        raise TypeError(dep + " is not " + ', or '.join(with_similar))
