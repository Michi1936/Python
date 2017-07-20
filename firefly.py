import bpy
import numpy as np

#delete all materials
for material in bpy.data.materials:
    material.user_clear()
    bpy.data.materials.remove(material)

#delete all objects
for obj in bpy.data.objects:
    if(obj.type=='MESH'):
        obj.select=True
    else:
        obj.select=False

bpy.ops.object.delete()

#calculation for firefly synchronization 
N=100
dim=2
thres=0.5
T=500
dt=0.1
pi=np.pi
omega=np.ones((N))*0.3
theta=np.random.rand(N)*2*pi
tmptheta=np.zeros(N)
diff=np.zeros(dim)

pos=np.random.rand(N,dim)*0.7
for i in range(N):
    pos[i][0]=pos[i][0]*2
time = np.arange(0,T,dt)
res=np.zeros((N,int(T)))

A=np.zeros((N,N))

def resetting(dist):
    if(dist<=thres):
        return (1-dist/thres)*0.003#strength of resetting
    elif(dist>thres):
        return 0

for i in range(N):
    for j in range(N):
        for k in range(dim):
            diff[k]=pos[i][k]-pos[j][k]
        sum=0
        for k in range(dim):
            sum+=diff[k]*diff[k]
        dist=np.sqrt(sum)
        A[i][j]=resetting(dist)
 
for t in range(int(T/dt)):
    sum=0
    for i in range(N):
        tmptheta[i]=theta[i]
    for i in range(N):
        if(t%10==0):
            res[i][int(t/10)]=np.mod(theta[i],2*pi)
        sum=0
        for j in range(N):
            sum+=A[i][j]*np.sin(tmptheta[j]-tmptheta[i])
        theta[i]+=(omega[i]+sum)*dt
        
#add spheres
for i in range(N):
    bpy.ops.mesh.primitive_ico_sphere_add(size=0.05, location=(pos[i][0]*3.0,pos[i][1]*3,0))
#add material
for obj in bpy.data.objects:
    if(obj.type=='MESH'):
        mat=bpy.data.materials.new('Fire')
        mat.diffuse_color=(0.85,1.0,0.5)
        mat.emit=1.0
        obj.data.materials.append(mat)

START=0
END=T

bpy.context.scene.frame_start=START
bpy.context.scene.frame_end=END

bpy.context.scene.frame_set(START)

for t in range(T):
    bpy.context.scene.frame_set(t)
    i=0
    for mat in bpy.data.materials:
        #mat.diffuse_color=(res[i][t*correc]/(2*pi),res[i][t*correc]/(2*pi),res[i][t*correc]/(2*pi))
        mat.emit=res[i][t]/(2*pi)
        #mat.keyframe_insert(data_path='diffuse_color')
        mat.keyframe_insert(data_path='emit')
        i=i+1

    
    
