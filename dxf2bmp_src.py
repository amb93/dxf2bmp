import ezdxf
import numpy as np
import cv2
import math
from PIL import Image

dpi = 1000
dpiout = 847
dpm = dpi/25.4
margin = 0
i=0
k=0
Ys=[]
Xs=[]
dxf = ezdxf.readfile('40x100.dxf')
space = dxf.modelspace()


def getPos(event,x,y,flags,param):

    if event == cv2.EVENT_LBUTTONDOWN:
        
        Fill(Blank,0,y,x)
        
    
def Fill(image,newValue,mouseY,mouseX):
    shape = np.shape(image)
    
    mouseY = shape[0] - mouseY

    print('x = %d, y = %d'%(mouseX, mouseY),np.shape(image))
    
    cv2.floodFill(image,mask = mask,seedPoint = (mouseX,mouseY),newVal=0 )
    image = np.flipud(image)
    cv2.imshow('as',image) 
    cv2.resizeWindow('as',600,600)
    
    BMPout = Image.fromarray(image)
    Factor = dpi/dpiout
    size = np.round(np.divide(np.shape(image),Factor))
    size = size.astype(int)
    BMPout = BMPout.resize((size[1],size[0]))
    BMPout = BMPout.convert('1')
    BMPout.save('ktest1.bmp',dpi = (dpiout,dpiout))

def DrawArc(image, center, radius, startAng, endAng, color,resolution):
    '''Draws an arc with specific reslution and color on an input image
    Args:
    image      - The input image to draw the arc on
    center     - Arc's center
    radius     - Arc's radius
    startAng   - the starting angle of the arc
    engAng     - the ending angle of the arc
    color      - Arc's color on the input image
    resolution - Number of points for calculation

    output:
    image      - updated image with plotted arc'''
    #print(center,radius,startAng,endAng)
    #startAng = 90 - startAng
    #endAng = 90 - endAng 
    
    if(startAng > endAng):
        fillAng = 360 - (startAng - endAng)
    else:
        fillAng = endAng - startAng

    #print(startAng,endAng,fillAng)
    endAng = startAng + fillAng
    startAng = 90 - startAng
    endAng = 90 - endAng 
    theta = np.linspace(startAng,endAng,resolution)
    #print(theta)
    x = np.ceil(radius*np.cos(np.deg2rad(theta)) + center[0])
    y = np.ceil(radius*np.sin(np.deg2rad(theta)) + center[1])
    x=x.astype(int)
    y=y.astype(int)

    #print(x)
    #print(np.shape(image))
    for k in range(np.size(theta)-1):
        #image[x[k]][y[k]] = color
        try:
            cv2.line(image,(y[k],x[k]),(y[k+1],x[k+1]),color,thickness=2)
        except:
            pass

    x = np.round(radius*np.cos(np.deg2rad(theta)) + center[0])
    y = np.round(radius*np.sin(np.deg2rad(theta)) + center[1])
    x=x.astype(int)
    y=y.astype(int)

    #image[x[np.size(theta)-1]][y[np.size(theta)-1]] = color
    #image[x[0]][y[0]] = color
    #cv2.line(image,(y[np.size(theta)-2],x[np.size(theta)-2]),(y[np.size(theta)-1],x[np.size(theta)-1]),color,thickness=1)
    #cv2.line(image,(y[0],x[0]),(y[1],x[1]),color,thickness=1)

    
    return image


for e in space:
    if e.dxftype()=="LINE":
        if i==0:
            Line = np.array([[e.get_dxf_attrib('start'),e.get_dxf_attrib('end')]])
            Lines = Line

        else:    
            Line = np.array([[e.get_dxf_attrib('start'),e.get_dxf_attrib('end')]])
            Lines = np.concatenate((Lines,Line),axis=0)
        
        i+=1
    
    if e.dxftype()=="ARC":
        if k==0:
            Arc = np.array([[e.get_dxf_attrib('center'),e.get_dxf_attrib('radius'),e.get_dxf_attrib('start_angle'),e.get_dxf_attrib('end_angle')]])
            #Check indexing for Arc ------------------------------------------------**************************************************---------------------------------------
            Arc = np.array([[Arc[0][0][0],Arc[0][0][1],Arc[0][1],Arc[0][2],Arc[0][3]]])
            Arcs = Arc

        else:    
            Arc = np.array([[e.get_dxf_attrib('center'),e.get_dxf_attrib('radius'),e.get_dxf_attrib('start_angle'),e.get_dxf_attrib('end_angle')]])
            Arc = np.array([[Arc[0][0][0],Arc[0][0][1],Arc[0][1],Arc[0][2],Arc[0][3]]])

            Arcs = np.concatenate((Arcs,Arc),axis=0)


        k+=1  

for L in Lines:
    Ys.append(L[0][1])
    Xs.append(L[0][0])

Xmax = math.ceil(np.amax(Xs)*dpm)
Xmin = math.floor(np.amin(Xs)*dpm)  
Ymax = math.ceil(np.amax(Ys)*dpm)
Ymin = math.floor(np.amin(Ys)*dpm)  



Blank = np.ones(((Ymax-Ymin)+(2*margin),(Xmax-Xmin)+(2*margin)),np.uint8)*255
#Blank = np.ones((1000,1000))
#print(np.shape(Blank))

mask = np.zeros(((Ymax-Ymin)+(2*margin)+2,(Xmax-Xmin)+(2*margin)+2),np.uint8)

for L in Lines:
    L[0][1] = round(L[0][1]*dpm - Ymin + margin)
    L[0][0] = round(L[0][0]*dpm - Xmin + margin)
    L[1][1] = round(L[1][1]*dpm - Ymin + margin)
    L[1][0] = round(L[1][0]*dpm - Xmin + margin)

    cv2.line(Blank,(int(L[0][0]),int(L[0][1])),(int(L[1][0]),int(L[1][1])),0,thickness=2)


for A in Arcs:
    A[0] = A[0]*dpm - Xmin + margin         #Normalize CenterX
    A[1] = A[1]*dpm - Ymin + margin         #Normalize CenterY
    A[2] = A[2]*dpm                         #Normalize Radius
    startAng = A[3] 
    endAng = A[4]
    #print(A[3],A[4])
    A=A.astype(int)
    Blank = DrawArc(Blank,(A[1],A[0]),A[2],startAng,endAng,0,100)
    #print(startAng,endAng)
    #cv2.ellipse(Blank,(A[0],A[1]),(A[2],A[2]), 0, endAng, start, 0 ,1)


BMP = Blank
BMP = np.flipud(Blank)

#BMP = BMP.astype(np.uint)
cv2.imshow('BMP',BMP) 
cv2.resizeWindow('BMP',600,600)

cv2.setMouseCallback('BMP',getPos)
cv2.waitKey(0) 


    