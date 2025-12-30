# Autonomous Mobile Robot (ROS2)

Basic AMR that will use LiDAR and a camera for autonomous navigation.

### Launch
**Gazebo**: $ ros2 launch amr_bringup sim.launch.py
**Teleop**: $ ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_drive_controller/cmd_vel_unstamped
