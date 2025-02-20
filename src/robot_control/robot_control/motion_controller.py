#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

from lidar_msg.msg import LidarData, LidarPoint
from lidar_msg.srv import StopRobot

import numpy as np

class MotionControl(Node):
    def __init__(self):
        super().__init__('motion_controller')

        self.MAX_LINEAR_SPEED = 0.2     # max linear speed of turtlebot3 burger
        self.MAX_ANGULAR_SPEED = 2.8    # max angular speed of turtlebot3 burger

        self.MIN_LIDAR_DISTANCE = 0.20
        self.MAX_LIDAR_DISTANCE = 0.40

        self.obstable_detected = False

        self.zone_access = np.ones(8, dtype=bool)

        self.lidar_subscription = self.create_subscription(
            LidarData,
            'lidar_data/a3',
            self.lidar_data_callback,
            10
        )
        self.lidar_subscription

        self.cmd_vel_publisher = self.create_publisher(
            Twist,
            'cmd_vel',
            10
        )

        self.stop_robot_server = self.create_service(
            StopRobot, 
            'stop_robot', 
            self.stop_robot_callback
        )
        
        self.get_logger().info('Motion controller node has been started')

    def stop_robot_callback(self, request, response):
        self.obstable_detected = request.stop
        self.zone_access = np.array(request.zone_access)
        response.success = True
        return response
    
    def get_zones(self, angles):
        angles = np.mod(angles, 360)
        return (angles // 45).astype(int)

    def check_angle_access(self, angles):
        zone = self.get_zones(angles)
        if self.zone_access[zone]:
            return True
        return False
    
    def lidar_data_callback(self, msg):
        cmd_vel = Twist()

        distances = np.array([point.distance for point in msg.scan_points])
        angles = np.array([point.angle for point in msg.scan_points])
        min_distance = np.min(distances) if len(distances) > 0 else float('inf')
        min_angle = angles[np.argmin(distances)] if len(distances) > 0 else 0

        if self.check_angle_access(min_angle):

            if self.MIN_LIDAR_DISTANCE <= min_distance <= self.MAX_LIDAR_DISTANCE:
                speed_factor = (self.MAX_LIDAR_DISTANCE - min_distance) / (self.MAX_LIDAR_DISTANCE - self.MIN_LIDAR_DISTANCE)

                cmd_vel.linear.x = speed_factor * np.cos(min_angle) * self.MAX_LINEAR_SPEED
                cmd_vel.angular.z = -1 * speed_factor * np.sin(min_angle) * self.MAX_ANGULAR_SPEED

        self.cmd_vel_publisher.publish(cmd_vel)

def main(args=None):
    rclpy.init(args=args)
    controller = MotionControl()
    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()