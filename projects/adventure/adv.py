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

# Initiate visited tracker
v_rooms = set()
# Add starting room to visited tracker
v_rooms.add(player.current_room.id)
# Intiate queue to track exits
queue = {player.current_room.id:{}}
# Add exits to queue
cur_exits = player.current_room.get_exits()
for e in cur_exits:
    queue[player.current_room.id].update({e:'?'})
prev_room_id = None
# While queue is not empty
while len(queue) > 0:
    print('Current room:', player.current_room.id)
    print('Queue:', queue)
    # dequeue next exit
    cur_exits = queue[player.current_room.id]
    if len(cur_exits) < 2:
        next_exit = queue[player.current_room.id].popitem()
        del queue[player.current_room.id]
    else:
        next_exit = queue[player.current_room.id].popitem()
        check_exit = next_exit
        print('Next Exit before checks:', str(next_exit))    
        if next_exit[1] != '?':
            print('check 1')
            next_exit = queue[player.current_room.id].popitem()
            if next_exit[1] == '?' and len(queue[player.current_room.id]) == 0:
                print('check 1a')
                queue[player.current_room.id][check_exit[0]] = check_exit[1]
            # if not bool(queue[next_exit[1]]):
            #     next_exit = queue[player.current_room.id].popitem()
            print('next exit after check 1:', str(next_exit))
        if next_exit[1] == prev_room_id:
            print('check 2')
            next_exit = queue[player.current_room.id].popitem()
            # if not bool(queue[player.current_room.id]):
            #     print('check 2a')
            #     del queue[player.current_room.id]
        if next_exit[1] =='?' and next_exit[1] in v_rooms:
            print('check 3')
            next_exit = queue[player.current_room.id].popitem()

    print('Updated queue:', queue)
    print('Next Exit after checks:', str(next_exit))   
        
    # Create prev room tracker
    prev_room_id = player.current_room.id
    # print('Previous room:', prev_room_id)
    move_direction = next_exit[0]
    # Move player to next room
    player.travel(next_exit[0])
    print('Player moved...........')
    print('Room after move:', player.current_room.id)
    print('Move Direction:', move_direction)
    traversal_path.append(next_exit[0])
    print('Path:', traversal_path)
    
    # Check if exit room is visited
    if player.current_room.id not in v_rooms:
        print('Current room added:', player.current_room.id)
        v_rooms.add(player.current_room.id)
        # Enqueue room exits
        cur_exits = player.current_room.get_exits()
        queue.update({player.current_room.id:{}})
        for e in cur_exits:
            queue[player.current_room.id].update({e:'?'})
        # Update rooms in queue
        if move_direction == 'n':
            queue[player.current_room.id]['s'] = prev_room_id
            if bool(queue[prev_room_id]):
                queue[prev_room_id]['n'] = player.current_room.id
        if move_direction == 'e':
            queue[player.current_room.id]['w'] = prev_room_id
            if bool(queue[prev_room_id]):
                queue[prev_room_id]['e'] = player.current_room.id
        if move_direction == 's':
            queue[player.current_room.id]['n'] = prev_room_id
            if bool(queue[prev_room_id]):
                queue[prev_room_id]['s'] = player.current_room.id
        if move_direction == 'w':
            queue[player.current_room.id]['e'] = prev_room_id
            if bool(queue[prev_room_id]):
                queue[prev_room_id]['w'] = player.current_room.id
    
    else:
        # Update rooms in queue
        if move_direction == 'n':
            queue[player.current_room.id]['s'] = prev_room_id
            # queue[prev_room_id]['n'] = player.current_room.id
        if move_direction == 'e':
            queue[player.current_room.id]['w'] = prev_room_id
            # queue[prev_room_id]['e'] = player.current_room.id
        if move_direction == 's':
            queue[player.current_room.id]['n'] = prev_room_id
            # queue[prev_room_id]['s'] = player.current_room.id
        if move_direction == 'w':
            queue[player.current_room.id]['e'] = prev_room_id
            # queue[prev_room_id]['w'] = player.current_room.id
    
    
    print('Rooms visited:', v_rooms)
    graph_keys = list(world.rooms.keys())
    v_rooms2 = list(v_rooms)
    print('Graph size', graph_keys)
    if graph_keys == v_rooms2:
        break
    print('------------------------Loop complete-----------------------------')
    


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
