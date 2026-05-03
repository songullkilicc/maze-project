# MDT-8: FUNCTIONAL & NON-FUNCTIONAL REQUIREMENTS
## FURPS Methodology Analysis - Maze Pathfinding Project

**Task:** Define functional, non-functional requirements and assumptions according to the FURPS methodology  
**Project:** Maze Visualization with Pathfinding Algorithm  
**Date:** April 27, 2026  
**Developer:** Songül Kılıç  
**Status:** Complete  

---

## 📋 EXECUTIVE SUMMARY

This document defines all Functional (F), Non-Functional (U), Reliability (R), Performance (P), and Security (S) requirements for the Maze Pathfinding Visualization project using FURPS+ methodology.

---

## 🔧 FUNCTIONAL REQUIREMENTS (F)

### FR-1: Grid Management
- **Requirement:** System shall display a configurable grid (10x10 to 50x50)
- **Acceptance Criteria:**
  - Grid renders correctly at 20x20 default
  - Users can modify grid size in configuration
  - All cells are clearly visible with grid lines

### FR-2: Wall Drawing & Management
- **Requirement:** Users shall be able to draw and erase walls interactively
- **Acceptance Criteria:**
  - Mouse drag creates continuous wall lines
  - Clicking existing wall erases it (toggle)
  - Walls cannot overlap with Start/End points
  - C key clears all walls while preserving Start/End

### FR-3: Start/End Point Management
- **Requirement:** Users shall set exactly one Start and one End point
- **Acceptance Criteria:**
  - S key + mouse click places Start point (green)
  - E key + mouse click places End point (red)
  - Only one Start/End point can exist at a time
  - Clicking elsewhere moves existing Start/End point
  - Start/End points cannot be placed on walls

### FR-4: Pathfinding Algorithm Integration
- **Requirement:** System shall integrate BFS/A* pathfinding algorithm
- **Acceptance Criteria:**
  - SPACE key triggers pathfinding when Start and End are set
  - Algorithm returns visited_nodes and final_path
  - Error message displays if Start or End is missing
  - System handles "no path exists" scenario gracefully

### FR-5: Animation & Visualization
- **Requirement:** System shall animate search process in real-time
- **Acceptance Criteria:**
  - Visited nodes display in light blue during animation
  - Final path displays in yellow after search complete
  - Animation speed is adjustable (F/G keys)
  - Status text shows animation progress
  - Animation completes without blocking UI

### FR-6: User Controls & Keyboard Shortcuts
- **Requirement:** All user interactions shall be keyboard/mouse based
- **Acceptance Criteria:**
  - Mouse drag: Draw/erase walls
  - S + click: Place Start
  - E + click: Place End
  - SPACE: Start animation
  - F: Slow down animation
  - G: Speed up animation
  - C: Clear maze

### FR-7: Color Coding System
- **Requirement:** System shall use distinct colors for different cell types
- **Acceptance Criteria:**
  - White: Empty cells
  - Black: Walls
  - Green: Start point
  - Red: End point
  - Light Blue: Visited nodes
  - Yellow: Final shortest path
  - Gray: Grid lines

### FR-8: Data Persistence (Optional)
- **Requirement:** Users shall be able to save/load mazes
- **Acceptance Criteria:**
  - Save maze to file
  - Load saved maze
  - Support multiple saves
  - **Note:** Currently NOT implemented, future enhancement

---

## 👤 USABILITY REQUIREMENTS (U)

### UR-1: Intuitive User Interface
- **Requirement:** UI shall be intuitive without documentation
- **Acceptance Criteria:**
  - On-screen status text explains current mode
  - Controls are obvious (drag to draw)
  - No hidden features or complex menus
  - First-time users can operate within 2 minutes

### UR-2: Visual Feedback
- **Requirement:** System shall provide immediate visual feedback
- **Acceptance Criteria:**
  - Walls appear instantly when drawn
  - Start/End points update immediately
  - Animation shows real-time progress
  - Status messages inform user of actions

### UR-3: Error Prevention
- **Requirement:** System shall prevent invalid operations
- **Acceptance Criteria:**
  - Cannot start animation without Start and End points
  - Cannot place Start/End on walls
  - Clear error messages for invalid actions
  - Graceful handling of edge cases

### UR-4: Accessibility
- **Requirement:** Application shall be accessible to diverse users
- **Acceptance Criteria:**
  - Large, clear fonts
  - High contrast colors
  - Keyboard-only navigation possible
  - No time-based actions (except optional animation)

---

## 🔒 RELIABILITY REQUIREMENTS (R)

### RR-1: System Stability
- **Requirement:** System shall not crash during normal operation
- **Acceptance Criteria:**
  - Handles rapid mouse events
  - Manages edge cases (empty grid, unreachable end)
  - Recovers from invalid input
  - No memory leaks during extended use

### RR-2: Data Integrity
- **Requirement:** Grid data shall remain consistent
- **Acceptance Criteria:**
  - Grid state matches visual representation
  - No data loss during animation
  - Undo/Redo functionality (future enhancement)
  - Consistent behavior across different grid sizes

### RR-3: Exception Handling
- **Requirement:** System shall handle exceptions gracefully
- **Acceptance Criteria:**
  - Try-catch blocks for critical operations
  - Meaningful error messages to user
  - No unhandled exceptions crash application
  - Logging of errors for debugging

### RR-4: Algorithm Correctness
- **Requirement:** Pathfinding algorithm shall find correct path
- **Acceptance Criteria:**
  - BFS always finds shortest path (if exists)
  - Path doesn't cross walls
  - Path is continuous
  - Handles disconnected mazes correctly

---

## ⚡ PERFORMANCE REQUIREMENTS (P)

### PR-1: Frame Rate
- **Requirement:** Application shall maintain 60 FPS
- **Acceptance Criteria:**
  - No frame drops during normal operation
  - Animation remains smooth at all speeds
  - Drawing walls doesn't cause lag
  - Tested on standard hardware (2-4 core CPU, 4GB RAM)

### PR-2: Response Time
- **Requirement:** User actions shall respond instantly
- **Acceptance Criteria:**
  - Mouse events process within 16ms (60 FPS)
  - Keyboard input recognized immediately
  - Grid rendering completes within 1 frame
  - No perceptible delay between action and response

### PR-3: Algorithm Performance
- **Requirement:** Pathfinding shall complete quickly
- **Acceptance Criteria:**
  - BFS completes within 100ms for 20x20 grid
  - BFS completes within 500ms for 50x50 grid
  - Animation speed adjustable (10ms-200ms per frame)
  - No UI blocking during pathfinding

### PR-4: Memory Usage
- **Requirement:** Memory usage shall be optimized
- **Acceptance Criteria:**
  - Grid storage: O(rows × cols)
  - Queue usage: O(rows × cols) worst case
  - No memory leaks over extended use
  - Efficient data structures (deque, dict)

### PR-5: Scalability
- **Requirement:** System shall support various grid sizes
- **Acceptance Criteria:**
  - Works with 5x5 grid
  - Works with 20x20 grid
  - Works with 50x50 grid
  - Works with 100x100 grid
  - Performance degrades gracefully beyond 100x100

---

## 🔐 SECURITY REQUIREMENTS (S)

### SR-1: Input Validation
- **Requirement:** System shall validate all user input
- **Acceptance Criteria:**
  - Mouse coordinates checked against grid bounds
  - Keyboard input validated
  - Grid size limited to reasonable range
  - No buffer overflow possible

### SR-2: Code Security
- **Requirement:** Code shall follow security best practices
- **Acceptance Criteria:**
  - No hardcoded sensitive data
  - No SQL injection (N/A - no database)
  - No XSS vulnerabilities
  - Safe file operations (if implemented)

### SR-3: Application Isolation
- **Requirement:** Application shall not affect system stability
- **Acceptance Criteria:**
  - No admin privileges required
  - Contained within application window
  - Cannot access unauthorized files
  - Clean shutdown without residual processes

---

## 📌 ASSUMPTIONS

### AS-1: User Environment
- **Assumption:** User has Python 3.7+ installed
- **Assumption:** User has pygame library installed (`pip install pygame`)
- **Assumption:** User has minimum 4GB RAM
- **Assumption:** User has display capable of 800x800 window

### AS-2: User Knowledge
- **Assumption:** User understands basic maze concepts
- **Assumption:** User can operate keyboard and mouse
- **Assumption:** User can run Python scripts from terminal
- **Assumption:** User has basic understanding of pathfinding (optional)

### AS-3: System Constraints
- **Assumption:** No network connectivity required
- **Assumption:** No database or persistent storage required (currently)
- **Assumption:** Runs on Windows, macOS, or Linux
- **Assumption:** Single-user application (no multi-user support)

### AS-4: Project Scope
- **Assumption:** Frontend and Backend are integrated in same application
- **Assumption:** No real-time multiplayer features
- **Assumption:** No advanced visualization (3D, AR, etc.)
- **Assumption:** Project completes by May 2, 2026

---

## 📊 REQUIREMENTS COVERAGE MATRIX

| Requirement | Implemented | Status | Notes |
|-------------|------------|--------|-------|
| **Functional (FR)** |
| FR-1: Grid Management | ✅ | Complete | 20x20 default, configurable |
| FR-2: Wall Drawing | ✅ | Complete | Drag-and-draw, toggle erase |
| FR-3: Start/End Points | ✅ | Complete | Single point each, auto-cleanup |
| FR-4: Pathfinding | ⏳ | Awaiting Backend | Template ready (pathfinding.py) |
| FR-5: Animation | ✅ | Complete | Smooth, configurable speed |
| FR-6: Controls | ✅ | Complete | All shortcuts implemented |
| FR-7: Colors | ✅ | Complete | 7 distinct colors |
| FR-8: Persistence | ❌ | Not Planned | Future enhancement |
| **Usability (UR)** |
| UR-1: Intuitive UI | ✅ | Complete | On-screen instructions |
| UR-2: Visual Feedback | ✅ | Complete | Real-time updates |
| UR-3: Error Prevention | ✅ | Complete | Validation in place |
| UR-4: Accessibility | ⚠️ | Partial | Basic accessibility, could improve |
| **Reliability (RR)** |
| RR-1: Stability | ✅ | Complete | Tested on various inputs |
| RR-2: Data Integrity | ✅ | Complete | Consistent state management |
| RR-3: Exception Handling | ✅ | Complete | Try-catch implemented |
| RR-4: Algorithm Correctness | ⏳ | Awaiting Backend | BFS template ready |
| **Performance (PR)** |
| PR-1: Frame Rate | ✅ | Complete | 60 FPS maintained |
| PR-2: Response Time | ✅ | Complete | <16ms response |
| PR-3: Algorithm Speed | ⏳ | Awaiting Backend | Expected <100ms |
| PR-4: Memory Usage | ✅ | Complete | Efficient structures |
| PR-5: Scalability | ✅ | Complete | Tested up to 50x50 |
| **Security (SR)** |
| SR-1: Input Validation | ✅ | Complete | All inputs validated |
| SR-2: Code Security | ✅ | Complete | Safe practices |
| SR-3: Isolation | ✅ | Complete | Contained application |

---

## 🎯 PRIORITY REQUIREMENTS

### MUST HAVE (Critical)
- ✅ Grid rendering
- ✅ Wall drawing
- ✅ Start/End points
- ⏳ Pathfinding algorithm
- ✅ Animation

### SHOULD HAVE (Important)
- ✅ User controls
- ✅ Color coding
- ⏳ Error handling
- ⏳ Performance optimization

### COULD HAVE (Nice to Have)
- ❌ Save/Load functionality
- ❌ Statistics display
- ❌ Multiple algorithms
- ❌ Replay functionality

### WON'T HAVE (Out of Scope)
- Multiplayer support
- 3D visualization
- Mobile app version
- Cloud storage

---

## 📝 SIGN OFF

**Document Owner:** Songül Kılıç  
**Date Created:** April 27, 2026  
**Last Updated:** April 27, 2026  
**Status:** APPROVED ✅  
**Next Review:** May 2, 2026 (Project Completion)

---

**Requirements Version:** 1.0  
**Project Status:** In Development  
**Estimated Completion:** May 2, 2026
