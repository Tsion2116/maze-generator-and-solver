# Maze Generator and Solver

## Overview

This project is a maze generator and solver built using Python and Pygame. The maze is created using a Depth-First Search (DFS) algorithm, where a “mouse” moves through the grid, carving paths by removing walls between cells. The mouse keeps track of its path using a stack, allowing it to backtrack when it reaches a dead end.
After the maze is generated, a solver traverses the maze from the entrance to the exit using a similar backtracking approach.

## Data Structure

Following the assignment specifications:
- northWall[R+1][C] → 1 = wall exists ABOVE cell (row, col)
- eastWall[R][C+1]  → 1 = wall exists RIGHT of cell (row, col)


•	Phantom row (index R): Stores bottom edge walls
•	Phantom column (index C): Stores right edge walls
•	Left edge openings: Controlled by eastWall[row][0]
•	Bottom edge openings: Controlled by northWall[R][col]

## How the Maze Generator Works

The generator uses a stack-based DFS algorithm (the "mouse"):
1.	Start from a random cell, mark as visited
2.	Find all unvisited neighboring cells
3.	Choose one randomly, eat the wall between them
4.	Push the chosen cell onto the stack
5.	If no unvisited neighbors exist, pop from stack (backtrack)
6.	Repeat until stack is empty
This creates a proper maze (tree structure) where every cell is connected by a unique path.

## Stack vs Queue (Assignment Question)

Stack (DFS) - Used in this project:
•	Explores one path deeply before backtracking
•	Creates long, winding corridors
•	Produces traditional "maze-like" structures

Queue (BFS) - If used instead:
•	Explores outward in layers
•	Creates short, branching paths
•	Results in a more "grid-like" appearance
•	Less suitable for maze generation

## Features
•	Random maze generation using DFS
•	Proper maze guarantee (all cells connected)
•	Backtracking maze solver
• Configurable entrance/exit placement
• Two entrance modes:
  - Boundary Mode: entrance on left edge, exit on right edge
  - Interior Mode: entrance and exit generated inside the maze

## Visual Indicators

| Element                        | Color         |
|--------------------------------|---------------|
| Visited cells (generation)     | Pale purple   |
| Current DFS cell               | Red           |
| Current position (solver)      | Green         |
| Dead ends                      | Blue          |
| Solution path                  | Yellow        |
| Start cell                     | Start         |
| End cell                       | Green/End     |
| Walls                          | Black         |

## Controls

| Action                     | Key                  |
|----------------------------|----------------------|
| Increase animation speed   | `Page Up`            |
| Decrease animation speed   | `Page Down`          |
| Restart the maze           | `R`                  |
| Toggle entrance mode       | SPACE                |

## Installation Requirements

•	Python 3.7+
•	Pygame

## Setup
- pip install pygame
- python main.py

