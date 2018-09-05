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


# heuristic, Euclidean distance
def h_Eu(curr):
	return math.sqrt(pow((gi - curr[0]), 2) + pow((gj - curr[1]), 2))


# Greedy search
def greedy(field, start, goal):

    adj_dir = [r, l, up, dn]

    closed = set()
    actual_path = {}
    h = {start:h_Eu(start)}
    op_heap = []

	# Step1
    heappush(op_heap, (h[start], start))
    
    while op_heap: # Step5(loop)
	
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
		
		#Step3
        closed.add(current)

        for i, j in adj_dir:
            adj_cell = current[0] + i, current[1] + j
            if 0 <= adj_cell[0] < field.shape[0]:
                if 0 <= adj_cell[1] < field.shape[1]:             
                    if field[adj_cell[0]][adj_cell[1]] == 1:
                        continue
                else:
                    continue
            else:
                continue
            
            if adj_cell in closed:
                continue

            # Step4
            actual_path[adj_cell] = current
            h[adj_cell] = h_Eu(adj_cell) # h
            heappush(op_heap, (h[adj_cell], adj_cell))
    
	# search failed            
    return False


def main():

	print("Shortest path by Greedy;")

	start = time.time()
	path = greedy(field, (si, sj), (gi, gj))
	elapsed_time = time.time() - start
	
	path.reverse()
	print path

	print('elapsed time: '+ str(elapsed_time) + '[sec]')


if __name__ == '__main__':
    main()

