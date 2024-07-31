#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 12:41:54 2022

@author: dan
"""
# VERSION WITH NO AI

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import csv
import random

print ("Dan is awesome")

# np array to store true treasure probability values (initiated at 0 for all
# cells, but we will read in the actual values from a .csv file)
true_treasure_vals = np.array([ 
    [0.0,0.0,0.0,0.0,0.0],
    [0.0,0.0,0.0,0.0,0.0],
    [0.0,0.0,0.0,0.0,0.0],
    [0.0,0.0,0.0,0.0,0.0],
    [0.0,0.0,0.0,0.0,0.0]
    ])

# read in the treasure probability values and overwrite the values above
with open("treasure_grid.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    
    current_row = 0
    
    for row in reader:
        true_treasure_vals[current_row][0] = row[0]
        true_treasure_vals[current_row][1] = row[1]
        true_treasure_vals[current_row][2] = row[2]
        true_treasure_vals[current_row][3] = row[3]
        true_treasure_vals[current_row][4] = row[4]
        
        current_row += 1

# np array to store the estimated treasure probability for each cell
treasure_estimate = np.array([ 
    [0.0,0.0,0.0,0.0,0.0],
    [0.0,0.0,0.0,0.0,0.0],
    [0.0,0.0,0.0,0.0,0.0],
    [0.0,0.0,0.0,0.0,0.0],
    [0.0,0.0,0.0,0.0,0.0]
    ])

# np array to store the number of digs made in each cell
treasure_digs = np.array([ 
    [0.0,0.0,0.0,0.0,0.0],
    [0.0,0.0,0.0,0.0,0.0],
    [0.0,0.0,0.0,0.0,0.0],
    [0.0,0.0,0.0,0.0,0.0],
    [0.0,0.0,0.0,0.0,0.0]
    ])

# np array to store the number of successful digs made in each cell
treasure_successes = np.array([ 
    [0.0,0.0,0.0,0.0,0.0],
    [0.0,0.0,0.0,0.0,0.0],
    [0.0,0.0,0.0,0.0,0.0],
    [0.0,0.0,0.0,0.0,0.0],
    [0.0,0.0,0.0,0.0,0.0]
    ])

# draw grid
# create discrete colormap
cmap = colors.ListedColormap(['white',
                              'lightyellow',
                              'lightgoldenrodyellow',
                              'bisque',
                              'wheat',
                              'orange',
                              'darkorange',
                              'orangered',
                              'red',
                              'deeppink'])
bounds = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
norm = colors.BoundaryNorm(bounds, cmap.N)

fig, ax = plt.subplots()
ax.imshow(treasure_estimate, cmap=cmap, norm=norm)

# draw gridlines
ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
ax.set_xticks(np.arange(-.5, 5, 1));
ax.set_yticks(np.arange(-.5, 5, 1));

ax.set_xticklabels(['A','B','C','D','E'])
ax.set_yticklabels(['1','2','3','4','5'])

for tick in ax.xaxis.get_majorticklabels():
    tick.set_horizontalalignment("left")
    
for tick in ax.yaxis.get_majorticklabels():
    tick.set_verticalalignment("top")
    
ax1 = fig.add_axes([0.85, 0.1, 0.05, 0.8])

cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap,
                                norm=norm,
                                orientation='vertical')

plt.show()

# parameter values
treasure_accumulated = 0
turn_number = 1
previous_cell_chosen = "Z9"

max_turns = 200

# while loop to play game
while turn_number < (max_turns + 1):
    column = 0
    
    print (f"--TURN NUMBER {turn_number}--")
    
    # get user input for chosen cell
    chosen_cell = input("CHOOSE CELL : ")
    
    try:
        # convert user input to coordinates for np array
        if chosen_cell[0] == "A":
            column = 0
        elif chosen_cell[0] == "B":
            column = 1
        elif chosen_cell[0] == "C":
            column = 2
        elif chosen_cell[0] == "D":
            column = 3
        elif chosen_cell[0] == "E":
            column = 4
        else:
            column = 999999 # invalid to trigger error
        
        row = int(chosen_cell[1]) - 1
        
        if row < 0 or row > 4:
            row = 999999 # invalid to trigger error
            
        # if invalid cell entered
        if column == 999999 or row == 999999:
            print ("Cell reference error")
        else:
            # if staying in same cell or this is first move of game
            if (chosen_cell == previous_cell_chosen or 
                previous_cell_chosen == "Z9"):
                
                # determine probability of digging treasure and record a dig
                probability_of_treasure = true_treasure_vals[row][column]
                
                treasure_digs[row][column] += 1.0
                
                # if get treasure, add 1 to treasure and record successs
                if random.uniform(0, 1) < probability_of_treasure:
                    print ("You found treasure!")
                    treasure_accumulated += 1
                    print (f"You now have {treasure_accumulated} units of",
                           "treasure")
                    treasure_successes[row][column] += 1.0
                else:
                    print ("Nothing.")
                    
                # calculate new estimate based on successes divided by total
                # digs in this cell
                treasure_estimate[row][column]=(treasure_successes[row][column]
                                                  /
                                                  treasure_digs[row][column])
                
                # update grid visualisation
                # create discrete colormap
                cmap = colors.ListedColormap(['white',
                              'lightyellow',
                              'lightgoldenrodyellow',
                              'bisque',
                              'wheat',
                              'orange',
                              'darkorange',
                              'orangered',
                              'red',
                              'deeppink'])
                bounds = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
                norm = colors.BoundaryNorm(bounds, cmap.N)
                
                fig, ax = plt.subplots()
                ax.imshow(treasure_estimate, cmap=cmap, norm=norm)
                
                # draw gridlines
                ax.grid(which='major', axis='both', linestyle='-', color='k', 
                        linewidth=2)
                ax.set_xticks(np.arange(-.5, 5, 1));
                ax.set_yticks(np.arange(-.5, 5, 1));
                
                ax.set_xticklabels(['A','B','C','D','E'])
                ax.set_yticklabels(['1','2','3','4','5'])
                
                for tick in ax.xaxis.get_majorticklabels():
                    tick.set_horizontalalignment("left")
                    
                for tick in ax.yaxis.get_majorticklabels():
                    tick.set_verticalalignment("top")
                    
                ax1 = fig.add_axes([0.85, 0.1, 0.05, 0.8])
                
                cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap,
                                                norm=norm,
                                                orientation='vertical')
                
                plt.show()
            else:
                # if moving from another cell, consume a turn to travel
                print (f"You spend 1 turn travelling from",
                       f"{previous_cell_chosen} to {chosen_cell}")
                turn_number += 1
                
                # check if sufficient turns left to dig on arrival
                if turn_number == max_turns:
                    print ("Sorry, you don't have any turns left to dig!")
                else:
                    print (f"--TURN NUMBER {turn_number}--")
                    print (f"You arrive and dig at {chosen_cell}")
                    
                    probability_of_treasure = true_treasure_vals[row][column]
                    
                    treasure_digs[row][column] += 1.0
                    
                    if random.uniform(0, 1) < probability_of_treasure:
                        print ("You found treasure!")
                        treasure_accumulated += 1
                        print (f"You now have {treasure_accumulated} units of",
                               "treasure")
                        treasure_successes[row][column] += 1.0
                    else:
                        print ("Nothing.")
                        
                    treasure_estimate[row][column]=(treasure_successes[row][column]
                                                      /
                                                      treasure_digs[row][column])
                    
                    # update grid visualisation
                    # create discrete colormap
                    cmap = colors.ListedColormap(['white',
                                  'lightyellow',
                                  'lightgoldenrodyellow',
                                  'bisque',
                                  'wheat',
                                  'orange',
                                  'darkorange',
                                  'orangered',
                                  'red',
                                  'deeppink'])
                    bounds = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
                    norm = colors.BoundaryNorm(bounds, cmap.N)
                    
                    fig, ax = plt.subplots()
                    ax.imshow(treasure_estimate, cmap=cmap, norm=norm)
                    
                    # draw gridlines
                    ax.grid(which='major', axis='both', linestyle='-', color='k', 
                            linewidth=2)
                    ax.set_xticks(np.arange(-.5, 5, 1));
                    ax.set_yticks(np.arange(-.5, 5, 1));
                    
                    ax.set_xticklabels(['A','B','C','D','E'])
                    ax.set_yticklabels(['1','2','3','4','5'])
                    
                    for tick in ax.xaxis.get_majorticklabels():
                        tick.set_horizontalalignment("left")
                        
                    for tick in ax.yaxis.get_majorticklabels():
                        tick.set_verticalalignment("top")
                        
                    ax1 = fig.add_axes([0.85, 0.1, 0.05, 0.8])
                    
                    cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap,
                                                    norm=norm,
                                                    orientation='vertical')
                    
                    plt.show()
            
            # print current table of estimated probabilities
            print (treasure_estimate)
            
            # record cell as being previous chosen, and increment turn number
            previous_cell_chosen = chosen_cell
            turn_number += 1
    except:
        # catch exceptions in user input
        print ("Cell reference error")

# print final total
print (f"*** FINAL TOTAL = {treasure_accumulated} units of treasure collected")

