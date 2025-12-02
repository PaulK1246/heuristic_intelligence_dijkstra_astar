# main.py

from typing import Dict, Any, Hashable

import networkx as nx

from graph_loader import load_graph
from benchmark import run_dijkstra, run_astar


DATASET_OPTIONS = ["roadNet-CA", "roadNet-TX", "OSM-Florida"]


def print_header() -> None:
    print("-" * 56)
    print("| Pathfinding Comparison Interface".ljust(55) + "|")
    print("-" * 56)


def select_dataset() -> str:
    print("\nAvailable Datasets:")
    for idx, name in enumerate(DATASET_OPTIONS, start=1):
        print(f"  ({idx}) {name}")
    while True:
        choice = input("Select Dataset [1-{}]: ".format(len(DATASET_OPTIONS))).strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(DATASET_OPTIONS):
                dataset_name = DATASET_OPTIONS[idx - 1]
                print(f"\nSelected Dataset: [{dataset_name}]")
                return dataset_name
        print("Invalid selection. Please try again.")


def get_node_input(prompt: str) -> Hashable:
    while True:
        value = input(prompt).strip()
        if value == "":
            print("Input cannot be empty.")
            continue
        # 기본적으로 int로 시도, 아니면 문자열로 사용
        try:
            return int(value)
        except ValueError:
            return value


def print_results_table(results: Dict[str, Dict[str, Any]]) -> None:
    print("-" * 56)
    print("Results")
    print("-" * 56)
    header = "{:<10} | {:>10} | {:>12} | {:>10}".format(
        "Algorithm", "Time (ms)", "Visited Nodes", "Mem (MB)"
    )
    print(header)
    print("-" * 56)
    for algo_name, metrics in results.items():
        time_ms = metrics["time_ms"]
        visited = metrics["visited"]
        mem_mb = metrics["memory_mb"]
        mem_str = f"{mem_mb:.2f}" if mem_mb is not None else "N/A"
        row = "{:<10} | {:>10.2f} | {:>12d} | {:>10}".format(
            algo_name, time_ms, visited, mem_str
        )
        print(row)
    print("-" * 56)


def main() -> None:
    print_header()

    dataset_name = select_dataset()
    print("\nLoading graph... (this may take some time)")
    graph, meta = load_graph(dataset_name)
    print(
        f"Loaded '{meta['name']}' with "
        f"{meta['num_nodes']} nodes and {meta['num_edges']} edges."
    )
    if not meta["has_coords"]:
        print(
            "Note: No coordinate information found. "
            "A* will fall back to h(n)=0 (equivalent to Dijkstra)."
        )

    while True:
        print("\n----------------------------------------")
        start = get_node_input("Enter Start Node: ")
        goal = get_node_input("Enter End Node: ")

        if start not in graph or goal not in graph:
            print("Either the start or end node does not exist in the graph.")
            continue

        print("\nSelect Algorithm:")
        print("  (1) Dijkstra")
        print("  (2) A*")
        algo_choice = input("Choice [1-2]: ").strip()

        print("\nOptions:")
        print("  [R] Run selected algorithm")
        print("  [C] Compare both algorithms")
        print("  [E] Exit")
        action = input("Select action [R/C/E]: ").strip().lower()

        if action == "e":
            print("Exiting...")
            break

        results = {}

        if action == "r":
            if algo_choice == "1":
                print("\nRunning Dijkstra...")
                results["Dijkstra"] = run_dijkstra(graph, start, goal)
            elif algo_choice == "2":
                print("\nRunning A*...")
                # 기본은 Euclidean, 필요하면 main에서 변경 가능
                results["A*"] = run_astar(graph, start, goal, heuristic_mode="euclidean")
            else:
                print("Invalid algorithm selection.")
                continue

        elif action == "c":
            print("\nRunning Dijkstra and A* for comparison...")
            results["Dijkstra"] = run_dijkstra(graph, start, goal)
            results["A*"] = run_astar(graph, start, goal, heuristic_mode="euclidean")

        else:
            print("Invalid action.")
            continue

        print_results_table(results)

        # path 길이와 거리 간단 표기(원하면 더 자세히)
        for algo_name, metrics in results.items():
            path = metrics["path"]
            distance = metrics["distance"]
            if path:
                print(
                    f"{algo_name} found a path with length {len(path)} "
                    f"and total distance {distance:.2f}."
                )
            else:
                print(f"{algo_name} could not find a path between the given nodes.")


if __name__ == "__main__":
    main()
