import math

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

def find(arr, fn):
    for i in arr:
        if fn(i):
            return i
    return False

