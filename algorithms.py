import heapq
import math
from typing import Any, Dict, Hashable, List, Tuple, Optional

import networkx as nx


Path = List[Hashable]


def reconstruct_path(
    parents: Dict[Hashable, Optional[Hashable]],
    start: Hashable,
    goal: Hashable,
) -> Path:
    if goal not in parents:
        return []
    path = [goal]
    cur = goal
    while cur != start:
        cur = parents.get(cur)
        if cur is None:
            return []
        path.append(cur)
    path.reverse()
    return path


def dijkstra(
    graph: nx.Graph,
    start: Hashable,
    goal: Hashable,
) -> Tuple[Path, float, int]:
    """
    Dijkstra's algorithm implemented from scratch.

    Returns:
        path: list of nodes from start to goal (empty if unreachable)
        distance: shortest distance (inf if unreachable)
        visited_count: number of expanded nodes
    """
    if start not in graph or goal not in graph:
        return [], math.inf, 0

    dist: Dict[Hashable, float] = {start: 0.0}
    parents: Dict[Hashable, Optional[Hashable]] = {start: None}
    visited = set()
    pq: List[Tuple[float, Hashable]] = [(0.0, start)]
    visited_count = 0

    while pq:
        cur_dist, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        visited_count += 1

        if u == goal:
            break

        for v, attrs in graph[u].items():
            w = float(attrs.get("weight", 1.0))
            nd = cur_dist + w
            if nd < dist.get(v, math.inf):
                dist[v] = nd
                parents[v] = u
                heapq.heappush(pq, (nd, v))

    distance = dist.get(goal, math.inf)
    path = reconstruct_path(parents, start, goal) if distance < math.inf else []
    return path, distance, visited_count


def _get_pos(graph: nx.Graph, node: Hashable) -> Optional[Tuple[float, float]]:
    pos = graph.nodes[node].get("pos")
    if pos is None:
        return None
    if isinstance(pos, (tuple, list)) and len(pos) >= 2:
        return float(pos[0]), float(pos[1])
    return None


def heuristic(
    graph: nx.Graph,
    node: Hashable,
    goal: Hashable,
    mode: str = "euclidean",
) -> float:
    """
    Heuristic h(n) used by A*.
    If no positional information is available, returns 0 (degenerates to Dijkstra).
    """
    p1 = _get_pos(graph, node)
    p2 = _get_pos(graph, goal)
    if p1 is None or p2 is None:
        return 0.0

    x1, y1 = p1
    x2, y2 = p2

    if mode == "manhattan":
        return abs(x1 - x2) + abs(y1 - y2)
    # default: euclidean
    return math.hypot(x1 - x2, y1 - y2)


def astar(
    graph: nx.Graph,
    start: Hashable,
    goal: Hashable,
    heuristic_mode: str = "euclidean",
) -> Tuple[Path, float, int]:
    """
    A* search implemented from scratch.

    Returns:
        path: list of nodes from start to goal (empty if unreachable)
        distance: shortest distance (inf if unreachable)
        visited_count: number of expanded nodes
    """
    if start not in graph or goal not in graph:
        return [], math.inf, 0

    open_set: List[Tuple[float, float, Hashable]] = []
    g_score: Dict[Hashable, float] = {start: 0.0}
    parents: Dict[Hashable, Optional[Hashable]] = {start: None}

    h0 = heuristic(graph, start, goal, heuristic_mode)
    heapq.heappush(open_set, (h0, 0.0, start))

    visited = set()
    visited_count = 0

    while open_set:
        f, cur_g, u = heapq.heappop(open_set)
        if u in visited:
            continue
        visited.add(u)
        visited_count += 1

        if u == goal:
            break

        for v, attrs in graph[u].items():
            w = float(attrs.get("weight", 1.0))
            tentative_g = cur_g + w

            if tentative_g < g_score.get(v, math.inf):
                g_score[v] = tentative_g
                parents[v] = u
                h = heuristic(graph, v, goal, heuristic_mode)
                f_new = tentative_g + h
                heapq.heappush(open_set, (f_new, tentative_g, v))

    distance = g_score.get(goal, math.inf)
    path = reconstruct_path(parents, start, goal) if distance < math.inf else []
    return path, distance, visited_count
