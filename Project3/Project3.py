import sys
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from time import sleep
import csv


from pywavefront import visualization
import pywavefront

track = pywavefront.Wavefront('CarOnTrack/FullTrack.obj')
car   = pywavefront.Wavefront('CarOnTrack/SG_Car.obj')
route = np.genfromtxt('CarOnTrack/RoutWnormal.xyz', delimiter=' ')

r = 40
angle = 0
windowWidth,windowHeight = 800,600

def car_transformation():
    M = np.identity(4)									# identity matrix I
    M = np.dot(M,midTranslated(*v))						# translate to route point
    vec = np.cross(vt,dv)
    vec = vec / np.linalg.norm(vec)
    M = np.dot(M,midRotated(dv,vec,vt))					# rotate to fit route
    M = np.dot(M,midTranslated(0,-4.8,1))				# translate to right lane
    M = np.dot(M,midRotated([0,1,0],[-1,0,0],[0,0,1]))	# rotate to X axis 
    M = np.dot(M,midScaled(0.2,0.2,0.2))				# scale the car size
    M = list(M.T.flatten())
    glMultMatrixf(M)									# multi with glLoadMatrix

def midLookAt(eyex,eyey,eyez,centerx,centery,centerz,upx=0,upy=1,upz=0):
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

def midScaled(x,y,z):
	M = np.array([ 
			[x ,0.,0.,0.],
			[0.,y ,0.,0.],
			[0.,0., z,0.],
			[0.,0.,0.,1.]
		])
	return M	

def midRotated(u,v,w):
	M = np.array([  
			[u[0], v[0], w[0], 0.],
			[u[1], v[1], w[1], 0.], 
			[u[2], v[2], w[2], 0.],
			[  0.,   0.,   0., 1.]
		])
	return M

def midTranslated(x,y,z):
	M = np.array([  
			[1.,0.,0.,x ],
			[0.,1.,0.,y ],
			[0.,0.,1.,z ],
			[0.,0.,0.,1.]
		])
	return M
		

def display():
    global angle
    angle = (angle + 1) % route.shape[0]
    global v,v_1,vt,dv
    v   = route[angle,:3]
    v_1 = route[angle-1,:3]
    vt  = route[angle,3:]
    dv = v - v_1
    dv = dv / np.linalg.norm(dv)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, 0, windowWidth, windowHeight)
    glOrtho(-float(windowWidth)/r,float(windowWidth)/r,-float(windowHeight)/r,float(windowHeight)/r,-windowHeight*10.0,windowHeight*10.0)    
    ##############################################   
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_LIGHTING)       
    midLookAt(*(route[angle-1,0:2]+2*route[angle-1,3:5]),28,*route[angle,:3],0,0,1)
    glPushMatrix() 
    visualization.draw(track)
    glPopMatrix()
    car_transformation()
    glPushMatrix()
    visualization.draw(car)
    glPopMatrix()
    glDisable(GL_LIGHTING)
    
    glLineWidth(3)
    ##############################################
    glutSwapBuffers()
    glutPostRedisplay()
    sleep(0.03)

def reshape(width,height):
    glViewport(0, 0, width, height)

def keyboard( key, x, y ):
    esc = 27
    if key == esc:
        sys.exit()



glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
glutCreateWindow(b'Midterm Project')
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

