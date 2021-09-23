import sys
import numpy as np
import re
import copy

class cubeio:
    
    def __init__(self,angconv):
        
        self.xorg=np.zeros(3,dtype=float)
        self.cell=np.zeros((3,3),dtype=float)
        self.nv=np.zeros(3, dtype=int)
        self.unit_conv = 1.0
        if angconv:
            self.unit_conv = 1.0/0.529177

        return
        
    def readcube(self,un):

        lines=un.readlines()

###Reading header information
        line=lines[2].strip()
        arr=line.split()
        self.nat=int(arr[0])
        self.pos=np.zeros((self.nat,3),dtype=float)
        self.zv=np.zeros(self.nat,dtype=int)
        for k in range(3):
                self.xorg[k]=float(arr[k+1])

        self.xorg = self.xorg*self.unit_conv

        for k in range(3):
                iline=k+3
                line=lines[iline].strip()
                arr=line.split()
                self.nv[k] = int(arr[0])
                for kk in range(3):
                        self.cell[kk,k] = float(arr[kk+1])

        self.cell = self.cell*self.unit_conv

###Assuming orthogonal box
        self.dx = self.cell[0,0]
        self.dy = self.cell[1,1]
        self.dz = self.cell[2,2]

        nx = self.nv[0]
        ny = self.nv[1]
        nz = self.nv[2]

        self.npts = nx*ny*nz

        tang=False

        if self.npts < 0:
                tang=True
                self.npts=-self.npts
                nx = abs(nx)
                ny = abs(ny)
                nz = abs(nz)

        for iat in range(self.nat):
                iline=6+iat
                line=lines[iline].strip()
                arr=line.split()
                self.zv[iat]=arr[0]
                for k in range(3):
                        self.pos[iat,k] = float(arr[k+2])

        self.pos = self.pos*self.unit_conv
##### Done reading header

        self.data=np.zeros(self.npts, dtype=float)

        ipt=0
        for line in lines[6+self.nat:]:
                arr=line.strip().split()
                nptx = len(arr)
                for k in range(nptx):
                        self.data[ipt] = float(arr[k])
                        ipt += 1

        return (self.data)

    def writecube(self,fnm,a):

        fnm = fnm+".cube"       
        un=open(fnm,"w")
        un.write("Generated by cubeio.py\n")
        un.write("OUTER LOOP: X, MIDDLE LOOP: Y, INNER LOOP: Z\n")

        un.write("%5d%12.6f%12.6f%12.6f\n" %(self.nat, self.xorg[0], self.xorg[1], self.xorg[2]))

        for i in range(3):
             un.write("%5d%12.6f%12.6f%12.6f\n" %(self.nv[i], self.cell[i,0], self.cell[i,1], self.cell[i,2]))

        x = 0.0
        for i in range(self.nat):
            un.write("%5d%12.6f%12.6f%12.6f%12.6f\n" %(self.zv[i], x, self.pos[i,0], self.pos[i,1], self.pos[i,2]))

        for ix in range(abs(self.nv[0])):
            for iy in range(abs(self.nv[1])):
                for iz in range(abs(self.nv[2])):
                    un.write("%12.6f" %(a[ix,iy,iz]))
                    if (iz % 6 == 5):
                        un.write("\n")  
                un.write("\n")
        
        un.close()
        return fnm
