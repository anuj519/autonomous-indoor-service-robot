# Autonomous Indoor Service Robot (ROS2)

## Overview

This project is a portfolio-focused autonomous robotics system built using **ROS2 Humble** and **Gazebo**. The long-term goal is to develop an autonomous indoor service robot capable of mapping unknown environments, localizing itself, planning safe paths, and completing multi-goal missions in custom environments.

The project is being developed incrementally to gain experience with modern robotics software while creating a portfolio piece relevant to robotics software engineering, autonomous systems, and perception roles.

---

## Current Features

* ROS2 Humble development environment
* TurtleBot3 simulation in Gazebo
* Keyboard teleoperation
* LiDAR-based SLAM using SLAM Toolbox
* Occupancy grid map generation
* Map saving
* AMCL localization
* Nav2 autonomous navigation
* Goal-based path planning

---

## Technologies

* ROS2 Humble
* Gazebo
* TurtleBot3
* SLAM Toolbox
* Nav2
* AMCL
* RViz2
* Ubuntu 22.04

---

## Roadmap

### Phase 1 (Completed)

* [x] Install and configure ROS2
* [x] Launch TurtleBot3 simulation
* [x] Implement teleoperation
* [x] Perform SLAM mapping
* [x] Save occupancy grid maps
* [x] Configure localization (AMCL)
* [x] Implement autonomous navigation

### Phase 2 (In Progress)

* [ ] Create custom indoor environment
* [ ] Improve navigation robustness
* [ ] Add multi-waypoint missions
* [ ] Evaluate navigation performance

### Phase 3 (Planned)

* [ ] Autonomous task execution
* [ ] Dynamic obstacle avoidance
* [ ] Behavior tree mission planning
* [ ] Object detection integration
* [ ] Raspberry Pi deployment (optional)

---

## Motivation

This project is intended to demonstrate practical experience integrating perception, localization, mapping, and autonomous navigation into a complete robotics software system while following engineering practices such as documentation, version control, and iterative development.

---

## Status

Current milestone: **Autonomous navigation in simulation using ROS2, SLAM Toolbox, AMCL, and Nav2.**
