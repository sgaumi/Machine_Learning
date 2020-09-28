pathim="train_images/"
pathlbl="train.csv"

imnb=2527

#label
#0 : all
#1 : all
#2 : no rotate (or only 180)
#3 : no rotate (or only 180)
#4 : no rotate (or only 180)
#5 : all

def get_fname(file_nb):
    return pathim+"train_"+(5-len(str(file_nb)))*'0'+str(file_nb)+".png"

def rotate(img,angle=90):
    import numpy as np
    rot=int(angle/90)
    for i in range(rot):
        img = np.transpose(img)
    return img

def brightness(img,bright=1):
    #img2=img+img*(-1+bright)
    img2=img+bright
    #img2=bright*img
    return img2

def mirror(img,axe='h'):
    import numpy as np
    img2=np.copy(img)
    if axe=='v':
        n=img.shape[1]
        for i in range(n//2):
            img2[:,i]=img[:,n-i-1]
            img2[:,n-i-1]=img[:,i]
    else:
        n=img.shape[0]
        for i in range(n//2):
            img2[i,:]=img[n-i-1,:]
            img2[n-i-1,:]=img[i,:]
    return img2

import shutil
import os
import matplotlib.pyplot as plt
import imageio

try:
    os.mkdir("data_augment")
except:
    print("data_augment already exist")
try:
    os.mkdir("data_augment/normal")
except:
    print("data_augment/normal already exist")
try:
    os.mkdir("data_augment/rotate")
except:
    print("data_augment/rotate already exist")
try:
    os.mkdir("data_augment/brightness")
except:
    print("data_augment/brightness already exist")
try:
    os.mkdir("data_augment/mirror")
except:
    print("data_augment/mirror already exist")
    
f=open(pathlbl,"r")
labels=f.readlines()
f.close()

#for mirror
axe=['h','v']
f=open("data_augment/train_m.csv","w")
f.write("ID,Label\n")
f.close()

#for brightness
f=open("data_augment/train_b.csv","w")
f.write("ID,Label\n")
f.close()

#for rotate
proh=[2,3,4]
angle=[90,180,270]
itr=0
f=open("data_augment/train_r.csv","w")
f.write("ID,Label\n")
f.close()

#for normal
f=open("data_augment/train_n.csv","w")
f.write("ID,Label\n")
f.close()

for i in range(0,imnb+1):
    lbl=int(labels[i+1][16])
    imname=labels[i+1][:15]
    img=plt.imread(pathim+imname)
    
    #mirror
    p_m=axe[i%2]
    imname_m=imname[:11]+"_m"+".png"
    img_m=mirror(img,axe=p_m)
    imageio.imwrite("data_augment/mirror/"+imname_m,img_m)
    f=open("data_augment/train_m.csv","a")
    f.write(imname_m+","+str(lbl)+"\n")
    f.close()
    
    #brightness
    imname_b=imname[:11]+"_b"+".png"
    img_b=brightness(img)
    imageio.imwrite("data_augment/brightness/"+imname_b,img_b)
    f=open("data_augment/train_b.csv","a")
    f.write(imname_b+","+str(lbl)+"\n")
    f.close()
    
    #rotate
    if lbl in proh:
        p_r=180
    else:
        p_r=angle[itr%3]
        itr+=1
    imname_r=imname[:11]+"_r"+".png"
    img_r=rotate(img,angle=p_r)
    imageio.imwrite("data_augment/rotate/"+imname_r,img_r)
    f=open("data_augment/train_r.csv","a")
    f.write(imname_r+","+str(lbl)+"\n")
    f.close()
    
    #normal
    shutil.copy(pathim+imname,"data_augment/normal/"+imname)
    f=open("data_augment/train_n.csv","a")
    f.write(imname+","+str(lbl)+"\n")
    f.close()

