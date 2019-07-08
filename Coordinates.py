import pandas as pd
import math
import networkx as nx
import matplotlib.pyplot as plt

# Calculates a distance between two cities using their coordinates
def dist(la_f, lo_f, la_s, lo_s):
    return int(1000 * 6371 * math.pi / 180 * math.sqrt((la_f - la_s)**2 + (math.cos(math.radians((la_f + la_s)/2)) * (lo_f - lo_s))**2))


def prim(g):
    ans = list()
    total_dist = 0
    INF = 10**10
    used = list()
    min_e = list()
    sel_e = list()
    for i in range(len(g)-1):
        used.append(False)
        min_e.append(INF)
        sel_e.append(-1)
    min_e[0] = 0
    for i in range(len(g)-1):
        v = -1
        for j in range(len(g)-1):
            if not used[j] and (v == -1 or min_e[j] < min_e[v]):
                v = j

        used[v] = True
        if sel_e[v] != -1:
            ans.append([v, sel_e[v]])
            total_dist += g[v+1][sel_e[v]+1]
        for to in range(len(g)-1):
            if v != to and g[v+1][to+1] < min_e[to]:
                min_e[to] = g[v+1][to+1]
                sel_e[to] = v

    return total_dist, ans


data = pd.read_csv("Malta.csv", sep=';')
coord = data[['Latitude', 'Longitude']]
g = list()
g.append(list())
g[0].append(' ')
for j in range(len(data)):
    g[0].append(data.at[j, 'AccentCity'])

for i in range(len(data)):
    g.append(list())
    g[i+1].append(data.at[i, 'AccentCity'])
    for j in range(len(data)):
        g[i+1].append(dist(coord.iloc[i, 0], coord.iloc[i, 1], coord.iloc[j, 0], coord.iloc[j, 1]))

# Creates output.csv file with the matrix of distances

#outp = pd.DataFrame(g)
#outp.to_csv("output.csv", sep='\t')

tot_dist, MST = prim(g)
print(tot_dist)
for item in MST:
    print(item)

# Creates a graph
gra = nx.Graph()
gra.add_edges_from(MST)
nx.draw(gra, with_labels=True)
plt.show()
