import sys
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from cv2 import *
from os.path import isfile

from pywavefront import visualization
import pywavefront


import hemisphere
# 假設沒有該文件，則創建文件(自動生成obj file)，反之則開啟文件
if isfile('model/left_hemisphere.obj'):
    meshes_L = pywavefront.Wavefront('model/left_hemisphere.obj')
else:
    hemisphere.generate('left_hemisphere')
if isfile('model/right_hemisphere.obj'):
    meshes_R = pywavefront.Wavefront('model/right_hemisphere.obj')
else:
    hemisphere.generate('model/right_hemisphere')

mouseLeftPressed = 0
mouseRightPressed = 0
clickPt = np.array([0,0])
transfMatrix = np.eye(4,dtype=float)

lightAmbient = [ 0.4,0.4,0.4,1.0 ]
lightDiffuse = [ 0.9,0.9,0.9,1.0 ]
lightSpecular = [ 1.0,1.0,1.0, 1.0 ]
lightPosition = [ 0,0,0,0.4 ]

windowWidth = 1200
windowHeight = 600
R0 = np.array([0,0])
zoom = 1


def drawGrid():
    glLineWidth(1)
    glBegin(GL_LINES)
    for y in range(0, 20):
        glColor3f(1-y/19,0,0)
        glVertex3f(0,10*y,0)
        glVertex3f(200,10*y,0)
    glEnd()
    glBegin(GL_LINES)
    for x in range(0, 20):
        glColor3f(0,1-x/19,0)
        glVertex3f(10*x,0,0)
        glVertex3f(10*x,200,0)
    glEnd()
    
def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    global transfMatrix, zoom
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(-5, 0, int(windowWidth/2.0), windowHeight) # 除以二切成兩半
    glFrustum(-400/2000.0/zoom, 400/2000.0/zoom,- 600/2000.0/zoom, 600/2000.0/zoom, 1.0, 5000)  
    gluLookAt(0,0,100, 0,0,0, 0,1,0)
    glEnable(GL_LIGHTING)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    transfMatrixT = np.transpose(transfMatrix)
    matmatList = [transfMatrixT[i][j] for i in range(4) for j in range(4)]
    glLoadMatrixf(matmatList)
    visualization.draw(meshes_L)
    glPopMatrix()
    glDisable(GL_LIGHTING)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(int(windowWidth/2.0)+5, 0, int(windowWidth/2.0), windowHeight) # 除以二切成兩半
    glFrustum(-400/2000.0/zoom, 400/2000.0/zoom,- 600/2000.0/zoom, 600/2000.0/zoom, 1.0, 5000)  
    gluLookAt(0,0,100, 0,0,0, 0,1,0)
    glEnable(GL_LIGHTING)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()  
    transfMatrixT = np.transpose(transfMatrix)
    matmatList = [transfMatrixT[i][j] for i in range(4) for j in range(4)]
    glLoadMatrixf(matmatList)
    visualization.draw(meshes_R)
    glPopMatrix()
    glDisable(GL_LIGHTING)

    glutSwapBuffers()

def reshape(width,height):
    glViewport(0, 0, width, height)

def keyboard( key, x, y ):
    if key == b'\x1b': #ESC
        print('terminate program')
        sys.exit()

def keyboardSpecial(key,x,y):
    global xv
    global yv
    if key==100:
        print('Left')
    elif key == 102:
        print('Right')
    elif key == 101:
        print('Up')
    elif key == 103:
        print('Down')
    else:
        print('No definition')  

def reset():
    global transfMatrix, zoom, R0
    R0 = np.array([0,0])
    zoom = 1
    transfMatrix = np.eye(4,dtype=float)    
    display()

def MouseFunc(button, state, x, y):
    global mouseLeftPressed, zoom, clickPt
    if button == 0: # 左鍵拖曳旋轉
        if state == 1:
            mouseLeftPressed = 0
        else:
            mouseLeftPressed = 1
            clickPt = np.array([x,y])
    if button == 2: # 右鍵點擊回到原點(復歸)
        if state == 0:
            reset()            
    elif button == 3: #中鍵滾動縮小
        zoom = zoom/0.95
        zoom = min(zoom,8)[0][0]
        display()
    elif button == 4: #中鍵滾動放大
        zoom = zoom*0.95
        zoom = max(zoom,0.5)[0][0]
        display()
	
def MouseMotion(x, y):
    global mouseLeftPressed, clickPt, transfMatrix, R0
    if mouseLeftPressed==1:
        dR = -np.array( [ x-clickPt[0] , y-clickPt[1] ] )
        rRatio = 100.0
        Rx = np.array([ [ 1.0, 0.0, 0.0, 0.0 ],\
                        [ 0.0, cos(dR[1]/rRatio), -sin(dR[1]/rRatio), 0.0 ],\
                        [ 0.0, sin(dR[1]/rRatio), cos(dR[1]/rRatio), 0.0 ],\
                        [ 0.0, 0.0, 0.0, 1.0 ] ])
        Ry = np.array([ [ cos(dR[0]/rRatio), 0.0, sin(dR[0]/rRatio), 0.0 ],\
                        [ 0.0, 1.0, 0.0, 0.0 ],\
                        [ -sin(dR[0]/rRatio), 0.0, cos(dR[0]/rRatio), 0.0 ],\
                        [ 0.0, 0.0, 0.0, 1.0 ] ])       
        R0_tmp = R0+dR
        if np.linalg.norm(R0_tmp)<(zoom**0.2)*100 :
            transfMatrix = Rx.dot(transfMatrix)
            transfMatrix = Ry.dot(transfMatrix)
            R0 = R0_tmp    
        display()
    clickPt = np.array([x,y])


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
glutCreateWindow(b'Final Project')
glutReshapeWindow(windowWidth,windowHeight)
glutReshapeFunc(reshape)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutSpecialFunc(keyboardSpecial)
glutMouseFunc(MouseFunc)
glutMotionFunc(MouseMotion)
glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_AMBIENT, lightAmbient)
glLightfv(GL_LIGHT0, GL_DIFFUSE, lightAmbient)
glLightfv(GL_LIGHT0, GL_SPECULAR, lightSpecular)
glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)
glutMainLoop()
