# Pygame Physics Simulator

## Overview
This is an interactive physics simulator built with pygame and pygame_gui. It allows users to spawn physics objects and static objects, configure their properties (mass, dimensions, velocity, gravity), and observe realistic physics interactions including collisions, gravity, and momentum transfer.

## Project Structure
- `Main.py` - Main application with the game loop, UI buttons, and simulation controls
- `Classes.py` - Object classes including `physics_obj` (dynamic objects affected by physics) and `static_obj` (immovable objects)
- `Window.py` - Property editor windows that appear when double-clicking objects
- `Constants.py` - Global constants (screen dimensions, pixels per meter, etc.)
- `requirements.txt` - Python dependencies

## Features
- **Spawn Physics Objects**: Create dynamic objects affected by gravity and collisions
- **Spawn Static Objects**: Create immovable obstacles
- **Drag & Drop**: Move objects around before starting the simulation
- **Property Editor**: Double-click any object to edit its properties in real-time:
  - Mass
  - Width and Height
  - Initial velocities (X and Y)
  - Gravity force (per object)
- **Start/Reset**: Control the simulation with Start and Reset buttons
- **Collision Detection**: Realistic collision handling with momentum transfer
- **Ground Plane**: Pre-configured ground at the bottom of the screen

## Setup
The project has been configured to run in the Replit environment with:
- Python 3.11
- pygame-ce 2.5.2 (Community Edition)
- pygame_gui 0.6.12
- VNC output for GUI display

## How to Use
1. The application opens with a control panel on the left side
2. Click "Spawn Physic Object" or "Spawn Static Object" to create objects
3. Drag objects to position them before starting
4. Double-click objects to edit their properties
5. Click "Start" to begin the physics simulation
6. Click "Reset" to stop and return all objects to their initial positions

## Physics Details
- Gravity: Configurable per object (default 9.81 m/s²)
- Scale: 30 pixels = 1 meter
- Collision detection with momentum transfer
- Realistic velocity and acceleration calculations

## Recent Changes
- 2025-11-05: Setup in Replit environment from dev branch
  - Installed Python 3.11 module
  - Configured pygame-ce and pygame_gui dependencies (stable versions)
  - Set up VNC workflow for GUI display
  - Created project documentation
