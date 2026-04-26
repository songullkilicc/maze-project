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

### Frontend (Songül) - COMPLETE ✅
- Task 1: GUI & Grid Rendering ✅
- Task 2: User Input & Interaction ✅
- Task 3: Animation Engine ✅

### Backend (Bouchra) - IN PROGRESS ⏳
- Task 2: Pathfinding Algorithm (BFS/A*)
- Task 3: Path Reconstruction

### Integration Status
⏳ Waiting for backend pathfinding implementation
📅 Expected: April 28, 2026
🔗 Ready to integrate immediately upon completion

---

## How to Contribute

If you're Bouchra:
1. Implement `find_path_bfs()` in `pathfinding.py`
2. Return format: `(visited_nodes, final_path)`
3. Push to GitHub
4. Notify Songül for integration

Frontend is fully documented and ready!

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
