import numpy as np
import time
import math
from heapq import *

# 1 represents obstacle
field = np.array([
    		[0,0,0,0,1,0,0,0,0,0,0,0],
            [0,0,0,0,1,0,0,0,0,0,0,0],
            [0,0,0,1,1,1,1,1,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,1,1,0,0,0,0,0],
            [0,0,0,0,1,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,1,0,0,0,0,0]])


# start/goal position
si, sj = 9, 5
gi, gj = 0, 5


# dir
r, l, up, dn = (0, 1), (0, -1), (1, 0), (-1, 0)


# cost(n,n')
one_step_cost = 1


# heuristic, Euclidean distance
def h_Eu(curr, dest):
	return math.sqrt(pow((dest[0] - curr[0]), 2) + pow((dest[1] - curr[1]), 2))


# A* search
def astar(field, start, goal):

    adj_dir = [r, l, up, dn] # possible move dir to adjacent blocks

    closed = set() # set, format: ((cell), ...)
    actual_path = {} # dictionary, format: {(child):(parent), ...}
    g = {start:0} # format: {(cell):g(n), ...}
    f = {start:h_Eu(start, goal)} # format: {(cell):h(n), ...}
    op_heap = [] # a list (of tuples, eventually)
	
	# Step1
    heappush(op_heap, (f[start], start)) # append start node to open list
    
    while op_heap: #Step5(loop)
		
		# Step2
        current = heappop(op_heap)[1]

        if current == goal:
			# trace
            trace = [] 
            while current in actual_path:
                trace.append(current)
                trace.append("->")
                current = actual_path[current]
            trace.append(current)
            return trace

		# Step3
        closed.add(current)

        for i, j in adj_dir:
            adj_cell = current[0] + i, current[1] + j            
            tent_g = g[current] + one_step_cost # calculating cost, alternative; h_Eu(current, adj_cell)
            if 0 <= adj_cell[0] < field.shape[0]: # as long as i is in the field
                if 0 <= adj_cell[1] < field.shape[1]: # as long as j is in the field               
                    if field[adj_cell[0]][adj_cell[1]] == 1: # skip if the cell is an obstacle
                        continue
                else:
                    continue
            else:
                continue
            
			# Step4
            # if there is the same node with worse cost in closed list, then skip it    
            if adj_cell in closed and g.get(adj_cell, 0) <= tent_g:
                continue
            
            # if there is the same node with better cost in open list or there is no same node    
            if tent_g < g.get(adj_cell, 0) or adj_cell not in (i[1] for i in op_heap):
            	actual_path[adj_cell] = current
                g[adj_cell] = tent_g
                f[adj_cell] = tent_g + h_Eu(adj_cell, goal) # f = g + h
                heappush(op_heap, (f[adj_cell], adj_cell))
    
	# search failed            
    return False

'''
field: numpy array
astar(array, start, destination) -> returns a list of tuples (shortest path)
'''

def main():

	print("Shortest path by A*;")

	start = time.time()
	path = astar(field, (si, sj), (gi, gj))
	elapsed_time = time.time() - start
	
	path.reverse()
	print path

	print('elapsed time: '+ str(elapsed_time) + '[sec]')


if __name__ == '__main__':
    main()

