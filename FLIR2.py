# coding:Shift_JIS
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize # Normalizeをimport

f=open("FLIR4.log")

a=f.read()
f_out=open("FLIR4.csv","w")
print(a)
print(len(a))
b = [[0] * 80 for i in range(60)]
c=0

for j in range(60):
   for i in range(80):
       x1=a[c:c+2]
       c=c+3
       x0=a[c:c+2]
       c=c+3
       print(x1,x0)
       b[j][i]=round((int(x1,16)*256+int(x0,16)-27315)*0.01,2)
       print(i,j,b[j][i])
   #print(c)
   #print(len(a))

#print(b[0])
#print(len(b[0]))

for i in range(60):
   for j in range(79):
      f_out.write(str(b[i][j]))
      f_out.write(",")
   f_out.write(str(b[i][79]))
   f_out.write("\n")

i=5
while True:
  i=i+5
  print(b)
  print(len(b))
  xx,yy=[],[]
  xx=np.arange(0,80,1)
  yy=np.arange(0,60,1)

  X, Y = np.meshgrid(xx, yy)
  #b[30][30]=i*i
  #plt.pcolormesh(X, Y, b, cmap='hsv',norm=Normalize(vmin=25, vmax=40)) # 等高線図の生成。cmapで色付けの規則を指定する。
  #plt.pcolormesh(X, Y, b, cmap='hsv')
  plt.pcolormesh(xx,yy,b,cmap='hsv')
  pp=plt.colorbar (orientation="vertical") # カラーバーの表示 

  '''
  h=np.arange(0,20,1.0)

  cont=plt.contourf(xx,yy,b,20)
  plt.xlabel("x")
  plt.ylabel("y")
  plt.colorbar()
  '''
  plt.pause(0.1)
  print(i)
  plt.clf()
     