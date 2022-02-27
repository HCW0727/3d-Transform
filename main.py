import numpy as np
import math
import cv2
from preprocessing import bgremoval
########## 사용자 설정 입력 ##########

scales = [0.003 , 0.005 , 0.010, 0.002 , 0.009 , 0.003]
img_route = 'img.jpg'
img2_route = 'img1.jpg' #자동으로 만들어지는 이미지 (임의로 설정)
obj_route = 'img.obj'
out_route = 'result.obj'
out2_route = 'result2.obj'

#####################################

pose_border =  [0.1555, 0.2127, 0.4254, 0.4963, 0.607, 0.8259]


########### mtl 파일 작성 ###############
f3 = open('img.mtl','w')

img_route = "img.jpg"
f3.writelines('newmtl Texture\n')
f3.writelines('Ka 0.500 0.500 0.500\n')
f3.writelines('Kd 0.500 0.500 0.500\n')
f3.writelines('Ks 0.500 0.500 0.500\n')
f3.writelines('Tr 1.000000\n')
f3.writelines('illum 1\n')
f3.writelines('Ns 0.000000\n')
f3.writelines('map_Kd ' + img2_route + '\n')

f3.close()
########################################

f = open(obj_route,"r")

######### obj 노멀화 + uv 매핑 ###########
img = cv2.imread(img_route)
height,width,_ = img.shape
contours = []

_,_,nobg_img = bgremoval(img_route)
_,mask_img = cv2.threshold(nobg_img,250,255,cv2.THRESH_BINARY_INV)
gray = cv2.cvtColor(mask_img,cv2.COLOR_BGR2GRAY)
temp = cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_TC89_KCOS)

for x in range(len(temp)):
    for y in range(len(temp[x])):
        for z in range(len(temp[x][y])):   
            contours.append(temp[x][y][z][0])
contours = contours[:len(contours)-4]

img_minx = width
img_maxx = 0

img_miny = height
img_maxy = 0

for x in contours:
    img_minx = min(img_minx,x[0])
    img_maxx = max(img_maxx,x[0])
    
    img_miny = min(img_miny,x[1])
    img_maxy = max(img_maxy,x[1])
    
img = img[img_miny:img_maxy,img_minx:img_maxx]

cv2.imwrite(img2_route,img)

height,width,_ = img.shape

f2 = open(out_route,"w")
lines = f.readlines()
length = len(lines)
idx = len(lines)

minx = 1.0e+6
maxx = -1.0e+6

miny = 1.0e+6
maxy = -1.0e+6

minz = 1.0e+6
maxz = -1.0e+6

for l in range(len(lines)):
    line = lines[l].split()
    if line[0] == 'v':
        minx = min(float(line[1]),minx)
        maxx = max(float(line[1]),maxx)
        
        miny = min(float(line[2]),miny)
        maxy = max(float(line[2]),maxy)
        
        minz = min(float(line[3]),minz)
        maxz = max(float(line[3]),maxz)

    elif line[0] == 'f':
        idx = min(idx,l)
        
lengthy = maxy - miny
lengthx = maxx - minx

tminy = 10
tmaxy = -10
sep = " "

f2.writelines('mtllib img.mtl\n\n')
vts = []
for x in range(idx):
    line = lines[x].split()
    if line[0] == 'v':
        newx = (float(line[1])-minx)/lengthy 
        newx1 = (float(line[1])-minx)/lengthx
        newy = (float(line[2])-miny)/lengthy 
        newz = (float(line[3])-minz) /lengthy 
        tminy = min(tminy,newy)
        tmaxy = max(tmaxy,newy)
        
        f2.writelines('v' + sep)
        f2.writelines(str(round(newx,8)) + sep)
        f2.writelines(str(round(newy,8)) + sep)
        f2.writelines(str(round(newz,8)) + '\n')
        
        vts.append(str(round(newx1,8)) + sep + str(round(newy,8)) + sep)
        
        
f2.writelines('\n')
for x in vts:
    f2.writelines('vt ')
    f2.writelines(x)
    f2.writelines('\n')
    
f2.writelines('\n')
f2.writelines('usemtl Texture\n')
        
for x in range(idx,length):
    line = lines[x].split()
    f2.writelines('f ')
    f2.writelines(line[1] + '/' + line[1]  + sep)
    f2.writelines(line[2] + '/' + line[2]+ sep)
    f2.writelines(line[3] + '/' + line[3] )
    f2.writelines('\n') 
    
f2.close()
f.close()
        
#########################################

lines = []

f4 = open(out_route,'r')
lines = f4.readlines()
f4.close()
length = len(lines)

idx = length

vertex = []

Normals = [[]for _ in range(length)]
vNormals = []

def AddVertex(arr):
    temp2 = [float(arr[1]),float(arr[2]),float(arr[3])]
    vertex.append(temp2)
    
def GetNormals(arr):
    v1 = vertex[int(arr[1].split('/')[0])-1]
    v2 = vertex[int(arr[2].split('/')[0])-1]
    v3 = vertex[int(arr[3].split('/')[0])-1]
        
    va = np.array([v2[0]-v1[0],v2[1]-v1[1],v2[2]-v1[2]])
    vc = np.array([v3[0]-v1[0],v3[1]-v1[1],v3[2]-v1[2]])
        
    res = np.cross(va,vc)
    l = math.sqrt(res[0]*res[0] + res[1]*res[1] + res[2]*res[2])
    
    
    if l < 1.0e-300:
        res[0] = res[0] * 1.0e+300
        res[1] = res[1] * 1.0e+300
        res[2] = res[2] * 1.0e+300
    else:
        res[0] = res[0]/l
        res[1] = res[1]/l
        res[2] = res[2]/l
        
    return res

def AddNormals(arr,res):
    
    Normals[int(arr[1].split('/')[0])-1].append(res)
    Normals[int(arr[2].split('/')[0])-1].append(res)
    Normals[int(arr[3].split('/')[0])-1].append(res)
    

def GetvNormals():
    for b in range(len(Normals)):
        xsum = 0
        ysum = 0
        zsum = 0
        for a in Normals[b]:
            # print(a)
            c = len(Normals[b])
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
    elif line[0] == 'vt':
        idx = min(idx,x)
    elif line[0] == 'f':
        AddNormals(line,GetNormals(line))
GetvNormals()      


miny = -1.0e+6
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

# print(border)
f5 = open(out2_route,"w")

sep = " "

f5.writelines('mtllib img.mtl\n\n')
for x in range(1,idx):
    line = lines[x].split()
    if len(line) == 0:
        continue
    f5.writelines('v ')
    yval = float(line[2])
    # print(yval)
    
    scale = 0
    for y in range(5):
        l = border[y]-border[y+1] 
        if border[y+1] <= yval < border[y]:
            scale = (yval-border[y+1])/l*scales[y] + (border[y]-yval)/l*scales[y+1]
    
    # print(scale)
    f5.writelines(str(round(float(line[1]) + vNormals[x][0]*scale,8)) + sep)
    f5.writelines(str(round(float(line[2]) + vNormals[x][1]*scale,8)) + sep)
    f5.writelines(str(round(float(line[3]) + vNormals[x][2]*scale,8)) + sep)
    f5.writelines('\n')
    
    # print(vNormals[x][0])
        

for x in range(idx,length):
    
    f5.writelines(lines[x])

f5.close()


print("Transformed!")