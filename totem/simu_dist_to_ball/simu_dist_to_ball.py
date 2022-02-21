from roblib import *
import numpy as np
import matplotlib.pyplot as plt
import sys
import time



def f(X,u):
    θ=X[2,0]
    return array([[cos(θ)], [sin(θ)],[u]])

X=array([[-20],[-10],[4]])
dt= 0.1
a,b = array([[-30],[-4]]), array([[30],[6]])
c,h =array([[30],[-20]]), array([[-30],[30]])
p,g, z=array([[-10],[-4]]), array([[10],[6]]),array([[35],[35]])

L=[c,b,a,h,g,p,z]
ax=init_figure(-40,40,-40,40)
C=zeros((2,2))


while True:
	D=[]

	for i in L:
		i=i.flatten()
		x_=X.flatten()
		d=sqrt((i[1]-x_[1])**2 + (i[0]-x_[0])**2)
		D.append(d)
		
	# for i in range(10):
	indice_min=D.index(min(D))
	obj=L[indice_min]
	time.sleep(0.2)
	for t in arange(0,50,dt):
		clear(ax)
		m=X[0:2]
		phi=arctan2(obj[1,0]-m[1,0],obj[0,0]-m[0,0])
		C[:,0]=(obj-m).T[0]
		C[:,1] = (m-m).T[0]
		e=det(C)/norm(b-a)
		thetabar=phi-arctan(e)
		u=arctan(tan((thetabar-X[2,0])/2))
		draw_tank(X,'darkblue')
		plot2D(hstack((m,obj)),'red')
		plot2D(a,'ro')
		plot2D(b,'ro')
		plot2D(c,'ro')
		plot2D(h,'ro')
		plot2D(p,'ro')
		plot2D(g,'ro') 
		plot2D(z,'ro')   
		X   = X+dt*f(X,u)
		if abs(obj[0]-m[0])<0.3:
			break
	del (L[indice_min])
	pass