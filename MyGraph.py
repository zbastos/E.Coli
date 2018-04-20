class MyGraph:

    def __init__(self, g={}):
        self.g = g


    def print_graph(self):
        [print (node, " --> " ,self.g[node]) for node in self.g.keys()]

    def get_nodes(self):
        return list(self.g.keys())

    def get_edges(self):
        return [(o, d) for o, nodes_dest in self.g.items() for d in nodes_dest]

    def add_node(self, node):
        if node not in self.g.keys():
            self.g[node]=[]

    def add_edge(self, orig, dest):
        if orig not in self.g.keys():
            self.add_node(orig)
        if dest not in self.g.keys():
            self.add_node(dest)
        if dest not in self.g[orig]:
            self.g[orig].append(dest)

    def get_successors(self, node):
        return list(self.g[node])


    def get_predecessors(self, node):
        return [node_orig for node_orig, nodes_dest in self.g.items() if node in nodes_dest]

    def get_adjacents(self, node):
        s = self.get_successors(node)
        p = self.get_predecessors(node)
        return list(set(s+p))

    def out_degree(self, node):
        return len(self.g[node])

    def in_degree(self, node):
        return len(self.get_predecessors(node))

    def degree(self, node):
        return len(self.get_adjacents(node))

    def reachableBFS (self, node):
        to_visit = [node]
        res=[]
        while to_visit:
            actual_node = to_visit.pop(0) #index required to remove the first element of the list
            if node!= actual_node : res.append(actual_node)
            to_visit.extend([elem for elem in self.g[actual_node] if elem not in res and elem not in to_visit])
        return res

    def reachableDFS (self, node):
        to_visit = [node]
        res = []
        while to_visit:
            actual_node = to_visit.pop(0)
            if node!= actual_node : res.append(actual_node)
            aux = [elem for elem in self.g[actual_node] if elem not in res and elem not in to_visit]
            to_visit = aux + to_visit
        return res


    def distance(self, orig, dest):
        if orig == dest: return 0
        l = [(orig, 0)]
        visited = [orig]
        while l:
            actual_node, dist = l.pop(0)
            for elem in self.g[actual_node]:
                if elem == dest:
                    return dist + 1
                elif elem not in visited:
                    l.append((elem, dist + 1))
                    visited.append(elem)
        return float("inf")


    def shortest_path(self, orig, dest):
        if orig == dest: return []
        l = [(orig, [])]
        visited = []
        while l:
            actual_node, path = l.pop(0)
            for elem in self.g[actual_node]:
                if elem == dest:
                    return [orig] + path + [elem]
                elif elem not in visited:
                    l.append((elem, path + [elem]))
                    visited.append(elem)
        return None


    def reachable_with_dist(self, node):
        res = []
        l = [(node, 0)]
        while len(l) > 0:
            actual_node, dist = l.pop(0)
            if actual_node != node: res.append((actual_node, dist))
            for elem in self.g[actual_node]:
                if elem not in [x[0] for x in l + res]:
                    l.append((elem, dist + 1))
        return res

    def node_has_cycle(self, node):
        l = [node]
        res = False
        visited = [node]
        while l:
            actual_node = l.pop()
            for elem in self.g[actual_node]:
                if elem == node: return True
                elif elem not in visited:
                    l.append(elem)
                    visited.append(elem)
        return res

    def has_cycle(self):
        #return any ([self.nodeHasCycle(v) for v in self.g.keys()])   # menos eficiente porque calcula para todo os v
        for v in self.g.keys():
            if self.node_has_cycle(v): return True
        return False

if __name__ == "__main__":
    gr = MyGraph({1: [2], 2: [3], 3: [2, 4], 4: [2]})
    gr.print_graph()
    print(gr.get_edges())
    print(gr.get_nodes())

    gr2 = MyGraph()
    gr2.add_node(1)
    gr2.add_node(2)
    gr2.add_node(3)
    gr2.add_node(4)

    gr2.add_edge(1,2)
    gr2.add_edge(2,3)
    gr2.add_edge(3,2)
    gr2.add_edge(3,4)
    gr2.add_edge(4,2)

    gr2.print_graph()
    print (gr.get_successors(2))
    print (gr.get_predecessors(2))
    print (gr.get_adjacents(2))
    print (gr.in_degree(2))
    print (gr.out_degree(2))
    print (gr.degree(2))

    #grafos travessia
    print("travessia")
    gr2 = MyGraph({1: [2, 3], 2: [4], 3: [5], 4: [], 5: []})
    print(gr2.reachableBFS(1))
    print(gr2.reachableDFS(1))

    print("shortest_path")
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    print (gr.shortest_path(1,4))
    print (gr.shortest_path(4,3))

    print("shortest_path")
    gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
    print (gr2.shortest_path(1,5))
    print (gr2.shortest_path(2,1))

    print ("reachable_with_dist")
    gr = MyGraph({1: [2], 2: [3], 3: [2, 4], 4: [2]})
    print(gr.reachable_with_dist(1))
    print(gr.reachable_with_dist(3))

    gr2 = MyGraph({1: [2, 3], 2: [4], 3: [5], 4: [], 5: []})
    print(gr2.reachable_with_dist(1))
    print(gr2.reachable_with_dist(5))

    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    print (gr.node_has_cycle(2))
    print (gr.node_has_cycle(1))
    print (gr.has_cycle())

    gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
    print (gr2.node_has_cycle(1))
    print (gr2.has_cycle())
