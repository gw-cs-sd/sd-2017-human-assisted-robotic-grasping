import numpy as np
import xml.etree.ElementTree as ET
import re
import transforms3d
from shutil import copyfile

#filename
fileName = './worlds/TESTDISCRETE/josh-test-book'
#rotate 90 degrees about the z axis and shift 2 meters on the y axis
finalPosition = [0,2000,0]
finalRotationAxis = [0,0,1]
finalRotationAngle = np.pi/2
steps = 10

#Copy the file the number of times we need for the specific steps
for i in range(1,steps+1):
    copyfile(fileName+'.xml',fileName+'_'+str(i)+'.xml')

tree = ET.parse(fileName+'.xml')
root = tree.getroot()
#print(root)
#Find all full transforms. First is object, second is arm
transforms = []
for transform in root.findall('*.transform'):
    #print(transform)
    transforms.append(transform.find('fullTransform').text)

transformDict = {}
i=0
for transform in transforms:
    #Parse into quaternion and translation
    print(transform)
    words = re.findall("-?\d+\.?\d*",transform)
    #for word in words:
        #print(word)
    quaternion = [float(words[0]),float(words[1]),float(words[2]),float(words[3])]
    translation = np.array([float(words[4]),float(words[5]),float(words[6])]).reshape((3,1))
    transformDict[i] = {}
    transformDict[i]['quaternion'] = quaternion
    transformDict[i]['translation'] = translation
    transformDict[i]['rotMat'] = transforms3d.quaternions.quat2mat(quaternion)
    transformDict[i]['transformToWorld'] = np.concatenate((transformDict[i]['rotMat'],translation),axis=1)
    #print(transformDict[i]['transformToWorld'])
    transformDict[i]['transformToWorld'] = np.concatenate((transformDict[i]['transformToWorld'],[[0,0,0,1]]),axis=0)
    print(transformDict[i]['transformToWorld'])
    i += 1


#now transformDict[0] is object, [1] is arm.
#Start generating new files
for i in range(1,steps+1):
    position = np.array([finalPosition[0]*i/steps,finalPosition[1]*i/steps,finalPosition[2]*i/steps])
    position = position.reshape(3,1)
    rotation = finalRotationAngle*i/steps
    rotMat = transforms3d.axangles.axangle2mat(finalRotationAxis,rotation)
    rotMat = np.concatenate((rotMat,position),axis=1)
    rotMat = np.concatenate((rotMat,[[0,0,0,1]]),axis=0)
    print(rotMat)

    #multiply rotMat by original matrices to get complete transform matrix
    objectTransform = np.matmul(rotMat,transformDict[0]['transformToWorld'])
    armTransform = np.matmul(rotMat,transformDict[1]['transformToWorld'])
    print(armTransform)

    quaternionObject = transforms3d.quaternions.mat2quat(objectTransform[0:3,0:3])
    quaternionArm = transforms3d.quaternions.mat2quat(armTransform[0:3,0:3])

    tree = ET.parse(fileName+'_'+str(i)+'.xml')
    root = tree.getroot()

    transforms = []
    for transform in root.findall('*.transform'):
        #print(transform)
        transforms.append(transform.find('fullTransform'))

    transforms[0].text = '(' + str(quaternionObject[0]) + ' ' + str(quaternionObject[1]) + ' ' + str(quaternionObject[2]) + ' ' + str(quaternionObject[3]) + ')[' + str(objectTransform[0,3]) + ' ' + str(objectTransform[1,3]) + ' ' + str(objectTransform[2,3]) + ']'

    transforms[1].text = '(' + str(quaternionArm[0]) + ' ' + str(quaternionArm[1]) + ' ' + str(quaternionArm[2]) + ' ' + str(quaternionArm[3]) + ')[' + str(armTransform[0,3]) + ' ' + str(armTransform[1,3]) + ' ' + str(armTransform[2,3]) + ']'

    tree.write(fileName+'_'+str(i)+'.xml')
