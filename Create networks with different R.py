import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
import os

def create_lattice(N, neighbor_type):
    G = nx.grid_2d_graph(N, N, periodic=False)
    if neighbor_type == 8:
        G.add_edges_from(((x, y), (x+1, y+1)) for x in range(N-1) for y in range(N-1))
        G.add_edges_from(((x+1, y), (x, y+1)) for x in range(N-1) for y in range(N-1))
    return G

def remove_nodes(G, X):
    num_to_remove = int(G.number_of_nodes() * X / 100)
    nodes_to_remove = random.sample(list(G.nodes()), num_to_remove)
    G.remove_nodes_from(nodes_to_remove)
    return G

def reinforce_and_immune_nodes(G, I, R):
    centrality = nx.betweenness_centrality(G)
    top_nodes_count = int(len(G.nodes()) * I / 100)
    reinforced_nodes = sorted(centrality, key=centrality.get, reverse=True)[:top_nodes_count]

    immune_nodes = set()
    for node in reinforced_nodes:
        G.nodes[node]['status'] = 'reinforced'
        immune_nodes.update(nx.single_source_shortest_path_length(G, node, cutoff=R).keys())

    # Apply immune status to all nodes within the radius R
    for node in immune_nodes:
        if 'status' not in G.nodes[node]:
            G.nodes[node]['status'] = 'immune'

    return G, reinforced_nodes, list(immune_nodes)

def plot_initial_map(G, output_path, sim_number):
    pos = {node: (node[1], -node[0]) for node in G.nodes()}
    color_map = ['red' if G.nodes[n].get('status') == 'reinforced' else
                 'blue' if G.nodes[n].get('status') == 'immune' else
                 'green' for n in G.nodes()]
    plt.figure(figsize=(8, 8))
    nx.draw(G, pos, node_color=color_map, with_labels=False, node_size=40)
    plt.savefig(os.path.join(output_path, f'Map({sim_number}).png'))
    plt.close()

def run_simulation(N, X, I, neighbor_type, R, sim_number, output_path):
    G = create_lattice(N, neighbor_type)
    G = remove_nodes(G, X)
    G, reinforced_nodes, immune_nodes = reinforce_and_immune_nodes(G, I, R)
    plot_initial_map(G, output_path, sim_number)

    data_records = []
    iteration = 1
    # Modify to keep reinforced and immune nodes
    nodes_to_consider_for_removal = [node for node in G.nodes() if 'status' not in G.nodes[node]]
    while nodes_to_consider_for_removal:
        node_to_remove = random.choice(nodes_to_consider_for_removal)
        G.remove_node(node_to_remove)
        nodes_to_consider_for_removal.remove(node_to_remove)  # Ensure this node is not considered again
        largest_cluster_size = len(max(nx.connected_components(G), key=len, default=[]))
        record = {
            'Iteration': iteration,
            'Total nodes remaining': len(G.nodes()),
            'Total reinforced nodes remaining': sum(1 for n in G.nodes if G.nodes[n].get('status') == 'reinforced'),
            'Total immune nodes remaining': sum(1 for n in G.nodes if G.nodes[n].get('status') == 'immune'),
            'Largest cluster size': largest_cluster_size
        }
        data_records.append(record)
        iteration += 1

    df = pd.DataFrame(data_records)
    df.to_csv(os.path.join(output_path, f'Data({sim_number}).csv'), index=True)


def main():
    N = 50
    X = 30
    I = 0
    neighbor_type = int(input("Enter neighbor type (4 or 8): "))
    R = int(input("Enter immune radius (R value): "))
    output_path = input("Enter output path: ")
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for j in range(1, 11):  # Run 10 simulations
        run_simulation(N, X, I, neighbor_type, R, j, output_path)
        print(f"Simulation {j} completed and data saved.")

if __name__ == '__main__':
    main()
