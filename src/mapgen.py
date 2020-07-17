import gamemap
import random

class Node:
    def __init__ (self, up_left, down_right, left_child=None, right_child=None):
        self.up_left = up_left
        self.down_right = down_right
        self.room_up_left = None
        self.room_down_right = None
        self.left_child = left_child
        self.right_child = right_child

class Tree:
    def __init__(self, map_array, room_width=10, room_height=10, dist_from_sister_node_min=1, dist_from_sister_node_max=3):
        y_len = len(map_array)
        x_len = len(map_array[0])
        self.root = Node((0, 0), (x_len, y_len))
        self.room_width = room_width
        self.room_height = room_height
        self.dist_from_sister_node_min = dist_from_sister_node_min
        self.dist_from_sister_node_max = dist_from_sister_node_max

    def build_bsp(self):
        if (self.root != None):
            self._split_room(self.root)
        else:
            print("Root is None")

    def _split_room(self, node):
        if (node.down_right[1] - node.up_left[1] < 2 * self.room_height and node.down_right[0] - node.up_left[0] < 2 * self.room_width):
            return node
        elif (node.down_right[1] - node.up_left[1] < 2 * self.room_height):
            self._split_vertical(node)
        elif (node.down_right[0] - node.up_left[0] < 2 * self.room_width):
            self._split_horizontal(node)
        else:
            hor = random.randint(0, 1)
            if (hor == 1):
                self._split_horizontal(node)
            else:
                self._split_vertical(node)

    def make_room(self):
        if (self.root != None):
            self._make_room(self.root)
        else:
            print("Root is None")

    def _make_room(self, node):
        if (node.left_child == None and node.right_child == None):
            ul_x = random.randint(self.dist_from_sister_node_min, self.dist_from_sister_node_max)
            ul_y = random.randint(self.dist_from_sister_node_min, self.dist_from_sister_node_max)
            lr_x = random.randint(self.dist_from_sister_node_min, self.dist_from_sister_node_max)
            lr_y = random.randint(self.dist_from_sister_node_min, self.dist_from_sister_node_max)
            node.room_up_left = (node.up_left[0] + ul_x, node.up_left[1] + ul_y)
            node.room_down_right = (node.down_right[0] - lr_x, node.down_right[1] - lr_y)
        else: 
            self._make_room(node.left_child)
            self._make_room(node.right_child)

    #def build_path(self):


    def _split_horizontal(self, node):
        split_y = random.randint(node.up_left[1] + self.room_height, node.down_right[1] - self.room_height)
        u_x = node.up_left[0]
        u_y = node.up_left[1]
        l_x = node.down_right[0]
        l_y = node.down_right[1]
        node.left_child = Node((u_x, u_y), (l_x, split_y))
        node.right_child = Node((u_x, split_y), (l_x, l_y))
        self._split_room(node.left_child)
        self._split_room(node.right_child)

    def _split_vertical(self, node):
        split_x = random.randint(node.up_left[0] + self.room_width , node.down_right[0] - self.room_width)
        u_x = node.up_left[0]
        u_y = node.up_left[1]
        l_x = node.down_right[0]
        l_y = node.down_right[1]
        node.left_child = Node((u_x, u_y), (split_x, l_y))
        node.right_child = Node((split_x, u_y), (l_x, l_y))
        self._split_room(node.left_child)
        self._split_room(node.right_child)

    def print_tree(self):
        if (self.root != None):
            self._print_tree(self.root)

    def _print_tree(self, node):
        if (node != None):
            self._print_tree(node.left_child)
            self._print_tree(node.right_child)
            print("up_left: " + str(node.up_left) + " , down_right: " + str(node.down_right))
            if (node.room_up_left != None and node.room_down_right != None):
                print("room_up_left: " + str(node.room_up_left) + " , room_down_right: " + str(node.room_down_right))
            print("")



map_array = [[1 for x in range (0, 20)] for y in range (0, 20)]
tree = Tree(map_array)
tree.build_bsp()
tree.make_room()
tree.print_tree()