import cv2
from preprocessing import bgremoval

contours = []
img = cv2.imread("img.png")

height,width,_ = img.shape

_,_,nobg_img = bgremoval("img.png")
_,mask_img = cv2.threshold(nobg_img,250,255,cv2.THRESH_BINARY_INV)
gray = cv2.cvtColor(mask_img,cv2.COLOR_BGR2GRAY)
temp = cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_TC89_KCOS)

for x in range(len(temp)):
    for y in range(len(temp[x])):
        for z in range(len(temp[x][y])):   
            contours.append(temp[x][y][z][0])
contours = contours[:len(contours)-1]

img_minx = width
img_maxx = 0

img_miny = height
img_maxy = 0
for x in contours:
    print(x)
    img_minx = min(img_minx,x[0])
    img_maxx = max(img_maxx,x[0])
    
    img_miny = min(img_miny,x[1])
    img_maxy = max(img_maxy,x[1])
    
print(img_minx,img_maxx,img_miny,img_maxy)

cv2.circle(img,(img_minx,img_miny),3,(255,0,0))
cv2.circle(img,(img_maxx,img_maxy),3,(255,0,0))

print(width)
# img2 = img[]
img = img[img_miny:img_maxy,img_minx:img_maxx]

cv2.imshow("test",img)
cv2.waitKey(0)



f = open("img.obj","r")
f2 = open("changed2.obj","w")
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
        
print(idx)
        
lengthy = maxy - miny

sep = " "
for x in range(idx):
    line = lines[x].split()
    if line[0] == 'v':
        newx = (float(line[1])-minx)/lengthy 
        newy = (float(line[2])-miny)/lengthy 
        # print(int(newy*height),int(newx))
        newz = (float(line[3])-minz) /lengthy 
        
        # print(img[int(newy*height)][int(newx*height)])
        cv2.circle(img,(int(newx*height),height-int(newy*height)),1,(255,0,0))
        
        f2.writelines('v ')
        f2.writelines(str(round(newx,8)) + sep)
        f2.writelines(str(round(newy,8)) + sep)
        f2.writelines(str(round(newz,8)) + sep)
        f2.writelines('\n ')
        # print(newx,newy,newz)
        
for x in range(idx,length):
    f2.writelines(lines[x])
    
f.close()
f2.close()

cv2.imshow("test",img)  
cv2.waitKey(0)