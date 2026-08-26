# Setup and Operating Guide

This guide reproduces the current ROS 2 Humble simulation, mapping, and point-to-point navigation workflow. Run each ROS command from a terminal that has sourced ROS 2 and set the TurtleBot3 model.

## 1. Requirements

- Ubuntu 22.04
- ROS 2 Humble Desktop
- Gazebo Classic 11
- Python 3
- A graphical desktop capable of running Gazebo and RViz2

Install the project dependencies:

```bash
sudo apt update
sudo apt install \
  gazebo \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-gazebo-ros2-control \
  ros-humble-turtlebot3 \
  ros-humble-turtlebot3-msgs \
  ros-humble-turtlebot3-simulations \
  ros-humble-turtlebot3-navigation2 \
  ros-humble-slam-toolbox \
  ros-humble-navigation2 \
  ros-humble-nav2-bringup
```

Clone the repository:

```bash
git clone https://github.com/anuj519/autonomous-indoor-service-robot.git
cd autonomous-indoor-service-robot
```

## 2. Configure each terminal

Run these commands in every new terminal used for the simulation:

```bash
source /opt/ros/humble/setup.bash
export TURTLEBOT3_MODEL=burger
```

To make the model selection persistent, add the export to your shell startup file:

```bash
echo 'export TURTLEBOT3_MODEL=burger' >> ~/.bashrc
```

## 3. Launch the custom office world

From the repository root:

```bash
gazebo --verbose worlds/office_fasttrack.world \
  -s libgazebo_ros_init.so \
  -s libgazebo_ros_factory.so
```

The primary world is a 16 m by 12 m enclosed environment with a central lobby, multiple rooms, and doorway gaps for navigation testing.

## 4. Spawn TurtleBot3

In a second configured terminal:

```bash
ros2 run gazebo_ros spawn_entity.py \
  -entity burger \
  -database turtlebot3_burger \
  -x 0 -y 0 -z 0.01
```

Confirm that the main ROS interfaces are present:

```bash
ros2 topic list
```

The working simulation should include `/cmd_vel`, `/scan`, `/tf`, `/tf_static`, and `/clock`.

## 5. Drive with responsive WASD controls

In another configured terminal:

```bash
python3 scripts/wasd_teleop.py
```

The node publishes `geometry_msgs/msg/Twist` commands to `/cmd_vel` at 20 Hz. It approximates key-down/key-up control by stopping when repeated key events are no longer received.

| Key | Command |
| --- | --- |
| `W` | Forward |
| `S` | Reverse |
| `A` | Rotate left |
| `D` | Rotate right |
| `Q` | Forward-left |
| `E` | Forward-right |
| `Space` | Immediate stop |
| `X` | Stop and exit |

## 6. Build a map with SLAM Toolbox

Start asynchronous SLAM in a configured terminal:

```bash
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true
```

Start RViz2 if it is not already running:

```bash
rviz2
```

Set the RViz2 fixed frame to `map`, add the `Map` and `LaserScan` displays, then drive the robot through the reachable rooms. Loop closures and revisiting areas generally improve the occupancy map.

Save the result from the repository root:

```bash
ros2 run nav2_map_server map_saver_cli -f maps/my_map
```

This creates `maps/my_map.pgm` and `maps/my_map.yaml`.

## 7. Navigate on the saved map

Stop the SLAM process before switching to localization and navigation. With Gazebo and the robot still running, launch the TurtleBot3 Nav2 configuration:

```bash
ros2 launch turtlebot3_navigation2 navigation2.launch.py \
  use_sim_time:=True \
  map:="$(pwd)/maps/my_map.yaml"
```

In RViz2:

1. Use **2D Pose Estimate** to align the robot with its simulated starting pose.
2. Use **Navigation2 Goal** to choose a reachable destination and heading.
3. Observe the global plan, local costmap, and robot motion.

## 8. Optional Docker image

The Dockerfile installs the same ROS 2, Gazebo, TurtleBot3, SLAM Toolbox, and Nav2 dependencies:

```bash
docker build \
  -t autonomous-indoor-service-robot:humble \
  -f docker/Dockerfile .
```

Gazebo and RViz2 require graphical display forwarding. Container graphics configuration varies by Linux display server and is intentionally left host-specific; the native Ubuntu 22.04 workflow is the primary supported path.

## Troubleshooting

### TurtleBot3 model errors

Verify the environment variable in the affected terminal:

```bash
echo "$TURTLEBOT3_MODEL"
```

It should print `burger`.

### No LiDAR data

Check that `/scan` exists and is publishing:

```bash
ros2 topic hz /scan
```

If it does not exist, confirm that the robot spawned successfully and that Gazebo was started with the ROS initialization and factory plugins.

### RViz2 reports no map

- Confirm the fixed frame is `map`.
- Confirm SLAM Toolbox is running with `use_sim_time:=true`.
- Move the robot so the mapper receives changing LiDAR scans and odometry.

### Nav2 or transform warnings

- Ensure Gazebo, localization, RViz2, and Nav2 all use simulation time.
- Publish an initial pose with **2D Pose Estimate** before sending a goal.
- Confirm that `/tf`, `/tf_static`, and `/clock` are active.

## Current reproducibility boundary

The commands above document the workflow used during development, but the repository does not yet contain a unified launch package or automated integration test. Packaging and repeatable trial automation are active roadmap items.
