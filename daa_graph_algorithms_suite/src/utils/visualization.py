"""
Visualization and output utilities
"""

import json
from typing import Any, Dict, List
from tabulate import tabulate
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False


def export_to_json(data: Any, filename: str) -> None:
    """Export data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, default=str)


def print_results(title: str, data: Dict[str, Any], color: bool = True) -> None:
    """Print formatted results"""
    if COLORS_AVAILABLE and color:
        print(f"\n{Fore.CYAN}{'=' * 60}")
        print(f"{Fore.GREEN}{title}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
    else:
        print(f"\n{'=' * 60}")
        print(title)
        print('=' * 60)
    
    for key, value in data.items():
        if isinstance(value, float):
            print(f"{key}: {value:.6f}")
        elif isinstance(value, list) and len(value) > 10:
            print(f"{key}: [{value[0]}, {value[1]}, ..., {value[-1]}] (length: {len(value)})")
        else:
            print(f"{key}: {value}")


def print_table(headers: List[str], rows: List[List[Any]], title: str = None) -> None:
    """Print formatted table"""
    if title:
        if COLORS_AVAILABLE:
            print(f"\n{Fore.CYAN}{title}{Style.RESET_ALL}")
        else:
            print(f"\n{title}")
    
    print(tabulate(rows, headers=headers, tablefmt='grid'))


def print_path(path: List[int], cost: float = None) -> None:
    """Print a path in a readable format"""
    path_str = " -> ".join(map(str, path))
    
    if COLORS_AVAILABLE:
        print(f"{Fore.YELLOW}Path: {Fore.WHITE}{path_str}{Style.RESET_ALL}")
        if cost is not None:
            print(f"{Fore.YELLOW}Cost: {Fore.WHITE}{cost:.2f}{Style.RESET_ALL}")
    else:
        print(f"Path: {path_str}")
        if cost is not None:
            print(f"Cost: {cost:.2f}")


def print_graph_info(graph) -> None:
    """Print graph information"""
    info = {
        'Type': str(graph),
        'Vertices': graph.get_vertex_count(),
        'Edges': graph.get_edge_count(),
        'Directed': graph.directed,
        'Weighted': graph.weighted
    }
    
    print_results("Graph Information", info)


def format_time(seconds: float) -> str:
    """Format time in human-readable format"""
    if seconds < 0.001:
        return f"{seconds * 1000000:.2f} μs"
    elif seconds < 1:
        return f"{seconds * 1000:.2f} ms"
    else:
        return f"{seconds:.2f} s"


def format_memory(mb: float) -> str:
    """Format memory in human-readable format"""
    if mb < 1:
        return f"{mb * 1024:.2f} KB"
    else:
        return f"{mb:.2f} MB"
