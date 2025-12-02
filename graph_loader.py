# graph_loader.py

from typing import Dict, Any, Tuple

import networkx as nx


# 이 부분을 네 로컬/클라우드 환경에 맞게 수정하면 됨.
DATASET_CONFIG: Dict[str, Dict[str, Any]] = {
    "roadNet-CA": {
        "edge_list": "data/roadNet-CA.txt",  # SNAP edge list 파일 경로
        "weighted": False,
        "delimiter": "\t",
        "coords": None,  # 예: "data/roadNet-CA-coords.csv"
    },
    "roadNet-TX": {
        "edge_list": "data/roadNet-TX.txt",
        "weighted": False,
        "delimiter": "\t",
        "coords": None,
    },
    "OSM-Florida": {
        "edge_list": "data/osm_florida_edges.txt",
        "weighted": True,   # weight가 있을 수도 있다고 가정
        "delimiter": " ",
        "coords": "data/osm_florida_coords.csv",  # (node_id, x, y)
    },
}


def load_edge_list(
    path: str,
    weighted: bool = False,
    delimiter: str = " ",
) -> nx.Graph:
    """
    단순 edge list 로더.
    형식:
        u v [w]
    주석(# 시작)과 빈 줄은 무시.
    """
    g = nx.Graph()
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(delimiter)
            if len(parts) < 2:
                continue
            u = int(parts[0])
            v = int(parts[1])
            if weighted and len(parts) >= 3:
                w = float(parts[2])
            else:
                w = 1.0
            g.add_edge(u, v, weight=w)
    return g


def attach_positions_from_csv(
    graph: nx.Graph,
    path: str,
    delimiter: str = ",",
    has_header: bool = True,
) -> None:
    """
    CSV 형식:
        node_id, x, y
    """
    import csv

    with open(path, "r") as f:
        reader = csv.reader(f, delimiter=delimiter)
        if has_header:
            next(reader, None)
        for row in reader:
            if len(row) < 3:
                continue
            node_id = int(row[0])
            x = float(row[1])
            y = float(row[2])
            if node_id in graph:
                graph.nodes[node_id]["pos"] = (x, y)


def load_graph(dataset_name: str) -> Tuple[nx.Graph, Dict[str, Any]]:
    """
    dataset_name: "roadNet-CA", "roadNet-TX", "OSM-Florida" 등

    Returns:
        graph: networkx Graph
        meta:  로딩에 사용된 설정 정보
    """
    if dataset_name not in DATASET_CONFIG:
        raise ValueError(f"Unknown dataset: {dataset_name}")

    cfg = DATASET_CONFIG[dataset_name]
    edge_list_path = cfg["edge_list"]
    weighted = bool(cfg.get("weighted", False))
    delimiter = cfg.get("delimiter", " ")

    graph = load_edge_list(edge_list_path, weighted=weighted, delimiter=delimiter)

    coords_path = cfg.get("coords")
    if coords_path:
        attach_positions_from_csv(graph, coords_path)

    meta = {
        "name": dataset_name,
        "num_nodes": graph.number_of_nodes(),
        "num_edges": graph.number_of_edges(),
        "weighted": weighted,
        "has_coords": coords_path is not None,
    }
    return graph, meta
