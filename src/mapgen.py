import gamemap
import random

class Room:
    def __init__(self, up_left, down_right):
        self.up_left = up_left
        self.down_right = down_right

class Node:
    def __init__ (self, up_left, down_right, left_child=None, right_child=None):
        self.up_left = up_left
        self.down_right = down_right
        self.room_up_left = None
        self.room_down_right = None
        self.left_child = left_child
        self.right_child = right_child
        self.split_hor = None 
        self.room_array = []

class Tree:
    def __init__(self, map_array, room_width=10, room_height=10, dist_from_sister_node_min=2, dist_from_sister_node_max=3):
        y_len = len(map_array)
        x_len = len(map_array[0])
        self.root = Node((0, 0), (x_len, y_len))
        self.map_array = map_array
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
            if (hor == 0):
                self._split_horizontal(node)
            else:
                self._split_vertical(node)

    def _split_horizontal(self, node):
        split_y = random.randint(node.up_left[1] + self.room_height, node.down_right[1] - self.room_height)
        u_x = node.up_left[0]
        u_y = node.up_left[1]
        l_x = node.down_right[0]
        l_y = node.down_right[1]
        node.left_child = Node((u_x, u_y), (l_x, split_y))
        node.right_child = Node((u_x, split_y), (l_x, l_y))
        node.split_hor = True
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
        node.split_hor = False
        self._split_room(node.left_child)
        self._split_room(node.right_child)

    def make_room(self):
        if (self.root != None):
            self._make_room(self.root)
        else:
            print("Root is None")

    # TODO: decide if this should return a value or not
    def _make_room(self, node):
        if (node == None):
            return None
        left = self._make_room(node.left_child)
        right = self._make_room(node.right_child)
        # TODO: add array of child rooms to node
        if (left == None and right == None):
            ul_x = random.randint(self.dist_from_sister_node_min, self.dist_from_sister_node_max)
            ul_y = random.randint(self.dist_from_sister_node_min, self.dist_from_sister_node_max)
            lr_x = random.randint(self.dist_from_sister_node_min, self.dist_from_sister_node_max)
            lr_y = random.randint(self.dist_from_sister_node_min, self.dist_from_sister_node_max)
            up_left = (node.up_left[0] + ul_x, node.up_left[1] + ul_y)
            down_right = (node.down_right[0] - lr_x, node.down_right[1] - lr_y)
            node.room_up_left = up_left
            node.room_down_right = down_right
        else:
            ran = random.randint(0, 1)
            if (ran == 0):
                up_left = node.left_child.room_up_left
                down_right = node.left_child.room_down_right
            else:
                up_left = node.right_child.room_up_left
                down_right = node.right_child.room_down_right
            node.room_up_left = up_left
            node.room_down_right = down_right

        for y in range(up_left[1], down_right[1] + 1):
            for x in range(up_left[0], down_right[0] + 1):
                self.map_array[y][x] = 0
 
        node.room_array.append(left)
        node.room_array.append(right)
        node.room_array.append((node.room_up_left, node.room_down_right))
        # room_array.append(node.room_up_left)
        # room_array.append(node.room_down_right)

        return node.room_array


    def build_path(self):
        if (self.root != None):
            self._build_path(self.root)
        else:
            print("Root is None")

    def _build_path(self, node):
        if (node == None):
            return 
        left = self._build_path(node.left_child)
        right = self._build_path(node.right_child)
        if (node.left_child == None and node.right_child == None):
            return
        else:
            # TODO: fix bug where min is large than max
            left_up = node.left_child.room_up_left
            left_down = node.left_child.room_down_right
            right_up = node.right_child.room_up_left
            right_down = node.right_child.room_down_right
            if (node.split_hor):
                # TODO: fix bug where path_max_x is for some reason getting larger of the two values
                print("hor")
                path_min_x = max(left_up[0], right_up[0])
                path_max_x = min(left_down[0], right_down[0])
                print(path_min_x)
                print(path_max_x)
                # TODO: Case where left child's room is lower than right child's room
                if (path_max_x < path_min_x):
                    pass
                path_x = random.randint(path_min_x, path_max_x)
                print(path_x)
                path_ul = (path_x, node.left_child.room_down_right[1] + 1)
                path_lr = (path_x + 1, node.right_child.room_up_left[1])
                print(path_ul)
                print(path_lr)
                print("")

                for y in range(path_ul[1], path_lr[1]):
                    for x in range(path_ul[0], path_lr[0]):
                        self.map_array[y][x] = "."
            else:
                print("ver")
                path_min_y = max(left_up[1], right_up[1])
                path_max_y = min(left_down[1], right_down[1])
                print(path_min_y)
                print(path_max_y)
                # TODO: Case where left child's room is lower than right child's room
                if (path_max_y < path_min_y):
                    pass
                path_y = random.randint(path_min_y, path_max_y)
                print (path_y)  
                path_ul = (node.left_child.room_down_right[0] + 1, path_y)
                path_lr = (node.right_child.room_up_left[0], path_y + 1)
                print(path_ul)
                print(path_lr)
                print("")
            
                for y in range(path_ul[1], path_lr[1]):
                    for x in range(path_ul[0], path_lr[0]):
                        self.map_array[y][x] = "."

            self.print_map()
            print("")

    
    def find_closest_room(self, left_child, right_child):
        pass


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

    def print_map(self):
        for row in map_array:
            for val in row:
                print (val, end='')
            print()



map_array = [["1" for x in range (0, 40)] for y in range (0, 40)]
tree = Tree(map_array)
tree.build_bsp()
tree.make_room()
tree.print_tree()
tree.print_map()
print("")


tree.build_path()
