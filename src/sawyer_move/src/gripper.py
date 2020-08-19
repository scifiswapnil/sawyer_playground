#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from sawyer_move.srv import grippercmd, grippercmdResponse


class RosNode:
    def __init__(self):
        rospy.init_node("sawyer_gripper_control")
        rospy.loginfo("Starting sawyer_gripper_control.")
        self.left_finger_pub = rospy.Publisher(
            "/robot/electric_gripper_controller/joints/right_gripper_r_finger_controller/command", Float64, queue_size=1)
        self.right_finger_pub = rospy.Publisher(
            "/robot/electric_gripper_controller/joints/right_gripper_l_finger_controller/command", Float64, queue_size=1)
        self.srv_server_handler = rospy.Service(
            "gripper_control", grippercmd, self.gripperCB)

    def gripperCB(self, data):
        left_finger_data = Float64()
        right_finger_data = Float64()
        
        if (data.grip.data):    
            left_finger_data.data, right_finger_data.data = -0.1, 0.1
        else:
            left_finger_data.data, right_finger_data.data = 0.0, 0.0
        self.left_finger_pub.publish(left_finger_data)
        self.right_finger_pub.publish(right_finger_data)
        results = grippercmdResponse()
        results.result.data = True
        return results


if __name__ == "__main__":
    ros_node = RosNode()
    rospy.spin()
