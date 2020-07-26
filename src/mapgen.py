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


    def return_coords(self):
        """
        Return coordinates of room
        """
        return self.up_left[0], self.up_left[1], self.down_right[0], self.down_right[1]




def find_common_x_between_rooms(left_room, right_room):
    """
    Finds the lowest and highest common x coord between 2 rooms

    Example:
    111111
    110001
    111111
    100011

    In this case lowest_common_x would be 2, since a path could only connect the 2 
    rows of 0s if its greater or equal to 2 and 

    In this case highest_common_x would be 3, since a path could only connect the 2
    rows of 0s if its less or equal to 2
    """
    # min x value that both rooms share in common
    lowest_common_x = max(left_room.up_left[0], right_room.up_left[0])
    # max x value that both rooms share in common
    highest_common_x = min(left_room.down_right[0], right_room.down_right[0]) 
    return lowest_common_x, highest_common_x




def find_common_y_between_rooms(left_room, right_room):
    """
    Finds the lowest and highest common y coord between 2 rooms

    Example:
    101111
    101101
    101101
    111101

    In this case lowest_common_y would be 1, since a path could only connect the 2
    rows of 0s if its greater or equal to 1

    In this case highest_common_y would be 2, since a path could only connect the 2
    rows of 0s if its less or equal to 2
    """
    # min y value that both rooms share in common
    lowest_common_y = max(left_room.up_left[1], right_room.up_left[1])
    # max y value that both rooms share in common
    highest_common_y = min(left_room.down_right[1], right_room.down_right[1])
    return lowest_common_y, highest_common_y




class Node:
    """
    Class that represents a node in the BST

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
    Class that represent A BST 

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

        Args:
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

        Args:
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

        Args:
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




    def _make_rooms(self, node):
        # TODO: could change it so the SUB_DUNGEON width/height correspond to the actual room dimensions
        #       instead of sub dungeon dimension
        """
        Recursively makes room in the leaf nodes and any parent node randomly chooses one of the child rooms
        as its room

        Args:
            node (Node, arg): node to make room in
        """
        # Return None if None node
        if (node == None):
            return None

        # Post order traversal of nodes 
        left = self._make_rooms(node.left_child)
        right = self._make_rooms(node.right_child)

        if (left == None and right == None):
            new_room = self._make_room_in_leaf_node(node)
        else:
            node.child_room_array = node.child_room_array + left
            node.child_room_array = node.child_room_array + right 
            # Choose one or the other
            new_room = self._get_room_from_random_child(node)
            # new_room = self._get_room_from_random_immediate_child(node)

        node.child_room_array.append(new_room)

        return node.child_room_array



    def _make_room_in_leaf_node(self, node):
        """
        Makes room in leaf nodes only and returns the room made

        Args:
            node (Node, arg): node to make room in
        """
        ul_x = random.randint(self.dist_from_sister_node_min, self.dist_from_sister_node_max)
        ul_y = random.randint(self.dist_from_sister_node_min, self.dist_from_sister_node_max)
        lr_x = random.randint(self.dist_from_sister_node_min, self.dist_from_sister_node_max)
        lr_y = random.randint(self.dist_from_sister_node_min, self.dist_from_sister_node_max)
        up_left = (node.up_left[0] + ul_x, node.up_left[1] + ul_y)
        down_right = (node.down_right[0] - lr_x, node.down_right[1] - lr_y)
        new_room = Room(up_left, down_right)
        node.room = new_room

        for y in range(up_left[1], down_right[1] + 1):
            for x in range(up_left[0], down_right[0] + 1):
                self.map_array[y][x] = FLOOR

        return new_room


    
    def _get_room_from_random_immediate_child(self, node):
        """
        Makes room in parent node by choosing a room from one of it's immediate children

        Args:
            node (Node, arg): node to make room in
        """
        ran = random.randint(0, 1)
        if (ran == 0):
            up_left = node.left_child.room.up_left
            down_right = node.left_child.room.down_right
        else:
            up_left = node.right_child.room.up_left
            down_right = node.right_child.room.down_right

        new_room = Room(up_left, down_right)
        node.room = new_room
        return new_room



    def _get_room_from_random_child(self, node):
        """
        Makes room in parent node by choosing a room from any of it's children

        Args:
            node (Node): node to make room in
        """
        room = random.choice(node.child_room_array)

        new_room = room    
        node.room = new_room
        return new_room





    def build_path(self):
        """
        Builds path to join sister nodes
        """
        if (self.root != None):
            # self._build_path(self.root)
            self._build_path_intelligent(self.root)
        else:
            print("Root is None")




    def _build_path(self, node):
        """
        Recursively builds path to join sister nodes.

        Do nothing on leaf nodes. Else join the 2 children node's room with a random 
        single tile path. Will cut through other rooms and paths. If there is no 
        straight path from both rooms, randomly make a zigzag path to connect the 2 rooms

        Args:
            node (Node, arg): node to build path for
        """
        if (node == None):
            return 

        left = self._build_path(node.left_child)
        right = self._build_path(node.right_child)

        # If leaf node do nothing
        if (node.left_child == None and node.right_child == None):
            return

        else:
            left_child = node.left_child
            right_child = node.right_child

            # If node was split horizontally
            if (node.split_hor):
                path_min_x, path_max_x = find_common_x_between_rooms(left_child.room, right_child.room)

                # Case: where left child is lower than right child (ie no straight path to both rooms)
                # 1111|1111
                # 1111|1001
                # 1111|1001
                # 1111|1111
                # 1000|1111
                # 1000|1111
                # 1111|1111

                # 1 = wall
                # 0 = floor
                # | = where the node was split (represents nothing on actual map)
                if (path_max_x < path_min_x):
                    self._hor_zigzag_path(left_child, right_child)
                    
                # There is a straight path to both rooms
                else:
                    self._hor_straight_path(node, path_min_x, path_max_x)



            # If node was vertically split
            else:
                path_min_y, path_max_y = find_common_y_between_rooms(left_child.room, right_child.room)

                # Case: where left child (top one) is more to the right than the right child (bottom one)
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

                # 1 = wall
                # 0 = floor
                # - = where node was split (represents nothing on actual map)
                if (path_max_y < path_min_y):
                    self._vert_zigzag_path(left_child, right_child)

                # Else there is a straight path to both rooms
                else:
                    self._vert_straight_path(node, path_min_y, path_max_y)






    def _build_path_intelligent(self, node):
        """
        Recursively builds path to join sister nodes.

        Do nothing on leaf nodes. Else join the 2 children node's room with a random single tile path.
        This method will build paths more intelligently (ie no zigzags and cutting through rooms)
        and connect rooms close to where the children nodes were divided

        Args:
            node (Node, arg): node to build path for
        """
        if (node == None):
            return 

        left = self._build_path_intelligent(node.left_child)
        right = self._build_path_intelligent(node.right_child)

        # If leaf node do nothing
        if (node.left_child == None and node.right_child == None):
            return

        else:
            self.build_path_to_closest_rooms(node)



    def _hor_straight_path(self, node, path_min_x, path_max_x):
        """
        Helper function to build straight path for horizontally split node

        Args:
            node (Node, arg): Current node to make path between 2 of it's children nodes
            path_min_x (int, arg): minimun x coordinate that the path must be
            path_max_x (int, arg): maximum x coordinate that the path must be
        """
        path_x = random.randint(path_min_x, path_max_x)

        path_ul = (path_x, node.left_child.room.down_right[1] + 1)
        path_lr = (path_x + 1, node.right_child.room.up_left[1])

        self._draw_hor_straight_path_on_map(path_ul, path_lr)


    def _build_hor_straight_path(self, left_room, right_room):
        """
        Helper function to build straight path for horizontally split node

        Arg
            left_room (Room, arg): left room to make path from
            right_room (Room, arg): right room to make path to
            # path_min_x (int, arg): minimun x coordinate that the path must be
            # path_max_x (int, arg): maximum x coordinate that the path must be
        """
        # TODO: could change these 2 lines to be in if, since in _build_path it
        #       calculated before calling this method, but in find_closest_room
        #       it isn't 
        path_min_y, path_max_y = find_common_y_between_rooms(left_room, right_room)

        path_y = random.randint(path_min_y, path_max_y)

        path_ul = (left_room.down_right[0] + 1, path_y)
        path_lr = (right_room.up_left[0], path_y + 1)

        self._draw_hor_straight_path_on_map(path_ul, path_lr)

    
    def _draw_hor_straight_path_on_map(self, path_ul, path_lr):
        """
        Draws straight horizontal path from path_ul to path_lr

        Args:
            path_ul ((int, int), arg): upper left of path coord
            path_lr ((int, int), arg): lower right of path coord
        """
        for y in range(path_ul[1], path_lr[1]):
            for x in range(path_ul[0], path_lr[0]):
                # if (self.map_array[y][x] == '1'):
                    self.map_array[y][x] = PATH


    def _vert_straight_path(self, node, path_min_y, path_max_y):
        """
        Helper function to build straight path for vertically split node

        Args:
            node (Node, arg): Current node to make path between 2 of it's children nodes
            path_min_y (int, arg): minimun y coordinate that the path must be
            path_max_y (int, arg): maximum y coordinate that the path must be
        """
        path_y = random.randint(path_min_y, path_max_y)

        path_ul = (node.left_child.room.down_right[0] + 1, path_y)
        path_lr = (node.right_child.room.up_left[0], path_y + 1)
    
        self._draw_vert_straight_path_on_map(path_ul, path_lr)


    def _build_vert_straight_path(self, left_room, right_room):
        """
        Helper function to build straight path for vertically split node

        Args:
            left_room (Room, arg): left room to make path from
            right_room (Room, arg): right room to make path to        
            # path_min_y (int, arg): minimun y coordinate that the path must be
            # path_max_y (int, arg): maximum y coordinate that the path must be
        """
        # TODO: could change these 2 lines to be in if, since in _build_path it
        #       calculated before calling this method, but in find_closest_room
        #       it isn't 
        path_min_x, path_max_x = find_common_x_between_rooms(left_room, right_room)

        path_x = random.randint(path_min_x, path_max_x)

        path_ul = (path_x, left_room.down_right[1] + 1)
        path_lr = (path_x + 1, right_room.up_left[1])
    
        self._draw_vert_straight_path_on_map(path_ul, path_lr)


    def _draw_vert_straight_path_on_map(self, path_ul, path_lr):
        """
        Draws straight vertical path from path_ul to path_lr

        Args:
            path_ul ((int, int), arg): upper left of path coord
            path_lr ((int, int), arg): lower right of path coord
        """
        for y in range(path_ul[1], path_lr[1]):
            for x in range(path_ul[0], path_lr[0]):
                # if (self.map_array[y][x] == '1'):
                    self.map_array[y][x] = PATH


    def _hor_zigzag_path(self, left_child, right_child):
        """
        Helper function to build a zigzag path for a horizontally split node

        Args:
            left_child (Node, arg): left child to build path to
            right_child (Node, arg): right child to build path to

        """
        left_child_up_x, left_child_up_y, left_child_down_x, left_child_down_y = left_child.room.return_coords()
        right_child_up_x, right_child_up_y, right_child_down_x, right_child_down_y = right_child.room.return_coords()

        # x coord of path connecting the left room
        left_x = random.randint(left_child_up_x, left_child_down_x)
        # x coord of path connecting the right room
        right_x = random.randint(right_child_up_x, right_child_down_x)

        diff_y = right_child_up_y - left_child_down_y

        # make sure that the path has atleast one square sticking straigh 
        # out from children before zigzagging
        left_y = random.randint(2, diff_y - 2)
        right_y = diff_y - left_y

        low = min(left_x, right_x)
        high = max(left_x, right_x)

        # draw zig part for right child
        for y in range(right_child_up_y - right_y, right_child_up_y):
            # if (self.map_array[y][right_x] == '1'):
                self.map_array[y][right_x] = PATH

        # draw zig part for left child
        for y in range(left_child_down_y + 1, left_child_down_y + left_y):
            # if (self.map_array[y][left_x] == '1'):
                self.map_array[y][left_x] = PATH

        # draw zag part that connects the two zig parts
        for x in range (low, high + 1):
            # if (self.map_array[left_child_down_y + left_y][x] == '1'):
                self.map_array[left_child_down_y + left_y][x] = PATH


    def _vert_zigzag_path(self, left_child, right_child):
        """
        Helper function to build a zigzag path for a vertically split node

        Args:
            left_up ((int, int), arg): left child room's up left coordinate
            left_down ((int, int), arg): left child room's down right coordinate
            right_up ((int, int), arg): right child room's up left coordinate
            right_down ((int, int), arg): right child room's down right coordinate
        """
        left_child_up_x, left_child_up_y, left_child_down_x, left_child_down_y = left_child.room.return_coords()
        right_child_up_x, right_child_up_y, right_child_down_x, right_child_down_y = right_child.room.return_coords()

        # y coord of path connecting the left room
        left_y = random.randint(left_child_up_y, left_child_down_y)
        # y coord of path connecting the right room
        right_y = random.randint(right_child_up_y, right_child_down_y)

        diff_x = right_child_up_x - left_child_down_x

        # make sure that the path has atleast one square sticking straigh 
        # out from children before zigzagging
        left_x = random.randint(2, diff_x - 2)
        right_x = diff_x - left_x

        low = min(left_y, right_y)
        high = max(left_y, right_y)

        # draw zig part for left child
        for x in range (left_child_down_x + 1, left_child_down_x + left_x):
            # if (self.map_array[left_y][x] == '1'):
                self.map_array[left_y][x] = PATH

        # draw zig part for left child
        for x in range (right_child_up_x - right_x, right_child_up_x):
            # if (self.map_array[right_y][x] == '1'):
                self.map_array[right_y][x] = PATH

        # draw zag part that connects the two zig parts
        for y in range (low, high + 1):
            # if (self.map_array[y][(left_child_down_x + left_x)] == '1'):
                self.map_array[y][(left_child_down_x + left_x)] = PATH

    
    def build_path_to_closest_rooms(self, node):
        """
        Builds paths between adjacent children rooms

        Args:
            node (Node, arg): node to build path between its children's room
        """
        if (node.split_hor):
            # Horizontally split means the two subdungeons are on top of each other
            # therefore we should find if it is vertically adjacent

            # TODO: could shuffle list to make it more random
            # random.shuffle(node.left_child.child_room_array)
            # random.shuffle(node.right_child.child_room_array)
            for l_room in (node.left_child.child_room_array):
                for r_room in (node.right_child.child_room_array):
                    if (self._find_if_rooms_are_vert_adjacent(l_room, r_room)):
                        self._build_vert_straight_path(l_room, r_room)
                        return

        else:
            # Vertically split means the two subdungeons are beside each other
            # therefore we should find if it is horizontally adjacent

            # TODO: could shuffle list to make it more random
            # random.shuffle(node.left_child.child_room_array)
            # random.shuffle(node.right_child.child_room_array)
            for l_room in (node.left_child.child_room_array):
                for r_room in (node.right_child.child_room_array):
                    if (self._find_if_rooms_are_hor_adjacent(l_room, r_room)):
                        self._build_hor_straight_path(l_room, r_room)
                        return


    

    def _find_if_rooms_are_vert_adjacent(self, left_room, right_room):
        """
        Return true if both rooms are vertically adjacent

        Rooms are considered vertically adjacent if the rooms have at 
        least 1 common x coord and are children of the same parent node,
        meaning that the distance between them is between 2* DIST_FROM_SISTER_NODE
        min/max

        Args:
            left_room (Room, arg): left room to check
            right_room (Room, arg): right room to check
        """

        # min and max x value that both rooms share in common
        path_min_x, path_max_x = find_common_x_between_rooms(left_room, right_room)

        # If both rooms are in the same x range = True, else False
        adj = path_min_x <= path_max_x

        if (adj):
            left_y = left_room.down_right[1]
            right_y = right_room.up_left[1]
            diff_y = right_y - left_y
            # Return if rooms are adjacent to each other, ie if the distance between them are 2 DIST_FROM_SISTER_NODE min and max
            return (diff_y >= (2 * DIST_FROM_SISTER_NODE_MIN)) and (diff_y <= (2 * DIST_FROM_SISTER_NODE_MAX))
        
        return False

    
    def _find_if_rooms_are_hor_adjacent(self, left_room, right_room):
        """
        Return true if both rooms are horizontally adjacent

        Rooms are considered horizontally adjacent if the rooms have at 
        least 1 common y coord and are children of the same parent node,
        meaning that the distance between them is between 2* DIST_FROM_SISTER_NODE
        min/max

        Args:
            left_room (Room, arg): left room to check
            right_room (Room, arg): right room to check
        """

        # min and max y value that both rooms share in common
        path_min_y, path_max_y = find_common_y_between_rooms(left_room, right_room)


        # If both rooms are in the same y range = True, else false
        adj = path_min_y <= path_max_y

        if (adj):
            left_x = left_room.down_right[0]
            right_x = right_room.up_left[0]
            diff_y = right_x - left_x
            # Return if rooms are adjacent to each other, ie if the distance between them are 2 DIST_FROM_SISTER_NODE min and max
            return (diff_y >= (2 * DIST_FROM_SISTER_NODE_MIN)) and (diff_y <= (2* DIST_FROM_SISTER_NODE_MAX))

        return False

        


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

        Args:
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
        Prints the map using the constants defined in constant.py
        """
        for row in self.map_array:
            for val in row:
                print (val, end='')
            print()