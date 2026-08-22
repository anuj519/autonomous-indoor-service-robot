#!/usr/bin/env python3

import curses
import threading
import time

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


LINEAR_SPEED = 0.18
ANGULAR_SPEED = 0.75

# If no repeated key event arrives within this time,
# assume the key was released and stop the robot.
KEY_RELEASE_TIMEOUT = 0.14

PUBLISH_RATE = 20.0


class WASDTeleop(Node):
    def __init__(self):
        super().__init__("wasd_teleop")

        self.publisher = self.create_publisher(Twist, "/cmd_vel", 10)

        self.linear = 0.0
        self.angular = 0.0

        self.last_key_time = 0.0
        self.running = True

        self.lock = threading.Lock()

        self.timer = self.create_timer(
            1.0 / PUBLISH_RATE,
            self.publish_velocity
        )

    def set_command(self, linear, angular):
        with self.lock:
            self.linear = linear
            self.angular = angular
            self.last_key_time = time.monotonic()

    def stop(self):
        with self.lock:
            self.linear = 0.0
            self.angular = 0.0
            self.last_key_time = time.monotonic()

        self.publisher.publish(Twist())

    def publish_velocity(self):
        with self.lock:
            linear = self.linear
            angular = self.angular
            elapsed = time.monotonic() - self.last_key_time

            # Simulated key-up behavior
            if elapsed > KEY_RELEASE_TIMEOUT:
                linear = 0.0
                angular = 0.0
                self.linear = 0.0
                self.angular = 0.0

        msg = Twist()
        msg.linear.x = linear
        msg.angular.z = angular

        self.publisher.publish(msg)


def keyboard_loop(stdscr, node):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(20)

    stdscr.addstr(
        0, 0,
        "ROS2 WASD Teleop\n\n"
        "Hold controls:\n"
        "  W = Forward\n"
        "  S = Backward\n"
        "  A = Turn left\n"
        "  D = Turn right\n"
        "  Q = Forward + left\n"
        "  E = Forward + right\n"
        "\n"
        "SPACE = Emergency stop\n"
        "X     = Exit\n\n"
        f"Linear speed:  {LINEAR_SPEED:.2f} m/s\n"
        f"Angular speed: {ANGULAR_SPEED:.2f} rad/s\n"
    )

    while rclpy.ok() and node.running:
        key = stdscr.getch()

        if key == -1:
            continue

        try:
            char = chr(key).lower()
        except ValueError:
            continue

        if char == "w":
            node.set_command(LINEAR_SPEED, 0.0)

        elif char == "s":
            node.set_command(-LINEAR_SPEED, 0.0)

        elif char == "a":
            node.set_command(0.0, ANGULAR_SPEED)

        elif char == "d":
            node.set_command(0.0, -ANGULAR_SPEED)

        elif char == "q":
            node.set_command(LINEAR_SPEED, ANGULAR_SPEED)

        elif char == "e":
            node.set_command(LINEAR_SPEED, -ANGULAR_SPEED)

        elif key == ord(" "):
            node.stop()

        elif char == "x":
            node.stop()
            node.running = False
            break


def main():
    rclpy.init()

    node = WASDTeleop()

    ros_thread = threading.Thread(
        target=rclpy.spin,
        args=(node,),
        daemon=True
    )
    ros_thread.start()

    try:
        curses.wrapper(keyboard_loop, node)

    except KeyboardInterrupt:
        pass

    finally:
        node.stop()
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
