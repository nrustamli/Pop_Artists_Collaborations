import json
import networkx as nx
import matplotlib.pyplot as plt

# Load data from JSON file
with open('collaborations_all.json', 'r') as file:
    data = json.load(file)

# Create a graph
G = nx.Graph()

# Add edges based on collaborations
for entry in data:
    artists = entry["Artists"].split(", ")
    for i, artist1 in enumerate(artists):
        for artist2 in artists[i + 1:]:
            G.add_edge(artist1, artist2, song=entry["Song Title"], year=entry["Year"], country=entry["Country"])

# Draw the graph with improvements
plt.figure(figsize=(12, 12))

# Use Kamada-Kawai layout for better clustering
pos = nx.kamada_kawai_layout(G)

# Draw nodes and edges
nx.draw_networkx_nodes(G, pos, node_size=140, node_color="lightblue", alpha=0.9, edgecolors="black")
nx.draw_networkx_edges(G, pos, alpha=0.3, width=1.2)
nx.draw_networkx_labels(G, pos, font_size=5, font_color="black")

# Annotate only a subset of edges with song titles to avoid clutter
edge_labels_subset = {edge: G.edges[edge]["song"] for edge in list(G.edges)[:10]}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_subset, font_size=0, label_pos=0.5)

#Get the number of nodes and edges
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()

# Display the number of nodes and edges
print(f"Number of nodes: {num_nodes}")
print(f"Number of edges: {num_edges}")

# Show plot with simplified design
plt.title("Pop Song Collaboration Network ", fontsize=16)
plt.axis("off")
plt.show()
