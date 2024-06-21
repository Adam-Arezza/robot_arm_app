import math
import numpy as np


def to_degrees(radians:list):
    result = []
    for i in radians:
        result.append(round(math.degrees(i)))
    return result

def to_radians(degrees:list):
    result = []
    for i in degrees:
        result.append(math.radians(i))
    return result

def find(arr:list, fn):
    for i in arr:
        if fn(i):
            return i
    return False


def rot_mat_to_euler(rot_mat) :
    sy = math.sqrt(rot_mat[0,0] * rot_mat[0,0] +  rot_mat[1,0] * rot_mat[1,0])
    singular = sy < 1e-6
    if  not singular :
        x = math.atan2(rot_mat[2,1] , rot_mat[2,2])
        y = math.atan2(-rot_mat[2,0], sy)
        z = math.atan2(rot_mat[1,0], rot_mat[0,0])
    else :
        x = math.atan2(-rot_mat[1,2], rot_mat[1,1])
        y = math.atan2(-rot_mat[2,0], sy)
        z = 0
    return np.array([x, y, z])



