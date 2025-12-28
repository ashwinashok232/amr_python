from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory
import os
from launch.actions import TimerAction

def generate_launch_description():
    description_pkg = get_package_share_directory('amr_description')
    control_pkg = get_package_share_directory('amr_control')

    xacro_path = os.path.join(description_pkg, 'urdf', 'amr.urdf.xacro')
    controller_config = os.path.join(control_pkg, 'config', 'diff_drive_controller.yaml')

    robot_description = ParameterValue(
        Command(['xacro ', xacro_path]),
        value_type=str
    )

    # 1) Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            )
        )
    )

    # 2) Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': True,
            'robot_description': robot_description
        }]
    )

    # 3) Spawn robot into Gazebo
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        output='screen',
        arguments=['-topic', 'robot_description', 
                   '-entity', 'amr'],
    )

    # 4) Spawn controllers AGAINST /gazebo_ros2_control
    spawn_joint_state_broadcaster = TimerAction(
        period=6.0,
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=[
                    'joint_state_broadcaster',
                    '--controller-manager', '/controller_manager'
                ],
                output='screen'
            )
        ]
    )

    spawn_diff_drive_controller = TimerAction(
        period=8.0,
        actions=[
            Node(
                package='controller_manager',
                executable='spawner',
                arguments=[
                    'diff_drive_controller',
                    '--controller-manager', '/controller_manager'
                ],
                output='screen'
            )
        ]
    )

    # 5) Return EVERYTHING here
    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_robot,
        spawn_joint_state_broadcaster,
        spawn_diff_drive_controller,
    ])
