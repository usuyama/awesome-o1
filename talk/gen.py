from chalk import *
import chalk
import numpy as np
import random
from functools import partial
from dataclasses import dataclass

c4 = "#257180"
c2 = "#F2E5BF"
c3 = "#FD8B51"
c1 = "#CB6040"


def rollout(t, v, T, d=1):
    n = v
    for t2 in range(t, T):
        n = n + (random.random() - 0.5) / d
        yield (t2 + 1, n)


def expand(t, v, T):
    if t == T:
        return []
    return [(t + 1, v + 1), (t + 1, v - 1)]


def rwalk1(t, v, T, d=1):
    if t == T:
        return []
    return [(t + 1, v + (random.random() - 0.5) / d)]


def rwalk(t, v, T, d=5):
    if t == T:
        return []
    return [(t + 1, v + random.random() / d), (t + 1, v - random.random() / d)]


def bwalk(t, v, T, d=5):
    if t == T:
        return []
    return [(t + 1, v + 1 if random.random() > 0.5 else -1)]


def chain(t, v, T):
    if t == T:
        return []
    return [(t + 1, v)]


def opt(t, v, T):
    if t == 3:
        return []
    return [(t + 1, 0)]


def nonopt(t, v, T):
    if t == T:
        return []
    if t >= 4:
        return [(t + 1, 0)]
    return [(t + 1, v + 1 if t < 2 else v - 1)]


def make_chain(expand, T=6):
    queue = [(0, 0)]
    # nodes, edges = [], []
    nodes, edges, roll = [], [], [((0, 0), (0, 0.1))]
    while queue:
        (t, v) = queue[0]
        queue = queue[1:]
        new = expand(t, v, T)
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


def make_beam(expand, T=6, end=None, beam=5, dorollout=True):
    if end is None:
        end = T
    queue = {}
    queue[0] = [(0, 0)]
    nodes, edges, roll = [], [], [((0, 0), (0, 0.1))]
    for t in range(end):
        random.shuffle(queue[t])
        queue[t] = queue[t][:beam]
        queue[t + 1] = []
        for t, v in queue[t]:
            if t < end - 1:
                new = expand(t, v, T)
                queue[t + 1] += new
                for n in new:
                    edges.append(((t, v), n))
            nodes.append((t, v))

            if t == end - 1 and t < T:
                # rollout
                if dorollout:
                    for _ in range(5):
                        c = (t, v)
                        for c2 in rollout(t, v, T):
                            roll.append((c, c2))
                            c = c2
                else:
                    c = (t, v)
                    roll.append((c, (T, 0)))

    return nodes, edges, roll


@dataclass
class Node:
    nodes: list["Node"]
    val: float
    win: int
    total: int
    layer: int
    parent: Optional["Node"]
    rollout: bool = False
    selected: bool = False


def mcts_step(root: Node, T=6) -> Node:
    # Traverse until expand
    path = Node([], 0, 0, 0, 0, None)
    yield path
    cur_path = path
    current_node = root
    while current_node.nodes:
        next_node = max(
            current_node.nodes,
            key=lambda n: n.win / n.total
            + np.sqrt(2 * np.log(current_node.total) / n.total)
            if n.total > 0
            else float("inf"),
        )
        cur_path.nodes.append(Node([], next_node.val, 0, 0, next_node.layer, cur_path))
        cur_path = cur_path.nodes[0]
        current_node = next_node

    yield path
    # Expansion
    selected_node = mcts_expand(current_node)
    cur_path.nodes.append(
        Node([], selected_node.val, 0, 0, selected_node.layer, cur_path)
    )
    yield path

    # Rollout
    result_win = simulate(selected_node, T=T)  # Assuming T=6, adjust as needed
    yield path
    selected_node.selected = False
    selected_node.nodes = []
    # Backpropagation
    current = selected_node
    while current:
        current.win += result_win
        current.total += 1
        current = current.parent if hasattr(current, "parent") else None

    yield path


def bound(x):
    return np.maximum(np.minimum(3, x), -3)


def mcts_expand(node: Node) -> Node:
    for i in range(2):
        new_node = Node(
            nodes=[],
            val=bound(node.val + random.uniform(-1.5, 1.5)),
            win=0,
            total=0,
            layer=node.layer + 1,
            parent=node,
        )
        node.nodes.append(new_node)
    return new_node


def simulate(node: Node, T: int) -> Node:
    results = []
    for _ in range(8):
        curr = node
        while curr.layer < T:
            new_node = Node(
                nodes=[],
                val=bound(curr.val + random.uniform(-1.0, 1.0)),
                win=0,
                total=0,
                layer=curr.layer + 1,
                parent=None,
                rollout=True,
            )
            curr.nodes.append(new_node)
            curr = new_node
        curr.win = int((curr.val < 0.5) and (curr.val > -0.5))
        results.append(curr)
    return sum([x.win for x in results]) / 8


def draw_node(root: Node):
    nodes = []
    edges = []
    rollout_edges = []

    def traverse(node, parent=None):
        if not node.rollout:
            nodes.append((node.layer, node.val, (node.win + 0.1) / (node.total + 0.8)))
            if parent:
                edges.append(((parent.layer, parent.val), (node.layer, node.val)))
        else:
            rollout_edges.append(((parent.layer, parent.val), (node.layer, node.val)))
        for child in node.nodes:
            traverse(child, node)

    traverse(root)

    return nodes, edges, rollout_edges if rollout_edges else [((0, 0), (0, 0.1))]


def draw(
    nodes,
    edges,
    rollout_edges,
    name,
    T=6,
    csize=0.2,
    lwidth=0.5,
    draw_final=True,
    final_opacity=1.0,
):
    ns = list(nodes)
    mag = False

    def round(v):
        if final_opacity < 1.0:
            return int(v * 2) / 2
        else:
            return v

    if len(nodes[0]) == 3:
        mag = True
        nodes = np.array([(t, v) for (t, v, m) in ns if t <= T - 1])
        nodes_m = np.array([m for (t, v, m) in ns if t <= T - 1])
        finaln = np.array([(t, round(v)) for (t, v, m) in ns if t == T])
    else:
        nodes = np.array([(t, v) for (t, v) in ns if t <= T - 1])
        finaln = np.array([(t, round(v)) for (t, v) in ns if t == T])
    edges = np.array(edges)
    redges = np.array(rollout_edges)

    c = circle(csize).line_width(0.1)
    pts = tx.to_P2(nodes)
    z = c.translate_by(pts)
    if mag:
        v = 5 * np.minimum(0.2, nodes_m[..., None])
        z = z.fill_color(v * to_color(c4) + (1 - v) * to_color("red"))
    else:
        z = z.fill_color(c4)
    if finaln.shape[0] > 0:
        pts = tx.to_P2(finaln)
        y = c.translate_by(pts)
        y = y.concat().fill_color(c1).fill_opacity(final_opacity)
    else:
        y = empty()

    lines = (
        (
            Path.from_points([tx.to_P2(edges[:, 0]), tx.to_P2(edges[:, 1])], False)
            .stroke()
            .line_width(lwidth)
            + c.scale(0.5).translate_by(tx.to_P2(edges[:, 1]))
        )
        .line_color("darkgrey")
        .fill_color("darkgrey")
    )
    lines2 = (
        (
            Path.from_points([tx.to_P2(redges[:, 0]), tx.to_P2(redges[:, 1])], False)
            .stroke()
            .line_width(lwidth)
            .line_color(c2)
            + c.scale(0.2).translate_by(tx.to_P2(redges[:, 1]))
        )
        .line_color(c2)
        .fill_color(c2)
    )
    if draw_final:
        final = (
            rectangle(0.6, 1)
            .line_width(lwidth)
            .translate(T, 0)
            .fill_color(c3)
            .fill_opacity(0.7)
            .line_width(0.05)
        )
    else:
        final = empty()
    base = (
        final
        + lines.concat()
        + lines2.concat()
        + z.concat().fill_color("white").line_width(0)
        + z.concat()
        + y
        + c.fill_color(c1)
    )
    if name:
        base2 = (
            rectangle(T + 1, 5)
            .align_l()
            .translate(-0.5, 0)
            .fill_color("#faf0e6")
            .line_width(0.4)
            + base
        )
        base2.render(name, 512, draw_height=250)
    return base


def make_background(d, minh=2):
    w = d.get_envelope().width
    h = d.get_envelope().height
    r = (
        rectangle(w + 1, max(h, minh))
        .align_l()
        .translate(-0.5, 0)
        .fill_color("#faf0e6")
        .line_width(0.2)
    )
    return r + d


def make_tree():
    # Create the root node
    root = Node([], 0, 0, 0, 0, None)

    # Layer 1
    root.nodes = [Node([], 1.5, 0, 0, 1, root), Node([], -0.5, 0, 0, 1, root)]

    # Layer 2
    root.nodes[0].nodes = [
        Node([], root.nodes[0].val + 0.8, 0, 0, 2, root.nodes[0]),
        Node([], root.nodes[0].val - 0.3, 0, 0, 2, root.nodes[0]),
    ]
    root.nodes[1].nodes = [
        Node([], root.nodes[1].val + 0.2, 0, 0, 2, root.nodes[1]),
    ]

    # Layer 3
    chosen_path = random.choice(root.nodes)
    for node in root.nodes:
        for child in node.nodes:
            if node == chosen_path:
                child.nodes = [
                    Node([], child.val + random.uniform(0.1, 0.5), 0, 0, 3, child),
                    Node([], child.val - random.uniform(0.1, 0.5), 0, 0, 3, child),
                ]
            else:
                child.nodes = []

    # Layer 4
    chosen_child = random.choice(chosen_path.nodes)
    for child in chosen_path.nodes:
        for grandchild in child.nodes:
            if child == chosen_child:
                grandchild.nodes = [
                    Node(
                        [],
                        grandchild.val + random.uniform(0.05, 0.3),
                        0,
                        0,
                        4,
                        grandchild,
                    ),
                    Node(
                        [],
                        grandchild.val - random.uniform(0.05, 0.3),
                        0,
                        0,
                        4,
                        grandchild,
                    ),
                ]
            else:
                grandchild.nodes = []

    # Layer 5
    chosen_grandchild = random.choice(chosen_child.nodes)
    chosen_grandchild.nodes.append(
        Node(
            [],
            chosen_grandchild.val + random.uniform(0.05, 0.3),
            0,
            0,
            5,
            chosen_grandchild,
        )
    )

    return root


def linearize_tree(root: Node) -> Node:
    def dfs(node):
        if not node.nodes:
            return [node]

        result = [node]
        for child in node.nodes:
            result.extend(dfs(child))
        return result

    flattened = dfs(root)
    for i in range(len(flattened) - 1):
        flattened[i].nodes = [flattened[i + 1]]
    flattened[-1].nodes = []
    return flattened[0]


random.seed(0)

tree = make_tree()
draw(*draw_node(tree), "images/search.png", T=5)
draw(*draw_node(linearize_tree(tree)), "images/search2.png", T=5)


T = 10
root = Node([], 0, 0, 0, 0, None)
list(mcts_step(root, T=T))
random.seed(0)
# for i in range(0, 5, 5):
for i in range(0, 100, 5):
    for j, path in enumerate(mcts_step(root, T=T)):
        d = (
            # rectangle(T + 1, 7).line_width(0).align_l().translate(-0.5, 0)
            draw(*draw_node(root), "", T=T, csize=0.07)
            + (
                draw(
                    *draw_node(path), "", csize=0.07, T=T, draw_final=False
                ).fill_color("orange")
                if path.nodes
                else empty()
            )
        )
        d = make_background(d, 7)
        d.render(f"images/mcts{i + j:03}.png", 512, draw_height=100)

vcat(
    [make_background(draw(*make_chain(partial(rwalk1, d=1)), "x")) for _ in range(5)]
).render("images/reject1.png", 512, draw_height=250)


draw(*make_chain(expand), "images/expand.png")
draw(*make_chain(chain), "images/chain.png")
draw(*make_chain(rwalk1), "images/ancestral.png", draw_final=False)


draw(
    *multi([make_chain(opt), make_chain(nonopt)]),
    "images/stream.png",
    draw_final=True,
)


draw(
    *multi([make_chain(partial(rwalk1, d=1)) for _ in range(10)]),
    "images/bwalk.png",
    draw_final=False,
    final_opacity=0.2,
)

random.seed(0)
draw(
    *multi(
        [
            (n, e, r)
            for _ in range(10)
            for n, e, r in [make_chain(partial(rwalk1, d=1))]
            if -0.5 < n[-1][-1] < 0.5
        ]
    ),
    "images/rejectb.png",
    draw_final=True,
)

random.seed(0)
draw(
    *multi(
        [
            (n, e, r)
            for _ in range(10)
            for n, e, r in [make_chain(partial(rwalk1, d=1))]
            if -0.5 < n[-1][-1] < 0.5
        ]
    ),
    "images/rejectb.png",
    draw_final=True,
)

draw(
    *multi([make_chain(partial(rwalk1, d=1)) for _ in range(100)]),
    "images/all.png",
    draw_final=True,
)


T = 6
draw(*make_beam(partial(rwalk, d=1), end=T + 1), "images/beam.png", draw_final=False)


for i in range(1, 5):
    random.seed(2)
    draw(*make_beam(partial(rwalk, d=2), beam=4, end=i + 1), f"images/beamroll{i}.png")


draw(
    *make_beam(partial(rwalk, d=1), beam=4, end=T - 1, dorollout=False),
    "images/beamguide.png",
)

draw(*make_beam(partial(rwalk1, d=1), beam=1, end=T - 2), "images/mcroll.png")

draw(*make_chain(rwalk), "images/random.png", csize=0.1, lwidth=0.2)
