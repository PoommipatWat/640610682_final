from setuptools import setup
import os
from glob import glob

package_name = 'robot_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
         glob(os.path.join('launch', '*launch.[pxy][yma]*')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Poommipat Wattanaprasit',
    maintainer_email='poommipat_wat@cmu.ac.th',
    description='Turtlebot3 control using RPLidar',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'lidar_data_converter = robot_control.lidar_data_converter:main',
            'motion_controller = robot_control.motion_controller:main',
            'obstacle_detector = robot_control.obstacle_detector:main',
        ],
    },
)