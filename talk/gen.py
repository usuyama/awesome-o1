from chalk import *
import chalk


def chain(ds):
    d = hcat([d.named(i) for i, d in enumerate(ds)], 1)
    l = len(ds)
    for i in range(l - 1):
        d = d.connect(i, i + 1)
    return d


base = chain([circle(1), circle(1)])
base.render("chain.png")
