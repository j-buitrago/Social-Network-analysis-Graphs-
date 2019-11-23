import networkx as nx
from networkx.readwrite import json_graph
import json
import networkx.algorithms.community as nxComm

with open('../datos/coldplay.json') as f:
    js_graph = json.load(f)
g = nx.Graph(json_graph.node_link_graph(js_graph))

commGreedy = list(nxComm.greedy_modularity_communities(g))

closeness = nx.closeness_centrality(g)
edgebetwenness = nx.edge_betweenness(g)
pagerank = nx.pagerank(g)

idComm = 1
for c in commGreedy:
    for node in c:
        g.nodes[node]['community'] = idComm
        g.nodes[node]['closeness'] = closeness[node]
        g.nodes[node]['pagerank'] = pagerank[node]
    idComm += 1

for edge in edgebetwenness:
    g[edge[0]][edge[1]]['eb'] = edgebetwenness[edge]

json_data = json_graph.node_link_data(g)
with open('../datos/coldplay_proc.json', 'w') as file:
    json.dump(json_data, file, indent='\t')



