#!/usr/bin/env python

import sys
import copy
import rospy
import time
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from sawyer_move.srv import grippercmd, grippercmdRequest, grippercmdResponse
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list


class moveRobot:
    def __init__(self):
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('move_group_python_interface')
        self.robot = moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface()
        self.group = moveit_commander.MoveGroupCommander("right_arm")
        rospy.wait_for_service("/gripper_control")
        self.gripper_service_control = rospy.ServiceProxy("/gripper_control", grippercmd)
        rospy.loginfo("we are good to go")

    def getInfo(self):
        rospy.loginfo("planning frame :" +
                      str(self.group.get_planning_frame()))
        rospy.loginfo("eff link :" + str(self.group.get_end_effector_link()))
        rospy.loginfo("robot planning groups" +
                      str(self.robot.get_group_names()))
        rospy.loginfo(self.robot.get_current_state())

    def getCurrentJointAngle(self):
        rospy.loginfo(self.group.get_current_joint_values())

    def getCurrentPoseAngle(self):
        rospy.loginfo(self.group.get_current_pose())

    def getJointNames(self):
        rospy.loginfo(self.group.get_joints())

    def sendJointGoal(self, data):
        self.group.go(data, wait=True)
        self.group.stop()
        rospy.loginfo("joint motion completed")

    def sendPoseGoal(self, data):
        pose_goal = geometry_msgs.msg.Pose()
        pose_goal.orientation.w = 1.0
        pose_goal.position.x = 0.4
        pose_goal.position.y = 0.1
        pose_goal.position.z = 0.4
        self.group.set_pose_target(pose_goal)
        plan = self.group.go(wait=True)
        self.group.stop()
        rospy.loginfo("pose motion completed")
    
    def gripperControl(self, data):
        grippersrv = grippercmdRequest()
        grippersrv.grip.data = data
        if (self.gripper_service_control.call(grippersrv)):
            rospy.loginfo("service call succeeded!")
        else:
            rospy.loginfo("service call failed")



if __name__ == "__main__":
    mr = moveRobot()
    pose_0 = [0.114, -0.69, -0.075, 2.06, 0.0131, 0.310, 0.0896]
    pose_1 = [0.658,-0.736,1.814,-2.243,-2.326,0.98,2.067]
    mr.getCurrentJointAngle()
    # mr.gripperControl(True)
    # time.sleep(1)
    # mr.gripperControl(False)
    # mr.sendJointGoal(pose_0)
    # mr.sendPoseGoal("a")








# 'right_j0'
# 'right_j1'
# 'right_j2'
# 'right_j3'
# 'right_j4'
# 'right_j5'
# 'right_j6'

