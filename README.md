# Maze Visualization Project

## Overview
This project is a grid-based maze visualization tool built with Python and Pygame.  
It allows users to create a maze and visualize a pathfinding process.

## Features
- Grid rendering system
- Draw/erase walls with mouse
- Set Start (S) and End (E) nodes
- Press SPACE to trigger animation

## Technologies
- Python
- Pygame

## How to Run
pip install pygame  
python main.py

## Current Status
**Task 1 & Task 3 (Frontend) - COMPLETED:**
✅ GUI and grid system implemented  
✅ User interaction completed (drag-and-draw, S/E/C keys)  
✅ Animation engine implemented with configurable speed (F/G keys)
✅ Final path color differentiation (yellow)
✅ Status text display on screen

**Task 2 (Backend) - IN PROGRESS:**
⏳ BFS/A* pathfinding algorithm (Bouchra)
⏳ Path reconstruction logic (Bouchra)

**Ready for:** Backend integration (expected April 28)

## Future Work
✅ Animation engine implemented  
⏳ Integrate BFS / A* algorithm (waiting for backend)
⏳ Visualize real visited nodes data  
⏳ Implement shortest path rendering with final path data

## Demo
<img width="622" height="657" alt="teamproj3" src="https://github.com/user-attachments/assets/60770f02-fe32-4052-83d5-0aef71b65f9e" />
https://github.com/user-attachments/assets/2389ccd6-d1a3-47fe-b040-5f8c12bffb78
+ after changing the main.py to new version: (Note: The animation system is implemented and ready. 
It will be activated once the backend pathfinding algorithm provides visited_nodes data.)
 <img width="887" height="186" alt="image" src="https://github.com/user-attachments/assets/904f3783-c139-44f4-9741-a2465620104a" />

## Controls
| Key | Action |
|-----|--------|
| Mouse Drag | Draw/Erase walls |
| S + Click | Place START point |
| E + Click | Place END point |
| SPACE | Start animation |
| F | Slow down animation |
| G | Speed up animation |
| C | Clear maze | 

## Author
Songül Kılıç
