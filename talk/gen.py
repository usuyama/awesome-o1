from chalk import *
import chalk
import numpy as np
import random
from functools import partial

T = 6


def rollout(t, v, d=2):
    n = v
    for t2 in range(t, T):
        n = n + (random.random() - 0.5) / d
        yield (t2 + 1, n)


def expand(t, v):
    if t == T:
        return []
    return [(t + 1, v + 1), (t + 1, v - 1)]


def rwalk(t, v, d=5):
    if t == T:
        return []
    return [(t + 1, v + random.random() / d), (t + 1, v - random.random() / d)]


def bwalk(t, v, d=5):
    if t == T:
        return []
    return [(t + 1, v + 1 if random.random() > 0.5 else -1)]


def chain(t, v):
    if t == 5:
        return []
    return [(t + 1, v)]


def make_chain(expand):
    queue = [(0, 0)]
    # nodes, edges = [], []
    nodes, edges, roll = [], [], [((0, 0), (0, 0.1))]
    while queue:
        (t, v) = queue[0]
        queue = queue[1:]
        new = expand(t, v)
        queue += new
        for n in new:
            edges.append(((t, v), n))
        nodes.append((t, v))

    return nodes, edges, roll


def multi(ls):
    n, e, r = [], [], []
    for n1, e1, r1 in ls:
        n.extend(n1)
        e.extend(e1)
        r.extend(r1)
    return n, e, r


def make_beam(expand, end=T):
    queue = {}
    queue[0] = [(0, 0)]
    nodes, edges, roll = [], [], [((0, 0), (0, 0.1))]
    for t in range(end):
        random.shuffle(queue[t])
        queue[t] = queue[t][:5]
        queue[t + 1] = []
        for t, v in queue[t]:
            if t < end - 1:
                new = expand(t, v)
                queue[t + 1] += new
                for n in new:
                    edges.append(((t, v), n))
            nodes.append((t, v))

            if t == end - 1 and t < T:
                # rollout
                c = (t, v)
                for c2 in rollout(t, v):
                    roll.append((c, c2))
                    c = c2
    return nodes, edges, roll


def draw(nodes, edges, rollout_edges, name, csize=0.2, lwidth=0.5, draw_final=True):
    nodes = np.array(nodes)
    edges = np.array(edges)
    redges = np.array(rollout_edges)

    c = circle(csize).line_width(lwidth)
    pts = tx.to_P2(nodes)
    z = c.translate_by(pts)
    lines = (
        Path.from_points([tx.to_P2(edges[:, 0]), tx.to_P2(edges[:, 1])], False)
        .stroke()
        .line_width(lwidth)
    )
    lines2 = (
        Path.from_points([tx.to_P2(redges[:, 0]), tx.to_P2(redges[:, 1])], False)
        .stroke()
        .line_width(lwidth)
        .line_color("gray")
    )
    if draw_final:
        final = rectangle(0.3, 2).line_width(lwidth).translate(T, 0).fill_color("green")
    else:
        final = empty()
    base = (
        lines.concat()
        + lines2.concat()
        + z.concat().fill_color("white").line_width(0)
        + z.concat().fill_color("red").fill_opacity(0.2)
        + c.fill_color("blue")
        + final
    )
    base.render(name, 512)


draw(*make_chain(expand), "images/expand.png")
draw(*make_chain(chain), "images/chain.png")
draw(
    *multi([make_chain(bwalk) for _ in range(5)]), "images/bwalk.png", draw_final=False
)
draw(*make_beam(partial(rwalk, d=1)), "images/beam.png")
draw(*make_beam(partial(rwalk, d=1), end=T - 2), "images/beamroll.png")

draw(*make_chain(rwalk), "images/random.png", csize=0.1, lwidth=0.2)
