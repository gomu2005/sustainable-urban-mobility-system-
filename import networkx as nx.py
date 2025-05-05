import networkx as nx
import matplotlib.pyplot as plt

# Define sustainability weights (lower is better)
SUSTAINABILITY_WEIGHTS = {
    'walk': 1,      # most sustainable
    'bike': 1.5,
    'bus': 2,
    'train': 2.5,
    'car': 5        # least sustainable
}

# Create a directed graph
G = nx.DiGraph()

# Add nodes (locations in the city)
locations = ['Home', 'Bus Stop', 'Train Station', 'Workplace', 'Market', 'Park', 'Cafe']
G.add_nodes_from(locations)

# Define edges: (from, to, mode, distance_km)
routes = [
    ('Home', 'Bus Stop', 'walk', 0.5),
    ('Bus Stop', 'Train Station', 'bus', 2.0),
    ('Train Station', 'Workplace', 'train', 5.0),
    ('Home', 'Park', 'bike', 1.0),
    ('Park', 'Workplace', 'walk', 1.2),
    ('Home', 'Market', 'car', 3.0),
    ('Market', 'Workplace', 'car', 2.5),
    ('Home', 'Cafe', 'walk', 0.7),
    ('Cafe', 'Workplace', 'bus', 1.5),
]

# Add edges with computed sustainability weight
for from_node, to_node, mode, distance in routes:
    weight = distance * SUSTAINABILITY_WEIGHTS[mode]
    G.add_edge(from_node, to_node, weight=weight, mode=mode, distance=distance)

# Find the most sustainable path
start, end = 'Home', 'Workplace'
path = nx.shortest_path(G, source=start, target=end, weight='weight')
total_weight = nx.shortest_path_length(G, source=start, target=end, weight='weight')

# Print the result
print(f"\nMost sustainable path from {start} to {end}:\n")
for i in range(len(path) - 1):
    edge = G[path[i]][path[i+1]]
    print(f"{path[i]} -> {path[i+1]} via {edge['mode']} (distance={edge['distance']} km, weight={edge['weight']:.2f})")

print(f"\nTotal sustainability weight: {total_weight:.2f}\n")

# Visualize the network
pos = nx.spring_layout(G, seed=1)
edge_labels = {(u, v): f"{d['mode']} ({d['weight']:.1f})" for u, v, d in G.edges(data=True)}

nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_weight='bold')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
nx.draw_networkx_edges(G, pos, width=2, arrows=True)
plt.title("Sustainable Urban Mobility Network")
plt.show()
