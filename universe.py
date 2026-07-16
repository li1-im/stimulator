import numpy as np
from numba import jit

from dataclasses import dataclass

@dataclass
class Dot:
    mass: float
    r_vec: np.array
    v_vec: np.array
    neighborj: list
    # the neighborj are those dots that has a string connected to this one.
    
    def __post_init__(self):
        self.a_vec=np.zeros_like(self.v_vec,dtype=float)
    def calc_init_distance(self):
        for neighboring_dot in self.neighborj:
            delta_r=neighboring_dot.dot.r_vec-self.r_vec
            neighboring_dot.initial_distance=np.linalg.norm(delta_r)
@dataclass
class Neighboring_Dot:
        dot: Dot
        K: float
        force: float =0.0
@jit(nopython=True)
def step(k_correct,Elast,g,delta_t,dotsm,r,v,a,ground_Y,neighbours_flat ,counts ,
    k_flat ,init_flat ,Ep=0,Ek=0):
    num=len(dotsm)
    forceflat=[]
    for i in range(num):
        a[i,1]-=g
        v[i]+=delta_t*a[i]
        r[i]+=delta_t*v[i]
        a[i,:]=0.0
        if r[i,1]<ground_Y:
            r[i,1]=ground_Y
            v[i,1]=-v[i,1]
    find =0
    for i in range(num):
        count=counts[i]
        for _ in range(count):
            nfind=neighbours_flat[find]
            kfind=k_flat[find]
            initfind=init_flat[find]
            delta_r=-(r[i]-r[nfind])
            delta_r_magnitude=np.sqrt(delta_r[0]*delta_r[0]+delta_r[1]*delta_r[1])
            delta_r_unit = delta_r / delta_r_magnitude
            force = kfind * (delta_r_magnitude - initfind)
            a[i]+=force/dotsm[i]*delta_r_unit
            Ep+=force**2/4/kfind
            forceflat.append(force)
            find+=1
        Ek += 0.5 * dotsm[i] * (v[i, 0]*v[i, 0] + v[i, 1]*v[i, 1])
        Ep+=dotsm[i]*r[i,1]*g
    
    E=Ek+Ep
    if Elast==None:
        Elast=E
    k_2=(1-((E-Elast)/Ek))
    if k_2>0:
        k_correct=k_2**0.5
    else:
        k_correct=0
    for i in range(num):
        v[i]*=k_correct
    return k_correct,Ep+Ek*k_correct**2,forceflat,Ep
class Universe:
    def __init__(self, g, delta_t, dotj, ground_Y, universe_R=None,ENERGY_CHECK_FREQ=10):
        self.g = g
        self.delta_t = delta_t
        self.dotj = dotj
        self.universe_R = universe_R if universe_R is not None else self.recommended_R()
        self.ground_Y = ground_Y
        self.mass_total = sum([dot.mass for dot in self.dotj])
        self.k_correct=1
        self.ENERGY_CHECK_FREQ=ENERGY_CHECK_FREQ

        for dot in self.dotj:
            dot.calc_init_distance()

        self.dotsm = np.array([dot.mass for dot in self.dotj])
        self.r = np.array([dot.r_vec for dot in self.dotj])
        self.v = np.array([dot.v_vec for dot in self.dotj])
        self.a = np.zeros_like(self.r)
        self.Elast=None
        self.Ep=0
       
       
        dot_to_find={id(dot):i for i , dot in enumerate(self.dotj)}
        neighbours_flat = []
        neighbour_counts=[]
        k_flat = []
        init_flat = []
        for dot in self.dotj:
            count = 0
            for neighbour in dot.neighborj:
                j= dot_to_find[id(neighbour.dot)]
                neighbours_flat.append(j)
                k_flat.append(neighbour.K)
                init_flat.append(neighbour.initial_distance)
                count += 1
            neighbour_counts.append(count)
        self.neighbours_flat = np.array(neighbours_flat, dtype=np.int64)
        self.neighbour_counts = np.array(neighbour_counts, dtype=np.int64)
        self.k_flat = np.array(k_flat, dtype=float)
        self.init_flat = np.array(init_flat, dtype=float)
    def main(self):
        self.k_correct,self.Elast,self.forceflat,self.Ep=step(self.k_correct,self.Elast,self.g,self.delta_t,self.dotsm,self.r,self.v,self.a,self.ground_Y,self.neighbours_flat ,self.neighbour_counts ,
        self.k_flat ,self.init_flat ,Ep=0,Ek=0)
        count =0
        for i, dot in enumerate(self.dotj):
            dot.r_vec[:] = self.r[i]
            dot.v_vec[:] = self.v[i]
            for neighbourdot in dot.neighborj:
                neighbourdot.force = self.forceflat[count]
                count+=1
    def recommended_R(self):
        return max([np.linalg.norm(self.dotj[j].r_vec-self.dotj[i].r_vec) for i in range(len(self.dotj)) for j in range(i+1,len(self.dotj))])*2
