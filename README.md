# heuristic_intelligence_dijkstra_astar

## Overview

This project implements and compares **Dijkstra’s Algorithm** and the **A\* Search Algorithm** on large real-world road network graphs. The main goal is to analyze how these two shortest-path algorithms behave in terms of:

- Runtime performance (milliseconds)
- Number of visited (expanded) nodes
- Memory usage (MB)
- Path length and total distance

The implementation is fully from scratch (no built-in shortest path functions) and is designed to work with large graph datasets such as **roadNet-CA** and **roadNet-TX** from the Stanford SNAP collection.  
When coordinate information is available (e.g., OSM-based data), A\* can use Euclidean or Manhattan distance as a heuristic. When no coordinates are available, A\* falls back to **h(n) = 0**, which theoretically degenerates to Dijkstra.

This repository was developed as part of **COP3530 – Data Structures and Algorithms** (Project 3).

---

## Features

- From-scratch implementations of:
  - **Dijkstra’s Algorithm**
  - **A\* Search** with pluggable heuristic (Euclidean / Manhattan / trivial)
- Common graph API using `networkx.Graph`
- Support for multiple large datasets:
  - `roadNet-CA` (California road network, SNAP)
  - `roadNet-TX` (Texas road network, SNAP)
  - `OSM-Florida` (optional, if user provides files)
- Benchmarking utilities:
  - Runtime (ms)
  - Number of visited nodes
  - Approximate memory usage (MB) using `psutil`
- Command-line interface:
  - Dataset selection
  - Start/goal node input
  - Choose algorithm or compare both (Dijkstra vs A\*)
- Clear textual summary of results:
  - Per-algorithm metrics table
  - Path length and total distance

---

## Project Structure

```text
.
├── algorithms.py      # Dijkstra and A* implementations + heuristic function
├── benchmark.py       # Benchmark runner (time, memory, visited count)
├── graph_loader.py    # Dataset configuration and graph loading utilities
├── main.py            # Command-line interface and main program loop
└── README.md          # Project documentation (this file)
```

## Install
~~~
pip install -r requirements.txt
~~~


## Run
~~~
python main.py
~~~


```text
--------------------------------------------------------
| Pathfinding Comparison Interface                     |
--------------------------------------------------------

Available Datasets:
  (1) roadNet-CA
  (2) roadNet-TX
  (3) OSM-Florida
Select Dataset [1-3]:
```

- Enter a dataset number (e.g., 1 for roadNet-CA).

```text
Selected Dataset: [roadNet-CA]

Loading graph... (this may take some time)
Loaded 'roadNet-CA' with 1965206 nodes and 2766607 edges.
Note: No coordinate information found. A* will fall back to h(n)=0 (equivalent to Dijkstra).
```

- Enter start and goal nodes

```text
----------------------------------------
Enter Start Node: 1
Enter End Node: 100
```

- Select algorithm and action

```txt
Select Algorithm:
  (1) Dijkstra
  (2) A*
Choice [1-2]: 1

Options:
  [R] Run selected algorithm
  [C] Compare both algorithms
  [E] Exit
Select action [R/C/E]: C
```

- view results

```txt
Running Dijkstra and A* for comparison...
--------------------------------------------------------
Results
--------------------------------------------------------
Algorithm  |  Time (ms) | Visited Nodes |   Mem (MB)
--------------------------------------------------------
Dijkstra   |     332.43 |       207636 |      36.05
A*         |     400.80 |       207636 |       8.50
--------------------------------------------------------
Dijkstra found a path with length 109 and total distance 108.00.
A* found a path with length 109 and total distance 108.00.
```