# benchmark.py

import os
import time
from typing import Callable, Dict, Any, Hashable, Tuple

import networkx as nx

import algorithms

try:
    import psutil
except ImportError:
    psutil = None  # psutil이 없으면 메모리 측정은 None 처리


def measure_algorithm(
    func: Callable[[], Tuple],
) -> Dict[str, Any]:
    """
    func() 는 (path, distance, visited_count) 를 반환한다고 가정.
    """
    process = psutil.Process(os.getpid()) if psutil is not None else None
    mem_before = (
        process.memory_info().rss if process is not None else None
    )

    t0 = time.perf_counter()
    path, distance, visited_count = func()
    t1 = time.perf_counter()

    mem_after = (
        process.memory_info().rss if process is not None else None
    )

    time_ms = (t1 - t0) * 1000.0
    if mem_before is not None and mem_after is not None:
        mem_mb = (mem_after - mem_before) / (1024 ** 2)
    else:
        mem_mb = None

    return {
        "time_ms": time_ms,
        "memory_mb": mem_mb,
        "path": path,
        "distance": distance,
        "visited": visited_count,
    }


def run_dijkstra(
    graph: nx.Graph,
    start: Hashable,
    goal: Hashable,
) -> Dict[str, Any]:
    return measure_algorithm(
        lambda: algorithms.dijkstra(graph, start, goal)
    )


def run_astar(
    graph: nx.Graph,
    start: Hashable,
    goal: Hashable,
    heuristic_mode: str = "euclidean",
) -> Dict[str, Any]:
    return measure_algorithm(
        lambda: algorithms.astar(graph, start, goal, heuristic_mode)
    )
