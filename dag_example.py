import networkx as nx
import matplotlib.pyplot as plt
import random
import requests

# get random work bank
word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

response = requests.get(word_site)
words = response.content.splitlines()

# convert byte into string
words = [word.decode() for word in words]

# append .csv for file-like names
files = [random.choice(words)+'.csv' for i in range(0,4)]

# create data structure for dependencies
dictionary = {}
for file in files:
    dictionary[file] = [random.choice(words) for i in range(0,2)]

# create our edge nodes according to our data structure
G = nx.Graph()
for files,tags in dictionary.items(): # iterating through dictionary items
    for tag in tags:
        G.add_edge(tag,files) # creating relationship between tag and files in our graph
        G.add_edge(random.choice(words),tag) # adding one more layer of dependencies

# create basic graph
nx.draw(G)
plt.show()
plt.clf()

# prettying it up
pos = nx.spring_layout(G,k=0.4)
args = dict(node_size=400,alpha=0.4,font_size=8,with_labels=True,node_color='b')
nx.draw(G, pos, **args)
plt.savefig('G.png',format='PNG') # saving figure to use picture later
plt.show()
plt.clf() # this closes the graph

# shell graph
pos = nx.shell_layout(G)
args = dict(node_size=400,alpha=0.4,font_size=8,with_labels=True,node_color='b')
nx.draw(G, pos, **args)
plt.savefig('G_shell.png',format='PNG') # saving figure to use picture later
plt.show()
plt.clf() # this closes the graph

# create our graph for DAGs
G = nx.DiGraph()
G.add_node('ingest_from_s3.py')
G.add_edge('ingest_from_s3.py','load_from_s3.py')
G.add_edge('load_from_s3.py','validate_data.py')
G.add_edge('load_from_s3.py','clean_data.py')
G.add_edge('clean_data.py','dump_into_snowflake.py')
G.add_edge('validate_data.py','dump_into_snowflake.py')

for layer, nodes in enumerate(nx.topological_generations(G)):
    # `multipartite_layout` expects the layer as a node attribute, so add the
    # numeric layer value as a node attribute
    for node in nodes:
        G.nodes[node]["layer"] = layer

pos = nx.multipartite_layout(G, subset_key="layer")

args = dict(node_size=400,alpha=0.4,font_size=8,with_labels=True,node_color='b',arrows=True)
nx.draw(G, pos, **args)
plt.savefig('G_dag.png',format='PNG') # saving figure to use picture later
plt.show()
plt.clf() # this closes the graph
