# imports
from cube import Cube
from visualizer import *
from alg_handler import *
from queue import Queue
import math


# ask user for information
# input_algorithm = input("What's your scramble?").split(" ")
# allowed_moves = input("What move types are allowed?").split(" ")
# max_depth_allowed = int(input("What is the maximum algorithm depth?"))

# given a list of lists, join_solutions creates a single list
# example input: [["D'", "U'", "R'"], ["U'", "D'", "R'"]]
# example output: ["D' U' R'", "U' D' R'"]
def join_solutions(solutions):
    joined_solutions = []
    for soln in solutions:
        joined_solutions.append(' '.join(soln))
    return joined_solutions


# generates all possible solutions for a scramble, subject to the given
# move_types and max_depth.
# scramble and move_types must be delimited by ","
def solve(scramble, move_types, max_depth):
    input_algorithm = scramble.split(",")
    allowed_moves = move_types.split(",")
    max_depth_allowed = int(max_depth)
    converted_max_depth_allowed = int(math.ceil((float(max_depth_allowed) / 2)))

    # create solved cube
    solved_cube = Cube()
    solved_cube.allowed_moves_for_chain = allowed_moves

    # create scrambled cube
    scrambled_cube = Cube()
    alg_handler.apply_alg(input_algorithm, scrambled_cube)
    scrambled_cube.moves_applied = []
    scrambled_cube.allowed_moves_for_chain = allowed_moves

    # present initial cubes
    # print_line()
    # print(f"Here are your cubes:")
    # print("Solved Cube")
    # cube_to_visual(solved_cube)
    # print("Scrambled Cube")
    # cube_to_visual(scrambled_cube)
    # print_line(3)

    # setup for search algorithm
    solved_hash = {}
    solved_queue = Queue()
    solved_queue.put(solved_cube)

    scrambled_hash = {}
    scrambled_queue = Queue()
    scrambled_queue.put(scrambled_cube)

    num_cubes = 0
    depth_next_queued = 0
    final_solutions = []

    # pruning
    odd_status = bool(max_depth_allowed % 2)

    # search algorithm
    while depth_next_queued < converted_max_depth_allowed:

        # take a cube from queue and make adjacency list
        got_cube = solved_queue.get()
        adj_list = got_cube.create_adj_list()

        for cube in adj_list:
            num_cubes += 1
            # set properties of adjacent cube
            cube.parent_cube = got_cube
            cube.depth = got_cube.depth + 1
            cube.allowed_moves_for_chain = cube.parent_cube.allowed_moves_for_chain

            # print info about cube
            # print("Started from solved cube")
            # cube_to_visual(cube)
            # print(f"Count: {num_cubes}")
            # print_depth(cube)
            # print_moves(cube)

            # handles if the cube state has/hasn't been reached from the solved (same) end
            if cube.update_tuple() not in solved_hash:
                # print("This cube state hasn't been reached from the solved end before, hashing now...")
                solved_hash[cube.update_tuple()] = [cube.moves_applied]
            else:
                # print("This cube state has already been reached from the solved end before via different moves,"
                #     "adding another sequence to hash now...")
                solved_hash[cube.update_tuple()].append(cube.moves_applied)

            # handles if the cube state has been reached from the scrambled end
            if cube.update_tuple() in scrambled_hash:
                # print("This cube state has been reached from the scrambled end before! Intersection found.")
                # print("Here are the ways we reached this state from the scrambled end:")

                # prints and adds solutions for when solved cube reaches state already found from scrambled end
                for scrambled_halfway in scrambled_hash[cube.update_tuple()]:
                    # print(scrambled_halfway)
                    stage_1 = reverse_and_invert_move_list(scrambled_halfway)
                    stage_2 = clean_up_intersection(cube.moves_applied, stage_1)
                    stage_3 = reverse_and_invert_move_list(stage_2)

                    if stage_3 not in final_solutions:
                        final_solutions.append(stage_3)

            # misc
            # print_line()
            solved_queue.put(cube)

        # for while condition
        depth_next_queued = solved_queue.queue[0].depth

        # ____________________________________ SCRAMBLED SIDE ____________________________________ #

        scrambled_got_cube = scrambled_queue.get()

        # pruning
        if odd_status and (scrambled_got_cube.depth == converted_max_depth_allowed - 1):
            continue

        scrambled_adj_list = scrambled_got_cube.create_adj_list()

        for scramble_cube in scrambled_adj_list:
            num_cubes += 1
            # set properties of adjacent cube
            scramble_cube.parent_cube = scrambled_got_cube
            scramble_cube.depth = scrambled_got_cube.depth + 1
            scramble_cube.allowed_moves_for_chain = scramble_cube.parent_cube.allowed_moves_for_chain

            # print info about cube
            # print(f"Started from scrambled cube")
            # cube_to_visual(scramble_cube)
            # print(f"Count: {num_cubes}")
            # print_depth(scramble_cube)
            # print_moves(scramble_cube)

            # handles if the cube state has/hasn't been reached from the scrambled (same) end
            if scramble_cube.update_tuple() not in scrambled_hash:
                # print("This cube state hasn't been reached from the scrambled end before, hashing now...")
                scrambled_hash[scramble_cube.update_tuple()] = [scramble_cube.moves_applied]

            else:
                # print("This cube state has already been reached from the solved end before, adding another moveset "
                #     "to hash now...")
                scrambled_hash[scramble_cube.update_tuple()].append(scramble_cube.moves_applied)

            # handles if the cube state has been reached from the solved end
            if scramble_cube.update_tuple() in solved_hash:
                # print("This cube state has been reached from the scrambled end before! Intersection found.")
                # print("Here are the ways we reached this state from the scrambled end:")

                # prints and adds solutions for when scrambled cube reaches state already found from solved end
                for solved_halfway in solved_hash[scramble_cube.update_tuple()]:
                    # print(solved_halfway)
                    stage_1 = reverse_and_invert_move_list(solved_halfway)
                    stage_2 = clean_up_intersection(scramble_cube.moves_applied, stage_1)

                    if stage_2 not in final_solutions:
                        final_solutions.append(stage_2)

            # misc
            # print_line()
            scrambled_queue.put(scramble_cube)

    # returns final solutions
    return join_solutions(final_solutions)


# testing
# print(solve("R,U,R',x,U,R,U'", "R,U,x", 8))
