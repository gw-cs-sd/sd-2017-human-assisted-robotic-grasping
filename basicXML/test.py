"""Loads up an environment, attaches a viewer, loads a scene, and requests information about the robot.
"""
from openravepy import *
import time
env = Environment() # create openrave environment
env.SetViewer('qtcoin') # attach viewer (optional)
env.Load('./testEnv.xml') # load a simple scene
time.sleep(10)
robot = env.GetRobots()[0] # get the first robot
#manipulator = robot.GetManipulators()[0]

#robot.SetActiveManipulator(manipulator)
target = env.GetKinBody("block")
gmodel = databases.grasping.GraspingModel(robot,target)
gmodel.autogenerate()

validgrasps, validindicees = gmodel.computeValidGrasps(startindex=0, checkcollision=True, checkik=True, checkgrasper=True, backupdist=0.0, returnnum=1)

print(validgrasps)

target = env.GetKinBody("cylinder")
gmodel = databases.grasping.GraspingModel(robot,target)
gmodel.autogenerate()
validgrasps, validindicees = gmodel.computeValidGrasps(startindex=0, checkcollision=True, checkik=True, backupdist=0.0, returnnum=1)

print(validgrasps)


target = env.GetKinBody("teapot")
gmodel = databases.grasping.GraspingModel(robot,target)
gmodel.autogenerate()
validgrasps, validindicees = gmodel.computeValidGrasps(startindex=0, checkcollision=True, checkik=True, backupdist=0.0, returnnum=1)

print(validgrasps)


target = env.GetKinBody("mug")
gmodel = databases.grasping.GraspingModel(robot,target)
gmodel.autogenerate()
validgrasps, validindicees = gmodel.computeValidGrasps(startindex=0, checkcollision=True, checkik=True, backupdist=0.0, returnnum=1)

print(validgrasps)


robot.Grab(target)
gmodel.showgrasp(validgrasps[0])
gmodel.moveToPreshape(validgrasps[0])
Tgoal = gmodel.getGlobalGraspTransform(validgrasps[0],collisionfree=True)
basemanip = interfaces.BaseManipulation(robot)
basemanip.MoveToHandPosition(matrices=[Tgoal])
robot.WaitForController(0)
taskmanip = interfaces.TaskManipulation(robot)
taskmanip.CloseFingers()
robot.WaitForController(0)

#with env: # lock the environment since robot will be used
#	raveLogInfo("Robot "+robot.GetName()+" has "+repr(robot.GetDOF())+" joints with values:\n"+repr(robot.GetDOFValues()))
#	robot.SetDOFValues([0.5],[0]) # set joint 0 to value 0.5
#	T = robot.GetLinks()[1].GetTransform() # get the transform of link 1
#	raveLogInfo("The transformation of link 1 is:\n"+repr(T))
