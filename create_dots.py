from math import sin,cos,pi
import  universe
import numpy
K0=1400
MASS=1.0
dotj=[]
n=60
layer_count=2
connect_upper_limit=12
deltaj=[i for i in range(-n,n+1) if i!=0 and ((abs(i)<=12 and (i%2==0 or i%4==0 or i %8==0 or i%10==0 or i %12==0))or i %31==0)]
outer_R=1.0
inner_R=0.2
Rj=[(i+1)/layer_count*(outer_R-inner_R)+inner_R for i in range(layer_count)]
v_coefj=[0]

for i in range(2*n):
    theta=2*pi/(2*n)*i
    
    r=numpy.array([Rj[i%layer_count]*cos(theta),Rj[i%layer_count]*sin(theta)])
    v=numpy.array([r[1], -r[0]])*v_coefj[i%len(v_coefj)]
    dotj.append(universe.Dot(MASS,r,v,[]))

'''R_mid=0.5
mid_dot_count=2
pos_in_midj=[[R_mid*cos(2*pi/mid_dot_count*i),R_mid*sin(2*pi/mid_dot_count*i)] for i in range(mid_dot_count)]
dot_in_midj=[
    universe.Dot(MASS*n/mid_dot_count,numpy.array(pos_in_mid),numpy.array([-0.0,0.0]),
        [universe.Neighboring_Dot(dot,K1) for dot in dotj]
    )   for pos_in_mid in pos_in_midj
    ]'''
for i in range(len(dotj)):
    dotj[i].neighborj=[
        universe.Neighboring_Dot(dotj[(i+delta) % len(dotj)],K0) 
            for delta in deltaj]
    '''+[universe.Neighboring_Dot(dot_in_mid,K1)
            for dot_in_mid in dot_in_midj]
dotj.extend(dot_in_midj)'''
unv=universe.Universe(g=9.8,delta_t=0.0005 ,dotj=dotj,
ground_Y=-1.5,universe_R=1.5,ENERGY_CHECK_FREQ=4)