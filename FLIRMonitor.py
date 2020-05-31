#coding:Shift-JIS

import serial
import serial.tools.list_ports
import numpy as np
import matplotlib.pyplot as plt
import time

import math
import numpy as np
import matplotlib.pyplot as plt

import struct
from matplotlib.colors import Normalize # Normalizeをimport


'''シリアル通信でデータの送受信を行う'''
def uart_write_read(w_data, r_size):
    # Write
    ser.write(w_data)
    print('Send: '+ str(w_data))

    # Read
    r_data = ser.read_until(size=r_size) #size分Read
    print('Recv: ' + str(r_data))

    return r_data

'''有効なCOMポートを自動的に探して返す'''
def search_com_port():
    coms = serial.tools.list_ports.comports()
    comlist = []
    for com in coms:
        comlist.append(com.device)
    print('Connected COM ports: ' + str(comlist))
    use_port = comlist[0]
    print('Use COM port: ' + use_port)

    return use_port

def getdata(ser):
    datc=[]
    dat=[]
    ser.write(b"1")
    time.sleep(1)
    while True:
        #r_data = ser.readline()
        r_data = ser.read(ser.inWaiting())
        print("datalen:",len(r_data))
        print(r_data)
        print("==========================")
        x=0
        if len(str(r_data)) > 3:
           for c in range(80):
                for r in range(32):
                    #print(r_data[x:x+2])
                    d=int.from_bytes(r_data[x:x+2], byteorder='little')
                    #print("----",d)
                    datc.append((d-8192)/30.0+28)
                    #datc.append(d)
                    x=x+2
                #print(datc)
                dat.append(datc)
                datc=[]
           print(dat)
           boardtemp=int.from_bytes(r_data[x:x+2], byteorder='little')
           print("bbbb",r_data[x:x+2],x)
           x=x+2
           for qq in range(20):
              term=int.from_bytes(r_data[x:x+2], byteorder='little')
              print("term",r_data[x:x+2],x)
              x=x+2
           
           extra=int.from_bytes(r_data[x:x+2], byteorder='little')
           print(boardtemp)
           print(term)
           print(extra)



           #r_data2 = ser.read(ser.inWaiting())
           #print("waiting:",len(r_data2))
           #print(r_data2)
           break

        if len(str(r_data)) == 3:
           print("333333")
           print(len(str(r_data)))
           break

    np.savetxt("out.csv",dat,delimiter=',')

    yy,zz=[],[]
    yy=np.arange(0,32,1)
    zz=np.arange(0,80,1)
    #print(dat[0])

    h=np.arange(30,32,0.1)
    #print(h)
    cont=plt.contourf(yy,zz,dat,20)
    #cont.clabel(fmt='%1.f',fontsize=6)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.colorbar()
    plt.show()



'''Main関数'''
if __name__ == '__main__':
    # Search COM Ports
    use_port = search_com_port()
    use_port="COM16"
    print(use_port)
    
    
    # Init Serial Port Setting
    ser = serial.Serial(use_port,115200)
    #ser.baundrate = 115200
    ser.timeout = 0.5 #sec
    
    sync=0
    buf = [[0] * 160 for i in range(60)]
    pict = [[0] * 80 for i in range(60)]
    print(type(buf))
    buf[0][0]=124
    print(buf[0][0])
    c=0
    r=0
    display=0
    f_out=open("FFFF.csv","w")
    f_out2=open("FF_hex.log","w")
    f_out3=open("FF_temp.log","w")
    
    xb=0
    xn=0
    tgl=False

    pictnum=0

    while True:
        
        r_data = ser.read(10000)
        x=0
        length=len(r_data)
        print(length)
        d0=hex(int.from_bytes(r_data[0:2], byteorder='little'))
        d1=hex(int.from_bytes(r_data[2:4], byteorder='little'))
        d2=int.from_bytes(r_data[0:1], byteorder='little')
        d3=int.from_bytes(r_data[1:2], byteorder='little')
        d4=hex(d2)
        d5=hex(d3)

        print("-----",d0,d2,d3,d4,d5,d1)
        if d0 == "0xadde" and d1 == "0xefbe":
           f_out2.write("\nStart\n")
           f_out3.write("\nStart\n")
           print("hit")
           sync=1
           c=0
           r=0
           x=4
           for i in range(length-4):
              #print(c,r,x,i)
              xn=hex(int.from_bytes(r_data[x:x+1], byteorder='little'))[2:4]
              if tgl == True:
                 tmp=round((int(xb,16)*256+int(xn,16)-27315)*0.01,2)
                 msg='{},{},{}{},{}\n'.format(c,r,xb,xn,tmp)
                 f_out2.write(msg)
              xb=xn
              tgl=not tgl
              
              buf[c][r]=int.from_bytes(r_data[x:x+1], byteorder='little')
              #print(c,r,hex(buf[c][r]))
              x=x+1
              r=r+1
              if r>159:
                 r=0
                 c=c+1

        elif sync==1:
           print("in")
           for i in range(length):
              #print(c,r,hex(buf[c][r]))
              xn=hex(int.from_bytes(r_data[x:x+1], byteorder='little'))[2:4]
              if tgl == True:
                 tmp=round((int(xb,16)*256+int(xn,16)-27315)*0.01,2)
                 msg='{},{},{}{},{}\n'.format(c,r,xb,xn,tmp)
                 f_out2.write(msg)
              xb=xn
              tgl=not tgl

              buf[c][r]=int.from_bytes(r_data[x:x+1], byteorder='little')
              x=x+1
              r=r+1
              if r>159:
                  r=0
                  c=c+1

              if r==0 and c==60:
                 sync=0
                 c=0
                 display=1
           #print("r=",r," c=",c,"disp",display)
        if display == 1:
           for i in range(59):
              for j in range(159):
                  f_out.write(str(buf[i][j]))
                  f_out.write(",")
              f_out.write(str(buf[i][159]))
              f_out.write("\n")
           display=0
           
           f_out2.write("start\n")
           max_val=-10000
           for i in range(60):
              for j in range(0,159,2):
                 #pict[i][int(j/2)]=buf[i][j]+buf[i][j+1]*256
                 val=round((buf[i][j]*256+buf[i][j+1]-27315)*0.01,2)
                 pict[i][int(j/2)]=val
                 max_val=max(val,max_val)
                 f_out3.write(str(pict[i][int(j/2)]))
                 f_out3.write(",")
              f_out3.write("\n")

           yy,zz=[],[]
           yy=np.arange(0,80,1)
           zz=np.arange(0,60,1)
           #print(yy,zz)
           #h=np.arange(0,20,1.0)
           #cont=plt.contourf(yy,zz,pict,20)
           plt.pcolormesh(yy, zz, pict, cmap='hsv',norm=Normalize(vmin=25, vmax=40))
           cont=plt.contourf(yy,zz,pict,30)
           print("KKKK",pict[0][0],pict[0][79],pict[59][0],pict[59][79])
           plt.xlabel("x")
           plt.ylabel("y")
           plt.colorbar()
           msg='Max:{}'.format(max_val)
           plt.text(10,65,msg)
           plt.savefig("img/fig"+str(pictnum)+".jpg")
           pictnum=pictnum+1
           plt.pause(0.01)
           plt.clf()
           print("PINT")




        '''
        print("-",len(r_data))
        #print(r_data[0:6])
        print("KKKKKKKK")
        d=hex(int.from_bytes(r_data[0:8], byteorder='little'))
        print(d)
        
        x=0
        for i in range(30):
           d=hex(int.from_bytes(r_data[x:x+2], byteorder='big'))
           print(d)
           x=x+2
        '''
        '''
           d=int.from_bytes(r_data[0:30], byteorder='little')
        print(d)
        d=int.from_bytes(r_data[0:30], byteorder='big')
        print(d)
        '''



