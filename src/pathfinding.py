from constant import *
import queue

class Node:
    """
    Node of a graph

    Attributes:
        x (arg, int): x coord of node
        y (arg, int): y coord of node
        edge (dictionary): dictionary with neighbours as keys
                            and their edge weights as values
    """
    def __init__ (self, x, y):
        self.x = x
        self.y = y
        self.edges = {}

class Graph:
    """
    Graph representing map

    Atrributes:
        nodes (dictionary): dictionary with node coord as key and 
                            node object as value
        walls (dictionary): dictionary with wall coord as key and
                            value of wall as value
    """
    def __init__ (self):
        self.nodes = {}
        self.walls = {}

    def make_graph(self, map, map_data):
        """
        Makes graph corresponding to map

        Makes a node if corresponding point on map isn't wall

        Args:
            map (2D array): 2D array representing map
            map_data (MapInfo): arg that holds map info
        """
        for y in range (map_data.tileheight):
            for x in range (map_data.tilewidth):
                if (not map[y][x] == WALL):
                    self.nodes[(x,y)] = (Node(x,y))
                else:
                    self.walls[(x,y)] = map[y][x]                    
    
    def neighbour(self):
        """
        Adds edges to all nodes with edge weight of 1
        """
        dirs = [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1],
                [1, -1], [-1, 1], [1, 1]]
        for node in self.nodes.values():
            for dir in dirs:
                neighbour = (node.x + dir[0], node.y + dir[1])
                if (neighbour in self.nodes):
                    node.edges[neighbour] = 1


    def bfs(self, start, goal):
        """
        BFS traversal of graph

        Visited is a dictionary of nodes and the previous node

        Args:
            start ((int, int)): start coord of bfs
            goal ((int, int)): goal of bfs

        Returns:
            visited (dictionary): dictionary of path of nodes
                                    to goal and the previous node
        """
        if (goal not in self.nodes):
            return
        visiting = queue.Queue()
        visiting.put(self.nodes[start])
        visited = {}
        visited[start] = None

        while not visiting.empty():
            node = visiting.get()

            if (node.x, node.y) == goal:
                break

            for next in node.edges:
                if next not in visited:
                    visiting.put(self.nodes[next])
                    visited[next] = (node.x, node.y)

        return visited


    def find_path(self, start, goal, visited):
        path = []
        current = goal
        while not current == start:
            path.append(current)
            current = visited[current]
        # path.append(start)
        path.reverse()
        return path

