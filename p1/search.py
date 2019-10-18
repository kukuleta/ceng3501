import pdb
import sys
class Edge:
    def __init__(self, name, node1, node2, length):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.length = length


class Graph:
    def __init__(self, edgesdict=None):
        if edgesdict:
            self.edges = [Edge(e['NAME'], e['NODE1'], e['NODE2'], e['VAL']) for e in edgesdict]

    def get_connected_nodes(self, node):
        result = [x.node2 for x in self.edges if x.node1 == node]
        ##result += [x.node1 for x in self.edges if x.node2 == node]
        return sorted(result)

    def get_edge(self, node1, node2):
        node_names = (node1, node2)
        for edge in self.edges:
            if ((edge.node1, edge.node2) == node_names or
                    (edge.node2, edge.node1) == node_names):
                return edge
        return None


def get_edge_name(current_num_of_edges):
    return "e" + str(current_num_of_edges + 1)

def path_length(Graph,node_names):
        distance_traveled = 0
        start_node = node_names[0]
        for nextNode in node_names[1:]:
            distance_traveled += Graph.get_edge(start_node, nextNode).length
            start_node = nextNode
        return distance_traveled
edgesdict=[]

with open(sys.argv[1]) as f:
    lines = f.read().split("\n")

for i in lines:
    parent_node = i[0:1]
    edge_dict = dict(zip(list(i[3::5]),list(i[5::5])))
    edges = [edge for edge in edge_dict.items() if int(edge_dict.get(edge[0])) != 0]
    for edge in edges:
        y ={"NAME": get_edge_name(len(edgesdict)), "VAL": int(edge[1]), "NODE1": parent_node , "NODE2": edge[0]}
        edgesdict.append(y)

Graph = Graph(edgesdict=edgesdict)


def is_node_deadEnd(graph,Node):
    if len(graph.get_connected_nodes(Node)) == 1:
        return True
    else:
        return False

start = input("Please enter the start state ")
goal = input("Please enter the goal state ")

def bfs(graph, start, goal):
    if start == goal:
        print("Give different goal input")
    else:
        closed_nodes = set()
        extended_paths = [[start]]
        path_to_extend = [[start]]
        while extended_paths != []:
            for path in path_to_extend:
                closed_nodes.update({closed_node for closed_node in path})
                for adjacentNodes in graph.get_connected_nodes(path[-1]):
                    if is_node_deadEnd(graph, adjacentNodes) and adjacentNodes != goal:
                        extended_paths.pop()
                    elif adjacentNodes not in closed_nodes and not is_node_deadEnd(graph,adjacentNodes):
                        path.append(adjacentNodes)
                        extended_paths.append(path.copy())
                        path.pop()
                path_removed = extended_paths.pop(0)
                if path_removed[-1] == goal:
                    return "BFS : {path}".format(path=path_removed)
                closed_nodes.clear()
            path_to_extend = extended_paths
        return "Not found"

def dfs(graph, start, goal):
    if start == goal:
        print("Give different goal input")
    else:
        closed_nodes = set()
        extended_paths = [[start]]
        path_to_extend = [start]
        while extended_paths != []:
            closed_nodes.update({closed_node for closed_node in path_to_extend})
            for adjacentNodes in graph.get_connected_nodes(path_to_extend[-1]):
                """if is_node_deadEnd(graph, adjacentNodes) and adjacentNodes != goal:
                    extended_paths.pop()"""
                if adjacentNodes not in closed_nodes and not is_node_deadEnd(graph,adjacentNodes):
                    path_to_extend.append(adjacentNodes)
                    extended_paths.append(path_to_extend.copy())
                    path_to_extend = path_to_extend[:-1]
            path_last_explored = extended_paths.pop()
            if path_last_explored[-1] == goal:
                return "DFS : {path}".format(path=path_last_explored)
            path_to_extend = path_last_explored
            closed_nodes.clear()
        return "Not found"

def ucs(graph, start, goal):
    if start == goal:
        print("Give different goal input")
    else:
        closed_nodes = set()
        extended_paths = [[start]]
        path_to_extend = [start]
        while extended_paths != []:
            path_last_explored = extended_paths.pop(0)
            if path_last_explored[-1] == goal:
                return "UCS : {path}".format(path=path_last_explored)
            closed_nodes.update({closed_node for closed_node in path_to_extend})
            for adjacentNodes in graph.get_connected_nodes(path_to_extend[-1]):
                #if adjacentNodes not in closed_nodes and \
                if not is_node_deadEnd(graph, adjacentNodes):
                    path_to_extend.append(adjacentNodes)
                    extended_paths.append(path_to_extend.copy())
                    path_to_extend = path_to_extend[:-1]
            extended_paths = sorted(extended_paths,key=lambda path: path_length(Graph,path))
            path_to_extend = extended_paths[0]
            closed_nodes.clear()
        return "Not found"

print(bfs(Graph,start,goal))
print(dfs(Graph,start,goal))
print(ucs(Graph,start,goal))