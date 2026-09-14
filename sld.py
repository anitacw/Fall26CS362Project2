import numpy as np
import pandas as pd

def build_sld_matrix() -> pd.DataFrame:

# 2D Coordinates (x, y) from the official Russell & Norvig AIMA codebase
    romania_locations = {
        "Arad": (91, 492),
        "Bucharest": (400, 327),
        "Craiova": (253, 288),
        "Drobeta": (165, 299),
        "Eforie": (562, 293),
        "Fagaras": (305, 442),
        "Giurgiu": (375, 270),
        "Hirsova": (534, 350),
        "Iasi": (473, 506),
        "Lugoj": (165, 379),
        "Mehadia": (168, 339),
        "Neamt": (406, 537),
        "Oradea": (131, 571),
        "Pitesti": (320, 368),
        "Rimnicu Vilcea": (233, 410),
        "Sibiu": (207, 457),
        "Timisoara": (94, 410),
        "Urziceni": (456, 350),
        "Vaslui": (509, 444),
        "Zerind": (108, 530),
    }

# Sort cities alphabetically for a clean matrix layout
    cities = sorted(romania_locations.keys())
    n = len(cities)
    matrix = np.zeros((n, n), dtype=int)

    # Calculate Euclidean distance between every city pair
    for i, city1 in enumerate(cities):
        for j, city2 in enumerate(cities):
            x1, y1 = romania_locations[city1]
            x2, y2 = romania_locations[city2]
            distance = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            matrix[i, j] = int(round(distance))

    # Create the pandas DataFrame
    romania_sld_df = pd.DataFrame(matrix, index=cities, columns=cities)

    # Display the DataFrame
    return romania_sld_df
