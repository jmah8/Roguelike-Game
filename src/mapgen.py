import gamemap
import random
from constant import *

class Room:
    """
    Class that represents a room

    Attributes:
        up_left ((int, int), arg): the coordinates of the topleft of the room
        down_right ((int, int), arg): the coordinates of the bottom right of the room
    """
    def __init__(self, up_left=None, down_right=None):
        self.up_left = up_left
        self.down_right = down_right

class Node:
    """
    Class that represents a node in the BSP Tree

    Attributes:
        up_left ((int, int), arg): coordinate of the topleft of the split node/sub dungeon
        down_right ((int, int), arg): coordinate of the bottom right of the split node/sub dungeon
        room (Room): Room object that the node holds
        left_child (Node, arg): left child of current node
        right_child (Node, arg): right child of current node
        split_hor (Boolean): Whether node is split horizontally or vertically. 
            True if split horizontally false for vertical. None for no split
        child_room_array = (Array): array of node's child's rooms
    """
    def __init__ (self, up_left, down_right, left_child=None, right_child=None):
        self.up_left = up_left
        self.down_right = down_right
        self.room = Room()
        self.left_child = left_child
        self.right_child = right_child
        self.split_hor = None 
        self.child_room_array = []

class Tree:
    """
    Class that represent A BSP Tree 

    Each node in tree represents a subdungeon in the tree

    Attributes
        root (Node): root node of tree. Should be size of whole map to generate
        map_array ([char[char]], arg): 2D array representing map. array should be all walls when tree is initialized
        sub_dungeon_width (int, arg): the min width of each sub dungeon
        sub_dungeon_height (int, arg): the min height of each sub dungeon
        dist_from_sister_node_min (int, arg): min distance a room should be from it's sister room or edge
        dist_from_sister_node_max (int, arg): max distance a room should be from it's sister room or edge
    """
    def __init__(self, map_array, sub_dungeon_width=SUB_DUNGEON_WIDTH, sub_dungeon_height=SUB_DUNGEON_HEIGHT,
                 dist_from_sister_node_min=DIST_FROM_SISTER_NODE_MIN, dist_from_sister_node_max=DIST_FROM_SISTER_NODE_MAX):
        y_len = len(map_array)
        x_len = len(map_array[0])
        self.root = Node((0, 0), (x_len - 1, y_len - 1))
        self.map_array = map_array
        self.sub_dungeon_width = sub_dungeon_width
        self.sub_dungeon_height = sub_dungeon_height
        self.dist_from_sister_node_min = dist_from_sister_node_min
        self.dist_from_sister_node_max = dist_from_sister_node_max

    def build_bsp(self):
        """
        Builds a bsp tree if root is not None
        """
        if (self.root != None):
            self._split_room(self.root)
        else:
            print("Root is None")

    def _split_room(self, node):
        """
        Recursively and randomly splits nodes into 2 rooms until can't split anymore

        Builds a bsp tree by randomly splitting map. Resulting nodes should have sub_dungeons with
        width and height >= sub_dungeon width and height

        If node's width and height is smaller than 2x sub_dungeon width/height, return node.
            (This is because each node must be >= sub_dungeon width/height)
        Else split whichever way is possible 

        Arg:
            node (Node, arg): Node to split
        """
        if (node.down_right[1] - node.up_left[1] < 2 * self.sub_dungeon_height and node.down_right[0] - node.up_left[0] < 2 * self.sub_dungeon_width):
            return node
        elif (node.down_right[1] - node.up_left[1] < 2 * self.sub_dungeon_height):
            self._split_vertical(node)
        elif (node.down_right[0] - node.up_left[0] < 2 * self.sub_dungeon_width):
            self._split_horizontal(node)
        else:
            hor = random.randint(0, 1)
            if (hor == 0):
                self._split_horizontal(node)
            else:
                self._split_vertical(node)

    def _split_horizontal(self, node):
        """
        Helper function to split node horizontally randomly, following sub_dungeon_height

        Arg:
            node (Node, arg): node to split horizontally
        """
        split_y = random.randint(node.up_left[1] + self.sub_dungeon_height, node.down_right[1] - self.sub_dungeon_height)
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
        """
        Helper function to split node vertically randomly, following sub_dungeon_width

        Arg:
            node (Node, arg): node to split vertically
        """
        split_x = random.randint(node.up_left[0] + self.sub_dungeon_width , node.down_right[0] - self.sub_dungeon_width)
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
        """
        Makes room in nodes if root is not None
        """
        if (self.root != None):
            self._make_rooms(self.root)
        else:
            print("Root is None")

    # TODO: decide if this should return a value or not
    def _make_rooms(self, node):
        """
        Recursively makes room in the leaf nodes and any parent node randomly chooses one of the child rooms

        Arg:
            node (Node, arg): node to make room in
        """
        # Return None if None node
        if (node == None):
            return None
        # Post order traversal of nodes 
        left = self._make_rooms(node.left_child)
        right = self._make_rooms(node.right_child)
        # TODO: add array of child rooms to node
        if (left == None and right == None):
            ul_x = random.randint(self.dist_from_sister_node_min, self.dist_from_sister_node_max)
            ul_y = random.randint(self.dist_from_sister_node_min, self.dist_from_sister_node_max)
            lr_x = random.randint(self.dist_from_sister_node_min, self.dist_from_sister_node_max)
            lr_y = random.randint(self.dist_from_sister_node_min, self.dist_from_sister_node_max)
            up_left = (node.up_left[0] + ul_x, node.up_left[1] + ul_y)
            down_right = (node.down_right[0] - lr_x, node.down_right[1] - lr_y)
            new_room = Room(up_left, down_right)
            node.room = new_room
        else:
            ran = random.randint(0, 1)
            if (ran == 0):
                up_left = node.left_child.room.up_left
                down_right = node.left_child.room.down_right
            else:
                up_left = node.right_child.room.up_left
                down_right = node.right_child.room.down_right
            new_room = Room(up_left, down_right)
            node.room = new_room
            node.child_room_array.append(left)
            node.child_room_array.append(right)

        for y in range(up_left[1], down_right[1] + 1):
            for x in range(up_left[0], down_right[0] + 1):
                self.map_array[y][x] = "0"
 

        node.child_room_array.append(new_room)

        return node.child_room_array


    # def _make_room(self, node):
    #     ul_x = random.randint(self.dist_from_sister_node_min, self.dist_from_sister_node_max)
    #     ul_y = random.randint(self.dist_from_sister_node_min, self.dist_from_sister_node_max)
    #     lr_x = random.randint(self.dist_from_sister_node_min, self.dist_from_sister_node_max)
    #     lr_y = random.randint(self.dist_from_sister_node_min, self.dist_from_sister_node_max)
    #     up_left = (node.up_left[0] + ul_x, node.up_left[1] + ul_y)
    #     down_right = (node.down_right[0] - lr_x, node.down_right[1] - lr_y)
    #     room = Room(up_left, down_right)
    #     node.room = room


    def build_path(self):
        """
        Builds path to join sister nodes
        """
        if (self.root != None):
            self._build_path(self.root)
        else:
            print("Root is None")

    def _build_path(self, node):
        """
        Recursively builds path to join sister nodes.

        Do nothing on leaf nodes. Else join the 2 children node's room with a random single tile path.
        Will cut through other rooms and paths. If there is no straight path from both rooms,
        randomly make a zigzag path to connect the 2 rooms

        Arg:
            node (Node, arg): node to build path for
        """
        if (node == None):
            return 

        left = self._build_path(node.left_child)
        right = self._build_path(node.right_child)

        if (node.left_child == None and node.right_child == None):
            return

        else:
            left_up = node.left_child.room.up_left
            left_down = node.left_child.room.down_right
            right_up = node.right_child.room.up_left
            right_down = node.right_child.room.down_right
            # If node was split horizontally
            if (node.split_hor):
                # print("hor")

                path_min_x = max(left_up[0], right_up[0])
                # example:
                # 111111
                # 110001
                # 111111
                # 100011
                # In this case path_min_x would be 2, since a path could only connect the 2 
                # rows of 0s if its greater or equal to 2

                path_max_x = min(left_down[0], right_down[0])
                # example:
                # 111111
                # 110001
                # 111111
                # 100011
                # In this case path_max_x would be 3, since a path could only connect the 2
                # rows of 0s if its less or equal to 2
                
                # print(path_min_x)
                # print(path_max_x)

                # Case: where left child is lower than right child (ie no straight path to both rooms)
                # 1111|1111
                # 1111|1001
                # 1111|1001
                # 1111|1111
                # 1000|1111
                # 1000|1111
                # 1111|1111
                """
                1 = wall
                0 = floor
                | = where the node was split (represents nothing on actual map)
                """
                if (path_max_x < path_min_x):
                    self._hor_zigzag_path(left_up, left_down, right_up, right_down)
                    
                # There is a straight path to both rooms
                else:
                    self._hor_straight_path(node, path_min_x, path_max_x)

            # If node was vertically split
            else:
                # print("ver")

                path_min_y = max(left_up[1], right_up[1])
                # example:
                # 101111
                # 101101
                # 101101
                # 111101
                # In this case path_min_y would be 1, since a path could only connect the 2
                # rows of 0s if its greater or equal to 1

                path_max_y = min(left_down[1], right_down[1])
                # example:
                # 101111
                # 101101
                # 101101
                # 111101
                # In this case path_max_y would be 2, since a path could only connect the 2
                # rows of 0s if its less or equal to 2

                # print(path_min_y)
                # print(path_max_y)

                # Case: where left child (top one) is higher up than the right child (bottom one)
                # (ie no straight path to both rooms)
                # 11111111
                # 11111001
                # 11111001
                # 11111111
                # --------
                # 11111111
                # 10001111
                # 10001111
                # 11111111
                """
                1 = wall
                0 = floor
                - = where node was split (represents nothing on actual map)
                """
                if (path_max_y < path_min_y):
                    self._vert_zigzag_path(left_up, left_down, right_up, right_down)

                # Else there is a straight path to both rooms
                else:
                    self._vert_straight_path(node, path_min_y, path_max_y)

            # self.print_map()
            # print("")


    def _hor_straight_path(self, node, path_min_x, path_max_x):
        """
        Helper function to build straight path for horizontally split node

        Arg:
            node (Node, arg): Current node to make path between 2 of it's children nodes
            path_min_x (int, arg): minimun x coordinate that the path must be
            path_max_x (int, arg): maximum x coordinate that the path must be
        """
        path_x = random.randint(path_min_x, path_max_x)
        # print(path_x)
        path_ul = (path_x, node.left_child.room.down_right[1] + 1)
        path_lr = (path_x + 1, node.right_child.room.up_left[1])
        # print(path_ul)
        # print(path_lr)
        # print("")

        for y in range(path_ul[1], path_lr[1]):
            for x in range(path_ul[0], path_lr[0]):
                # if (self.map_array[y][x] == '1'):
                    self.map_array[y][x] = "."


    def _vert_straight_path(self, node, path_min_y, path_max_y):
        """
        Helper function to build straight path for vertically split node

        Arg:
            node (Node, arg): Current node to make path between 2 of it's children nodes
            path_min_y (int, arg): minimun y coordinate that the path must be
            path_max_y (int, arg): maximum y coordinate that the path must be
        """
        path_y = random.randint(path_min_y, path_max_y)
        # print (path_y)  
        path_ul = (node.left_child.room.down_right[0] + 1, path_y)
        path_lr = (node.right_child.room.up_left[0], path_y + 1)
        # print(path_ul)
        # print(path_lr)
        # print("")
    
        for y in range(path_ul[1], path_lr[1]):
            for x in range(path_ul[0], path_lr[0]):
                # if (self.map_array[y][x] == '1'):
                    self.map_array[y][x] = "."


    def _hor_zigzag_path(self, left_up, left_down, right_up, right_down):
        """
        Helper function to build a zigzag path for a horizontally split node

        Arg:
            left_up ((int, int), arg): left child room's up left coordinate
            left_down ((int, int), arg): left child room's down right coordinate
            right_up ((int, int), arg): right child room's up left coordinate
            right_down ((int, int), arg): right child room's down right coordinate
        """
        left_x = random.randint(left_up[0], left_down[0])
        right_x = random.randint(right_up[0], right_down[0])
        diff_y = right_up[1] - left_down[1]
        left_y = random.randint(2, diff_y - 2)
        right_y = diff_y - left_y 
        # path_ul = (right_x, right_y)
        # path_lr = (left_x, left_y)
        low = min(left_x, right_x)
        high = max(left_x, right_x)

        for y in range(right_up[1] - right_y, right_up[1]):
            if (self.map_array[y][right_x] == '1'):
                self.map_array[y][right_x] = '.'

        for y in range(left_down[1] + 1, left_down[1] + left_y):
            if (self.map_array[y][left_x] == '1'):
                self.map_array[y][left_x] = '.'

        for i in range (low, high + 1):
            if (self.map_array[left_down[1] + left_y][i] == '1'):
                self.map_array[left_down[1] + left_y][i] = '.'


    def _vert_zigzag_path(self, left_up, left_down, right_up, right_down):
        """
        Helper function to build a zigzag path for a vertically split node

        Arg:
            left_up ((int, int), arg): left child room's up left coordinate
            left_down ((int, int), arg): left child room's down right coordinate
            right_up ((int, int), arg): right child room's up left coordinate
            right_down ((int, int), arg): right child room's down right coordinate
        """
        left_y = random.randint(left_up[1], left_down[1])
        right_y = random.randint(right_up[1], right_down[1])
        diff_x = right_up[0] - left_down[0]
        left_x = random.randint(2, diff_x - 2)
        right_x = diff_x - left_x
        # print(left_x)
        # print(right_x)
        # path_ul = ((right_up[0] - right_x), right_y)
        # path_lr = ((left_down[0] + left_x), left_y)
        low = min(left_y, right_y)
        high = max(left_y, right_y)
        # print("Zigzag path")
        # print(path_ul)
        # print(path_lr)

        for x in range (left_down[0] + 1, left_down[0] + left_x):
            # if (self.map_array[left_y][x] == '1'):
                self.map_array[left_y][x] = '.'

        for x in range (right_up[0] - right_x, right_up[0]):
            # if (self.map_array[right_y][x] == '1'):
                self.map_array[right_y][x] = '.'

        for i in range (low, high + 1):
            # if (self.map_array[i][(left_down[0] + left_x)] == '1'):
                self.map_array[i][(left_down[0] + left_x)] = '.'

    
    def find_closest_room(self, coord, left_child, right_child):
        #TODO: could use this for make better paths
        pass

    def print_tree(self):
        """
        Prints tree information if root is not None.

        Prints the up_left and down_right coordinate of node and room up_left and down_right
        if node has room
        """
        if (self.root != None):
            self._print_tree(self.root)

    def _print_tree(self, node):
        """
        Recursively prints tree information using post order traversal

        Arg:
            node (Node, arg): node to print information
        """
        if (node != None):
            self._print_tree(node.left_child)
            self._print_tree(node.right_child)
            print("up_left: " + str(node.up_left) + " , down_right: " + str(node.down_right))
            if (node.room.up_left != None and node.room.down_right != None):
                print("room.up_left: " + str(node.room.up_left) + " , room.down_right: " + str(node.room.down_right))
            print("")

    def print_map(self):
        """
        Prints maps
        """
        for row in self.map_array:
            for val in row:
                print (val, end='')
            print()



# map_array = [["1" for x in range (0, 40)] for y in range (0, 40)]
# tree = Tree(map_array)
# tree.build_bsp()
# tree.make_room()
# tree.build_path()
# tree.print_map()
