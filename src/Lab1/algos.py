import pygame
from maze import *
from const import *
import time as t
import heapq
import math

def DFS(g: SearchSpace, sc: pygame.Surface):
    start = t.time()

    open_set = [g.start.id]
    closed_set = []
    father = [-1] * g.get_length()

    while open_set:
        curr_node_id = open_set.pop()
        curr_node = g.grid_cells[curr_node_id]

        if curr_node_id == g.goal.id:
            print("You have reached the goal")

            # Reconstruct the path from the goal to the start
            path = []
            while curr_node_id != -1:
                path.append(curr_node_id)
                curr_node_id = father[curr_node_id]
            path.reverse()
            print("Path reconstructed:", path)

            # Color the nodes in the path blue (except the first and last nodes)
            for index, node_id in enumerate(path):
                if index != 0 and index != len(path) - 1:
                    g.grid_cells[node_id].set_color(BLUE, sc)
                    print("total cost: ", index)
            # End the execution timer
            end = t.time()
            print("The time of execution of above program is :", (end-start) * 10**3, "ms")
            return path

        if curr_node_id != g.start.id and curr_node_id != g.goal.id:
            curr_node.set_color(YELLOW, sc)
            pygame.time.delay(5)
            pygame.display.update()
            curr_node.set_color(RED, sc)
        
        
        for neighbor in reversed(g.get_neighbors(curr_node)):
            neighbor_id = neighbor.id
            if neighbor_id not in closed_set and neighbor_id not in open_set:
                open_set.append(neighbor_id)
                father[neighbor_id] = curr_node_id    
        closed_set.append(curr_node_id)

    return None

    # raise NotImplementedError('not implemented')

def BFS(g: SearchSpace, sc: pygame.Surface):
    # Start the execution timer
    start = t.time() 
    
    print('Implement BFS algorithm')

    open_set = [g.start.id]
    closed_set = []
    father = [-1]*g.get_length()
    
    while open_set:
        current_node_id = open_set.pop(0)  # Dequeue the first node from the open set (queue)
        current_node = g.grid_cells[current_node_id]

        if current_node_id == g.goal.id:
            print("You have reached the goal")

            # Reconstruct the path from the goal to the start
            path = []
            while current_node_id != -1:
                print(f"Adding node {current_node_id} to the path")
                path.append(current_node_id)
                current_node_id = father[current_node_id]
            path.reverse()
            print("Path reconstructed:", path)

            # Color the nodes in the path blue
            for index, node_id in enumerate(path):
                if(index != 0 and index != len(path) - 1):
                    g.grid_cells[node_id].set_color(BLUE, sc)
                    
            # End the execution timer
            end = t.time()
            print("The time of execution of above program is :", (end-start) * 10**3, "ms")
            
            return path

        # Mark the current node as red
        if(current_node_id != 0):
            current_node.set_color(YELLOW, sc)
            # if(current_node_id > 1):
                # father.set_color(RED, sc)
            pygame.time.delay(10)
            pygame.display.update()
            current_node.set_color(RED, sc)
            
            

        for neighbor in g.get_neighbors(current_node):
            neighbor_id = neighbor.id
            if neighbor_id not in open_set and neighbor_id not in closed_set:
                open_set.append(neighbor_id)  # Enqueue the neighbor
                father[neighbor_id] = current_node_id
                

        closed_set.append(current_node_id)
    
    return None

    # raise NotImplementedError('not implemented')

def UCS(g: SearchSpace, sc: pygame.Surface):
    # Start the execution timer
    start = t.time()
    
    print('Implement UCS algorithm')

    # +1 respect if you can implement UCS with a priority queue
    open_set = [(0, g.start.id)]
    closed_set = set()
    father = [-1]*g.get_length()
    cost = [100000]*g.get_length()
    cost[g.start.id] = 0
    nn_cost = 0

    while (open_set):
        curr_cost, curr_node_id = heapq.heappop(open_set)
        
        if curr_node_id == g.goal.id:
            path =[]
            print("Total cost:", curr_cost + 1)
            
            while curr_node_id != -1:
                print(f"Adding node {curr_node_id} to the path")
                path.append(curr_node_id)
                curr_node_id = father[curr_node_id]
            path.reverse()
            print("Path reconstructed:", path)
            
            
            for index, node_id in enumerate(path):
                if(0 < index < len(path) - 1):
                    g.grid_cells[node_id].set_color(BLUE, sc)
            end = t.time() 
            print("The time of execution of above program is :", (end-start) * 10**3, "ms")
            return path
    
        if curr_node_id in closed_set:
            continue
        
        curr_node = g.grid_cells[curr_node_id]
        if(curr_node_id != 0):
            curr_node.set_color(YELLOW, sc)
            pygame.time.delay(1)
            pygame.display.update()
            curr_node.set_color(RED, sc)
        
        
        closed_set.add(curr_node_id)
    
        for nn in g.get_neighbors(curr_node):
            nn_id = nn.id
            if nn not in closed_set:
                nn_cost = cost[curr_node_id] + 1
                
                if nn_cost < cost[nn_id]:
                    cost[nn_id] = nn_cost
                    father[nn_id] = curr_node_id
                    heapq.heappush(open_set, (nn_cost, nn_id))
                    
    return None
    # raise NotImplementedError('not implemented')

def AStar(g: SearchSpace, sc: pygame.Surface):
    print('Implement AStar algorithm')

    # +1 respect if you can implement AStar with a priority queue
    open_set = [(0, g.start.id)]
    closed_set = set()
    father = [-1]*g.get_length()
    g_cost = [float('inf')] * g.get_length()
    h_cost = [float('inf')] * g.get_length()
    f_cost = [float('inf')] * g.get_length()
    g_cost[g.start.id] = 0

    # Define a heuristic function, e.g., Manhattan distance algorithm (L1 distance, city block distance)
    def heuristic(node, goal_node):
        x1, y1 = node.id % COLS, node.id // COLS
        x2, y2 = goal_node.id % COLS, goal_node.id // COLS
        return abs(x1 - x2) + abs(y1 - y2)  
        
    # Define a heuristic function, e.g., Diagonal distance algorithm 
    def heuristic2 (node, goal_node):
        x1, y1 = node.id % COLS, node.id // COLS
        x2, y2 = goal_node.id % COLS, goal_node.id // COLS
        
        dx, dy = abs(x1-x2), abs(y1-y2)
        
        return (dx + dy) + (math.sqrt(2) - 2) * min(dx,dy)

    # Define a heuristic function, e.g., Euclide distance algorithm 
    def euclide (node, goal_node):
        x1, y1 = node.id % COLS, node.id // COLS
        x2, y2 = goal_node.id % COLS, goal_node.id // COLS
        
        return math.sqrt((x1 -x2)**2 + (y1-y2)** 2)

    def get_distance(node1, node2):
        x1, y1 = node1.id % COLS, node1.id // COLS
        x2, y2 = node2.id % COLS, node2.id // COLS
        if(x1 == x2 or y1 == y2):
            return 1
        else:
            return 1.4

    while open_set:
        # Get the node with the lowest f-cost from the priority queue
        current_f_cost, current_node_id = heapq.heappop(open_set)

        if current_node_id == g.goal.id:
            path = []
            print("Total cost: ", current_f_cost + 1)
            while current_node_id != -1:
                print(f"Adding node {current_node_id} to the path")
                path.append(current_node_id)
                current_node_id = father[current_node_id]
            path.reverse()
            print("Path reconstructed:", path)

            for index, node_id in enumerate(path):
                if 0 < index < len(path) - 1:
                    g.grid_cells[node_id].set_color(BLUE, sc)
            return path

        if current_node_id in closed_set:
            continue
        
        current_node = g.grid_cells[current_node_id]
        if current_node_id != 0:
            current_node.set_color(YELLOW, sc)
            pygame.time.delay(10)
            pygame.display.update()
            current_node.set_color(RED, sc)

        closed_set.add(current_node_id)

        for neighbor in g.get_neighbors(current_node):
            neighbor_id = neighbor.id
            tentative_g_cost = g_cost[current_node_id] + get_distance(current_node, neighbor)

            if tentative_g_cost < g_cost[neighbor_id]:
                if neighbor_id not in open_set and neighbor_id not in closed_set:
                    father[neighbor_id] = current_node_id
                    g_cost[neighbor_id] = tentative_g_cost
                    h_cost[neighbor_id] = euclide(neighbor, g.goal)
                    f_cost[neighbor_id] = g_cost[neighbor_id] + h_cost[neighbor_id]
                    heapq.heappush(open_set, (f_cost[neighbor_id], neighbor_id))

    return None


    # raise NotImplementedError('not implemented')
