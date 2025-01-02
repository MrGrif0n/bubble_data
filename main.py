import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter
import re

# Step 1: Read and preprocess the file
def read_file(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    # Remove punctuation and convert to lowercase
    words = re.findall(r'\b\w+\b', text.lower())
    return words

# Step 2: Count word frequencies and filter
def filter_words(words, threshold=50):
    word_counts = Counter(words)
    filtered_words = {word: count for word, count in word_counts.items() if count > threshold}
    return filtered_words

# Step 3: Generate relationships (naive co-occurrence model)
def build_relationships(words, filtered_words):
    word_set = set(filtered_words.keys())
    relationships = Counter()
    for i, word in enumerate(words):
        if word not in word_set:
            continue
        # Look at the next few words for simplicity
        for neighbor in words[i + 1 : i + 5]:
            if neighbor in word_set:
                relationships[(word, neighbor)] += 1
    return relationships

# Step 4: Create the bubble chain graph
import matplotlib.pyplot as plt
import networkx as nx

def visualize_bubble_chain(filtered_words, relationships):
    G = nx.Graph()

    # Add nodes with size
    for word, size in filtered_words.items():
        G.add_node(word, size=size)

    # Add edges with weight
    for (word1, word2), weight in relationships.items():
        if weight > 5:  # Adjust threshold for meaningful relationships
            G.add_edge(word1, word2, weight=weight)
    
    # Draw the graph
    plt.figure(figsize=(14, 14))
    pos = nx.spring_layout(G, k=0.3)  # Adjust k for spacing
    sizes = [filtered_words[node] * 20 for node in G.nodes()]  # Adjust size scaling
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
    
    nx.draw_networkx_edges(G, pos, alpha=0.3, edge_color="gray", width=[w * 0.1 for w in edge_weights])
    nx.draw_networkx_nodes(G, pos, node_size=sizes, node_color="skyblue", alpha=0.8)
    nx.draw_networkx_labels(G, pos, font_size=8, font_color="black")

    # Add a title
    plt.title("Bubble Chain of Words (Filtered and Enhanced)", fontsize=16)
    plt.axis("off")
    plt.show()

# Main execution
file_path = './src_txt/book.txt'
words = read_file(file_path)
filtered_words = filter_words(words, threshold=50)
relationships = build_relationships(words, filtered_words)
visualize_bubble_chain(filtered_words, relationships)
