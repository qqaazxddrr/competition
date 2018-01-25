#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 00:07:52 2017

@author: gaokuang
"""

import math, heapq
import scipy.io as sio
import numpy as np
import csv
import pandas as pd
from datetime import *

# Adjust the size of the board and the cells
cell_size = 1
X_cells = 548
Y_cells=421

start = None
goal = None

result=[]

cells = {}      # Dictionary of Cells where a tuple (immutable set) of (x,y) coordinates is used as keys

for x in range(X_cells):
    for y in range(Y_cells):
        cells[(x,y)]= { 'state':None,   # None, Wall, Goal, Start Are the possible states. None is walkable 
                        'f_score':None, # f() = g() + h() This is used to determine next cell to process
                        'h_score':None, # The heuristic score, We use straight-line distance: sqrt((x1-x0)^2 + (y1-y0)^2)
                        'g_score':None, # The cost to arrive to this cell, from the start cell
                        'parent':None}  # In order to walk the found path, keep track of how we arrived to each cell

open_list = []      # our priority queue of opened cells' f_scores

pq_dict = {}   
             
closed_list = {}    # A dictionary of closed cells

# This allows for the dynamic changing of the chosen heuristic
heuristic = 'manhattan' # Could be 'manhattan' or 'crow' anything else is assumed to be 'zero'

def calc_f(node):
    cells[node]['f_score'] = cells[node]['h_score'] + cells[node]['g_score']

def calc_h(node):
    global heuristic
    x1, y1 = goal
    x0, y0 = node
    if heuristic == 'manhattan':
        cells[node]['h_score'] = (abs(x1-x0)+abs(y1-y0))*10#
    elif heuristic == 'crow':
        cells[node]['h_score'] = math.sqrt( (x1-x0)**2 + (y1-y0)**2 )*10
    else:
        cells[node]['h_score'] = 0

def onBoard(node):
    x, y = node
    return x >= 0 and x < X_cells and y >= 0 and y < Y_cells


# Return a list of adjacent orthoganal walkable cells 

def orthoganals(current):
    x, y = current
    
    N = x-1, y
    E = x, y+1
    S = x+1, y
    W = x, y-1
    
    directions = [N, E, S, W]
    return [x for x in directions if onBoard(x) and cells[x]['state'] != 'Wall' and not x in closed_list]

# Check if diag is blocked by a wall, making it unwalkable from current

def blocked_diagnol(current,diag):
    x, y = current
    
    N = x-1, y
    E = x, y+1
    S = x+1, y
    W = x, y-1
    NE = x-1, y+1
    SE = x+1, y+1
    SW = x+1, y-1
    NW = x-1, y-1
    
    if diag == NE:
        return cells[N]['state'] == 'Wall' or cells[E]['state'] == 'Wall'
    elif diag == SE:
        return cells[S]['state'] == 'Wall' or cells[E]['state'] == 'Wall'
    elif diag == SW:
        return cells[S]['state'] == 'Wall' or cells[W]['state'] == 'Wall'
    elif diag == NW:
        return cells[N]['state'] == 'Wall' or cells[W]['state'] == 'Wall'
    else:
        return False # Technically, you've done goofed if you arrive here.

# Return a list of adjacent diagonal walkable cells

def diagonals(current):
    x, y = current
    
    NE = x-1, y+1
    SE = x+1, y+1
    SW = x+1, y-1
    NW = x-1, y-1
    
    directions = [NE, SE, SW, NW]
    return [x for x in directions if onBoard(x) and cells[x]['state'] != 'Wall' and not x in closed_list and not blocked_diagnol(current,x)]

# Update a child node with information from parent, such as g_score and the parent's coords

def update_child(parent, child, cost_to_travel):
    cells[child]['g_score'] = cells[parent]['g_score'] + cost_to_travel
    cells[child]['parent'] = parent


# Display the shortest path found

def unwind_path(coord):
    if cells[coord]['parent'] != None:
        left, top = coord
#        print(str(left)+','+str(top))
        result.append(left)
        result.append(top)
        unwind_path(cells[coord]['parent'])


# Recursive function to process the current node, which is the node with the smallest f_score from the list of open nodes

def processNode(coord):
    global goal, open_list, closed_list, pq_dict, board, screen, needs_refresh
    if coord == goal:
        print "Cost %d\n" % cells[goal]['g_score']
        unwind_path(cells[goal]['parent'])
        return
        
    # l will be a list of walkable adjacents that we've found a new shortest path to
    l = [] 
    
#    # Check all of the diagnols for walkable cells, that we've found a new shortest path to
#    for x in diagonals(coord):
#        # If x hasn't been visited before
#        if cells[x]['g_score'] == None:
#            update_child(coord, x, cost_to_travel=14)
#            l.append(x)
#        # Else if we've found a faster route to x
#        elif cells[x]['g_score'] > cells[coord]['g_score'] + 14:
#            update_child(coord, x, cost_to_travel=14)
#            l.append(x)
    
    for x in orthoganals(coord):
        # If x hasn't been visited before
        if cells[x]['g_score'] == None:
            update_child(coord, x, cost_to_travel=10)
            l.append(x)
        # Else if we've found a faster route to x
        elif cells[x]['g_score'] > cells[coord]['g_score'] + 10:
            update_child(coord, x, cost_to_travel=10)
            l.append(x)
    
    for x in l:
            
        # If we found a shorter path to x
        # Then we remove the old f_score from the heap and dictionary
        if cells[x]['f_score'] in pq_dict:
            if len(pq_dict[cells[x]['f_score']]) > 1:
                pq_dict[cells[x]['f_score']].remove(x)
            else:
                pq_dict.pop(cells[x]['f_score'])
            open_list.remove(cells[x]['f_score'])
        # Update x with the new f and h score (technically don't need to do h if already calculated)
        calc_h(x)
        calc_f(x)
        # Add f to heap and dictionary
        open_list.append(cells[x]['f_score'])
        if cells[x]['f_score'] in pq_dict:
            pq_dict[cells[x]['f_score']].append(x)
        else:
            pq_dict[cells[x]['f_score']] = [x]
    
    heapq.heapify(open_list)
    

    if len(open_list) == 0:
        print 'NO POSSIBLE PATH!'
        return
    f = heapq.heappop(open_list)
    if len(pq_dict[f]) > 1:
        node = pq_dict[f].pop()
    else:
        node = pq_dict.pop(f)[0]
    
    heapq.heapify(open_list)
    closed_list[node]=True

    processNode(node)

# Start the search for the shortest path from start to goal

def findPath(start_tuple,goal_tuple,pic):
    global start,goal
    start=start_tuple
    goal=goal_tuple
    cells[start]['state']='Start'
    cells[goal]['state']='goal'
    cells[start]['g_score'] = 0
    for x_index in range(548):
        for y_index in range(421):
            if pic[x_index,y_index]==1:
                cells[(x_index, y_index)]['state']='Wall'
    calc_h(start)
    calc_f(start)
        

    closed_list[start]=True
    processNode(start)
    tmp=np.array(result).reshape(len(result)/2,2)
    tmp=tmp[::-1].tolist()
    tmp.insert(0,[start[0],start[1]])
    tmp.append([goal[0],goal[1]])
    return tmp
  

    

    
if __name__ == "__main__":   
    
    London=[142,328]
    cityX=125
    cityY=375
    data=sio.loadmat('testingDataFusion.mat')
    data=data['outputData']
    data=np.where(data>=15,1,0)
    data=data.reshape(90,548,421)
    
    a=findPath((142,328),(125,375),data[0])
#    
#    
#    pic=data[0]
#    cityX=[84,199,140,236,315,358,363,423,125,189]
#    cityY=[203,371,234,241,281,207,237,266,375,274]
#    
#    start = (London[0], London[1])
#    goal = (cityX[8], cityY[8])
#    cells[start]['state']='Start'
#    cells[goal]['state']='goal'
#    
#    for x_index in range(548):
#        for y_index in range(421):
#            if pic[x_index,y_index]==1:
#                cells[(x_index, y_index)]['state']='Wall'
#    a=findPath()
    

    
#    with open('test.csv', 'wb') as f:
#        writer = csv.writer(f)
#        for row in result:
#            writer.writerow(row)