from math import sin,cos,pi
import  universe
import numpy
height = 7
width =10
K=1400000
MASS=1.0
dotj=[]
n=height*width
h=0.2
w=0.2
v_coefj=[0]

for i in range(n):
    r=numpy.array([(i%width)*w,(i//width)*h])
    v=numpy.array([r[1], -r[0]])*v_coefj[i%len(v_coefj)]
    dotj.append(universe.Dot(MASS,r,v,[]))
for i in range(len(dotj)):
    if i//width==0:
        dotj[i].neighborj.append(universe.Neighboring_Dot(dotj[i+width],K))
        if i%width!=0:
            dotj[i].neighborj.append(universe.Neighboring_Dot(dotj[i-1],K))
        if i%width!=width-1:
           dotj[i].neighborj.append(universe.Neighboring_Dot(dotj[i+1],K))
    elif i//width==height-1:
        dotj[i].neighborj.append(universe.Neighboring_Dot(dotj[i-width],K))
        if i%width!=0:
            dotj[i].neighborj.append(universe.Neighboring_Dot(dotj[i-1],K))
        if i%width!=width-1:
           dotj[i].neighborj.append(universe.Neighboring_Dot(dotj[i+1],K))
    else:
        dotj[i].neighborj.append(universe.Neighboring_Dot(dotj[i+width],K))
        dotj[i].neighborj.append(universe.Neighboring_Dot(dotj[i-width],K))
        if i%width!=0:
            dotj[i].neighborj.append(universe.Neighboring_Dot(dotj[i-1],K))
        if i%width!=width-1:
           dotj[i].neighborj.append(universe.Neighboring_Dot(dotj[i+1],K))
unv=universe.Universe(g=9.8,delta_t=0.0005 ,dotj=dotj,
ground_Y=-2.0,universe_R=2.0,ENERGY_CHECK_FREQ=4)