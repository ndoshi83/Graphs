from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# function to search dictionary by value
def dictionarySearch(d, v, t):
    if t == 1:
        k_list = []
        dv = d.items()
        for i in dv:
            if i[1] == v:
                k_list.append(i[0])

        nd = {x:d[x] for x in k_list}
    elif t == 2:
        k_list = []
        dv = d.items()
        for i in dv:
            if i[1] != v:
                k_list.append(i[0])

        nd = {x:d[x] for x in k_list}
    else:
        nd = {}

    return nd

# Create empty queue
q = {}
# Enqueue exits into queue
q[player.current_room.id] = {}
cur_exits = player.current_room.get_exits()
for e in cur_exits:
    q[player.current_room.id][e] = '?'
visited = set()
visited.add(player.current_room.id)
# While queue is populated
while len(q) > 0:
    # Dequeue exit from current room
    exit = q[player.current_room.id].popitem()
    # print(exit[0])
    # Track prior room
    p_room = player.current_room.id
    # print('Prior room:', p_room)
    # Make move to next room
    player.travel(exit[0])
    # print(player.current_room.id)
    # Add move direction to traversal path
    traversal_path.append(exit[0])
    # Check if new room is visited before
    if player.current_room.id not in visited:
        # print('Check Visited')
        # Add new room to visited
        visited.add(player.current_room.id)
        # Add new room exits to queue
        new_exits = player.current_room.get_exits()
        q[player.current_room.id] = {}
        for e in new_exits:
            q[player.current_room.id][e] = '?'
        # Update flags
        if exit[0] == 'n':
            # Update current room
            q[player.current_room.id]['s'] = p_room
            temp_c = dictionarySearch(q[player.current_room.id],'?',2)
            temp_c.update(dictionarySearch(q[player.current_room.id],'?',1))
            q[player.current_room.id] = temp_c
            # Update prior room
            if len(new_exits) > 2:
                q[p_room]['n'] = player.current_room.id
                temp_p = dictionarySearch(q[p_room],'?',2)
                temp_p.update(dictionarySearch(q[p_room],'?',1))
                q[p_room] = temp_p
        if exit[0] == 's':
            # Update current room
            q[player.current_room.id]['n'] = p_room
            temp_c = dictionarySearch(q[player.current_room.id],'?',2)
            temp_c.update(dictionarySearch(q[player.current_room.id],'?',1))
            q[player.current_room.id] = temp_c
            # Update prior room
            if len(new_exits) > 2:
                q[p_room]['s'] = player.current_room.id
                temp_p = dictionarySearch(q[p_room],'?',2)
                temp_p.update(dictionarySearch(q[p_room],'?',1))
                q[p_room] = temp_p
        if exit[0] == 'w':
            # Update current room
            q[player.current_room.id]['e'] = p_room
            temp_c = dictionarySearch(q[player.current_room.id],'?',2)
            temp_c.update(dictionarySearch(q[player.current_room.id],'?',1))
            q[player.current_room.id] = temp_c
            # Update prior room
            if len(new_exits) > 2:
                q[p_room]['w'] = player.current_room.id
                temp_p = dictionarySearch(q[p_room],'?',2)
                temp_p.update(dictionarySearch(q[p_room],'?',1))
                q[p_room] = temp_p
        if exit[0] == 'e':
            # Update current room
            q[player.current_room.id]['w'] = p_room
            temp_c = dictionarySearch(q[player.current_room.id],'?',2)
            temp_c.update(dictionarySearch(q[player.current_room.id],'?',1))
            q[player.current_room.id] = temp_c
            # Update prior room
            if len(new_exits) > 2:
                q[p_room]['e'] = player.current_room.id
                temp_p = dictionarySearch(q[p_room],'?',2)
                temp_p.update(dictionarySearch(q[p_room],'?',1))
                q[p_room] = temp_p
    else:
        keys = list(q[player.current_room.id].keys())
        # print(keys)
        if exit[0] == 'n':
            od = 's'
        if exit[0] == 's':
            od = 'n'
        if exit[0] == 'w':
            od = 'e'
        if exit[0] == 'e':
            od = 'w'
        # print(od)
        if od in keys: 
            if q[player.current_room.id][od] == '?':
                q[player.current_room.id][od] = p_room
                temp_c = dictionarySearch(q[player.current_room.id],'?',2)
                temp_c.update(dictionarySearch(q[player.current_room.id],'?',1))
                q[player.current_room.id] = temp_c
            else:
                q[player.current_room.id].pop(od)
                
    # print(q)
    # print(visited)

    graph_keys = list(world.rooms.keys())
    # print(graph_keys)
    visited2 = list(visited)
    # print(visited2)
    if graph_keys == visited2:
        break
#     print('--------------------Loop-------------------------------------------------')
# print(traversal_path)
  


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
