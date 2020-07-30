import sys
from constant import *
import queue
from dataclasses import dataclass, field
from typing import Any


class Node:
    """
    Node of a graph

    Attributes:
        x (arg, int): x coord of node
        y (arg, int): y coord of node
        edge (dictionary): dictionary with neighbours as keys
                            and their edge weights as values
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.edges = {}


@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any = field(compare=False)


class Graph:
    """
    Graph representing map

    Atrributes:
        nodes (dictionary): dictionary with node coord as key and 
                            node object as value
        walls (dictionary): dictionary with wall coord as key and
                            value of wall as value
    """

    def __init__(self):
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
        for y in range(map_data.tileheight):
            for x in range(map_data.tilewidth):
                if (not map[y][x] == WALL):
                    self.nodes[(x, y)] = (Node(x, y))
                else:
                    self.walls[(x, y)] = map[y][x]

    def neighbour(self):
        """
        Adds edges to all nodes with edge weight of 1
        """
        dirs = [[-1, 0], [1, 0], [0, -1], [0, 1],
                [-1, -1], [1, -1], [-1, 1], [1, 1]]
        for node in self.nodes.values():
            for dir in dirs:
                neighbour = (node.x + dir[0], node.y + dir[1])
                if (neighbour in self.nodes):
                    node.edges[neighbour] = 1

    def bfs(self, start, goal):
        """
        BFS traversal of graph.
        Start at start and end at goal

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

    def dijkstra(self, start, goal):
        """
        Dijkstra's shortest path traversal of graph. 
        Start at start and end at goal

        Visited is dictionary of nodes and previous node
        Current Cost is dictionary of lowest cost to a node

        Args:
            start ((int, int)): start coord of dijkstra's shorest path
            goal ((int, int)): goal of dijkstra's shorest path

        Returns:
            visited (dictionary): dictionary of path of nodes
                to goal and the previous node
        """
        if (goal not in self.nodes):
            return
        visiting = queue.PriorityQueue()
        visiting.put(PrioritizedItem(0, self.nodes[start]))
        visited = {}
        current_cost = {}
        visited[start] = None
        current_cost[start] = 0

        while not visiting.empty():
            node = visiting.get().item

            if (node.x, node.y) == goal:
                break

            for next in node.edges:
                new_cost = current_cost[(node.x, node.y)] + node.edges[next]
                if next not in current_cost or new_cost < current_cost[next]:
                    current_cost[next] = new_cost
                    visiting.put(PrioritizedItem(new_cost, self.nodes[next]))
                    visited[next] = (node.x, node.y)

        return visited

    def a_star(self, start, goal):
        """
        A* search of graph. Start at start and end at goal

        Visited is dictionary of nodes and previous node
        Current Cost is dictionary of lowest cost to a node

        Args:
            start ((int, int)): start coord of A* 
            goal ((int, int)): goal of A*

        Returns:
            visited (dictionary): dictionary of path of nodes
                to goal and the previous node
        """
        if (goal not in self.nodes):
            return
        visiting = queue.PriorityQueue()
        visiting.put(PrioritizedItem(0, self.nodes[start]))
        visited = {}
        current_cost = {}
        visited[start] = None
        current_cost[start] = 0

        while not visiting.empty():
            node = visiting.get().item

            if (node.x, node.y) == goal:
                break

            for next in node.edges:
                new_cost = current_cost[(node.x, node.y)] + node.edges[next]
                if next not in current_cost or new_cost < current_cost[next]:
                    current_cost[next] = new_cost
                    visiting.put(PrioritizedItem(new_cost + _distance(next, goal), self.nodes[next]))
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


def _distance(coord1, coord2):
    """
    Returns distance between nodes using diagonal distance

    D1 is cost of moving vertically and horizontally
    D2 is cost of moving diagonally
    
    Taken from:
        https://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html#diagonal-distance

    Arg:
        coord1 ((int,int)): First coord to compute distance between
        coord2 ((int,int)): Second coord to compute distance between

    Returns:
        Distance between coord1 and coord2 using diagonal distance
    """
    D1 = 1
    D2 = 1
    dx = abs(coord1[0] - coord2[0])
    dy = abs(coord1[1] - coord2[1])
    return D1 * (dx + dy) + (D2 - 2 * D1) * min(dx, dy)


def auto_path(game, graph):
    """
    Automatically move the player to the
    closest unseen tile

    Args:
        game (Game): Game with game data
        graph (Graph): Graph with nodes
    """
    start, goal = _find_closest_tile(game)
    visited = graph.bfs(start, goal)
    if (visited):
        game.auto_move_player(start, goal, visited)


def _find_closest_tile(game):
    """
    Find closest unseen_tile from player

    Closest tile is by distance, not amount of
    tiles walked to get to it

    Args:
        game (Game): Game with all game data

    Returns:
        p_coord ((int, int)): player's coordinate (start)
        closest_unseen_tile ((int, int)): closest unseen tile (goal)
    """
    closest_unseen_tile = None
    closest_distance = sys.maxsize
    p_coord = (game.player.x, game.player.y)
    # Find the closest (by literal distance, not
    # how many steps it would take) unseen tile
    for tile in game.map_data.unseen_tiles:
        dist = _distance(p_coord, tile)
        if (closest_distance > dist):
            closest_distance = dist
            closest_unseen_tile = tile
    return p_coord, closest_unseen_tile

