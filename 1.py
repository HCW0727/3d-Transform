import numpy as np
import math
#####################################

scales = [0.05 , 0.1 , 0.3, 0.2 , 0.1 , 0.05]

#####################################

pose_border =  [0.1555, 0.2127, 0.4254, 0.4963, 0.607, 0.8259]

f = open("result_test_256.obj","r")
lines = f.readlines()
length = len(lines)

idx = length

vertex = []

Normals = [[]for _ in range(length)]
vNormals = []

def AddVertex(arr):
    temp = [float(arr[1]),float(arr[2]),float(arr[3])]
    vertex.append(temp)
        
def AddPolygon(arr):
    temp = [arr[1],arr[2],arr[3]]
    
def GetNormals(arr):
    v1 = vertex[int(arr[1])-1]
    v2 = vertex[int(arr[2])-1]
    v3 = vertex[int(arr[3])-1]
    
    va = np.array([v2[0]-v1[0],v2[1]-v1[1],v2[2]-v1[2]])
    vc = np.array([v3[0]-v1[0],v3[1]-v1[1],v3[2]-v1[2]])
    
    res = np.cross(va,vc)
    l = math.sqrt(res[0]*res[0] + res[1]*res[1] + res[2]*res[2])    
    
    if l < 1.0e-30:
        res[0] = res[0] * 1.0e+30
        res[1] = res[1] * 1.0e+30
        res[2] = res[2] * 1.0e+30
    else:
        
        res[0] = res[0]/l
        res[1] = res[1]/l
        res[2] = res[2]/l
    return res

def AddNormals(arr,res):
    Normals[int(arr[1])-1].append(res)
    Normals[int(arr[2])-1].append(res)
    Normals[int(arr[3])-1].append(res)
    

def GetvNormals():
    for b in range(len(Normals)):
        xsum = 0
        ysum = 0
        zsum = 0
        for a in Normals[b]:
            c = len(Normals[b])
            # print(a)
            xsum += a[0]
            ysum += a[1]
            zsum += a[2]
            
        rx = xsum / c
        ry = ysum / c
        rz = zsum / c
        
        vNormals.append([rx,ry,rz])
        
            


for x in range(len(lines)):
    line = lines[x] 
    line = line.split()
    if len(line) == 0:
        continue
    elif line[0] == 'v':
        AddVertex(line)
    elif line[0] == 'f':
        idx = min(idx,x)
        AddNormals(line,GetNormals(line))
        
GetvNormals()        
f.close()

miny = 1.0e-6
maxy = 1.0e+6

for v in vertex:
    miny = max(v[1],miny)
    maxy = min(v[1],maxy)
    
img_length = miny-maxy
border = []
b_l = [0] * 6
b_h = [0] * 6

for b in range(6):
    border.append(round(miny - pose_border[b] * img_length,4))

print(border)
f2 = open("changed.obj","w")

sep = " "
for x in range(idx):
    f2.writelines('v ')
    line = lines[x].split()
    
    yval = float(line[2])
    # print(yval)
    
    scale = 0
    for x in range(5):
        l = border[x]-border[x+1] 
        if border[x+1] <= yval < border[x]:
            scale = (yval-border[x])/l*scales[x+1] + (border[x+1]-yval)/l*scales[x]
    
    # print(scale)
    f2.writelines(str(round(float(line[1]) + vNormals[x][0]*scale,8)) + sep)
    f2.writelines(str(round(float(line[2]) + vNormals[x][1]*scale,8)) + sep)
    f2.writelines(str(round(float(line[3]) + vNormals[x][2]*scale,8)) + sep)
    f2.writelines(str(float(line[4])) + sep)
    f2.writelines(str(float(line[5]))+ sep)
    f2.writelines(str(float(line[6])) + sep)
    f2.writelines('\n')
    
    print(vNormals[x][0]*scale)
    

for x in range(idx,length):
    
    f2.writelines(lines[x])

f2.close()


print("Transformed!")