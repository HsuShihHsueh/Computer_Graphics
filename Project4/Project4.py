import sys
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from time import sleep
import cv2

from pywavefront import visualization
import pywavefront

object_list = [ #create 3 object and their parameters
  # mode,  name ,        obj data ,   r, carmea vector
    ('O','Dog3' ,'model/Dog3.obj' ,  30, [  -10,   10,  10, 0,  0,  0]),
    ('O','Hand' ,'model/Hand.obj' ,  50, [   10,  210,  10, 0,200,  0]),
    ('O','mouse','model/mouse.obj',  80, [  100,   0, 140, 0,  0,140, 0,0,-1]),
    ('P','Dog3' ,'model/Dog3.obj' , 130, [-1500,1500,1500, 0,  0,  0]),
    ('P','Hand' ,'model/Hand.obj' , 130, [ 1000,1000,1000, 0,200,  0]),
    ('P','mouse','model/mouse.obj',  40, [  100,   0, 140, 0,  0,140, 0,0,-1]),
]

wholeWidth,wholeHeight = 8000,6000
amplify = 10 # amplify 800x600 picture 10x10 times
windowWidth,windowHeight = int(wholeWidth/amplify),int(wholeHeight/amplify)


def drawCoordinate():
    glLineWidth(3)
    glBegin(GL_LINES)
    glColor3f(1,0,0)
    glVertex3f(0,0,0)
    glVertex3f(1000,0,0)
    glColor3f(0,1,0)
    glVertex3f(0,0,0)
    glVertex3f(0,1000,0)
    glColor3f(0,0,1)
    glVertex3f(0,0,0)
    glVertex3f(0,0,1000)
    glEnd()

def midLookAt(eyex,eyey,eyez,centerx=0,centery=0,centerz=0,upx=0,upy=1,upz=0):  # =gluLookat
    w = np.array([eyex,eyey,eyez])-np.array([centerx,centery,centerz])
    w = w / np.linalg.norm(w)
    U = np.array([upx,upy,upz])
    u = np.cross(U,w)   
    u = u / np.linalg.norm(u)
    v = np.cross(w,u)
    M = [ 
        [u[0], v[0], w[0], eyex],
        [u[1], v[1], w[1], eyey], 
        [u[2], v[2], w[2], eyez],
        [  0.,   0.,   0.,   1.]
    ]   
    M = list(np.linalg.inv(M).T.flatten())
    glLoadMatrixf(M)

def save_pic():
    colorBuffer = (GLubyte * (windowWidth*windowHeight*3) )(0) # 1440000 == 800*600*3
    glReadPixels(0, 0, windowWidth, windowHeight, GL_BGR, GL_UNSIGNED_BYTE, colorBuffer)
    imgColorflip = np.fromstring(colorBuffer, np.uint8).reshape( windowHeight, windowWidth, 3 )
    imgColor = cv2.flip(imgColorflip, 0) 
    img_buffer.append(imgColor)	  #store in img_buffer


def display():     
    global count,img_buffer
    for mode,name,obj_file,r,camera_vector in object_list:
        obj_data = pywavefront.Wavefront(obj_file)
        img_buffer = []
        count = 0
        while 1:            
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glViewport(0,0,windowWidth,windowHeight)
            x,y = count//amplify,count%amplify #capture piece screen,ex: 86=>x=8,y=6
            left,right = wholeWidth*(-1+x*2/amplify)/r,wholeWidth*(-1+(x+1)*2/amplify)/r
            buttom,top = wholeHeight*(-1+y*2/amplify)/r,wholeHeight*(-1+(y+1)*2/amplify)/r
            if mode == 'P': # use glFrustum to create perspective mode
                glFrustum(left/r,right/r,buttom/r,top/r, 5,4000)
            else:   # use glOrtho to create orthogonal mode
                glOrtho(left,right,buttom,top,-windowHeight*10.0,windowHeight*10.0)    
            glMatrixMode(GL_MODELVIEW)
            midLookAt(*camera_vector)
            glEnable(GL_LIGHTING)
            visualization.draw(obj_data)
            glDisable(GL_LIGHTING)   
            glutSwapBuffers()
            glutPostRedisplay() 
            save_pic()   
            count += 1    
            if count > amplify**2:  
                print() 
                img_buffer2 = []
                img_buffer.pop(0) # delete first dummy picture
                for i in range(amplify):
                    img_buffer2.append(np.vstack(img_buffer[i*amplify:i*amplify+amplify][::-1])) # combine row 
                image =  np.hstack(img_buffer2) # combine column
                cv2.imwrite('output/'+mode+'_'+name+'.JPG',image)  
                sleep(0.5) 
                break
    sys.exit()
    

def reshape(width,height):
    glViewport(0, 0, width, height)

def keyboard( key, x, y ):
    esc = 27
    if key == esc:
        sys.exit()



glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
glutCreateWindow(b'Homework3')
glutReshapeWindow(windowWidth,windowHeight)
glutReshapeFunc(reshape)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
lightAmbient = [ 0.5,0.5,0.5,1.0 ]
lightDiffuse = [ 0.9,0.9,0.9,1.0 ]
lightSpecular = [ 1.0,1.0,1.0, 1.0 ]
lightPosition = [ 0,1000,1000,1.0 ]
glLightfv(GL_LIGHT0, GL_AMBIENT, lightAmbient)
glLightfv(GL_LIGHT0, GL_DIFFUSE, lightAmbient)
glLightfv(GL_LIGHT0, GL_SPECULAR, lightSpecular)
glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)
glutMainLoop()

