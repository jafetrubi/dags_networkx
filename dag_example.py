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
G = nx.DiGraph()
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
plt.clf()