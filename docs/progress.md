# Project Progress

This document tracks demonstrated functionality separately from planned work. The project is under active development and is not yet a complete autonomous delivery system.

## Completed milestones

| Milestone | Evidence in this repository | Status |
| --- | --- | --- |
| ROS 2 simulation baseline | ROS 2 Humble Dockerfile and TurtleBot3/Gazebo workflow | Complete |
| 2D LiDAR mapping | Saved `my_map.pgm` and `my_map.yaml` produced with SLAM Toolbox | Complete |
| Localization | AMCL workflow against the saved occupancy map | Complete |
| Point-to-point navigation | Nav2 workflow for RViz2 goals | Complete |
| Custom test environment | `office_fasttrack.world` with a central lobby and multiple rooms | Complete |
| Responsive teleoperation | Custom `/cmd_vel` WASD node with release timeout and immediate stop | Complete |

## Current engineering focus

The next high-value milestone is a custom multi-waypoint mission node, preferably implemented as a ROS 2 C++ package using the Nav2 action interface. The node should:

1. Load an ordered list of named office destinations.
2. Dispatch navigation goals sequentially.
3. Record goal state, elapsed time, and failure reason.
4. Stop safely or invoke a bounded retry when a goal fails.
5. Produce repeatable trial data for later evaluation.

## Planned evaluation

The project will evaluate navigation across repeated trials using:

- Goal success rate
- Mission completion time
- Path length
- Recovery count
- Final position and heading error, when measurable

No quantitative results are claimed until the trial procedure and measurements are implemented.

## Known limitations

- Simulation only; no physical robot deployment has been completed.
- Gazebo, robot spawning, SLAM, and Nav2 currently require multiple terminal commands.
- Multi-waypoint mission execution is not yet implemented.
- Dynamic-obstacle response and failure recovery have not been systematically tested.
- The repository does not yet include automated ROS integration tests.
- A recorded Gazebo/RViz2 demonstration is still needed.

## Presentation milestones

- [x] Public repository with saved map, custom world, Dockerfile, and teleoperation node
- [x] Reproducible written setup workflow
- [ ] End-to-end mapping and navigation video
- [ ] Multi-waypoint mission demonstration
- [ ] Repeated-trial results table and plots
- [ ] Resume update with the final repository link and measured outcomes
