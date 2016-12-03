import os;
import re;
import unicodedata;
import sys;
import random;
import time;
import math;

print ("AVG_PER_START");
print (time.strftime('%Y-%m-%d %H:%M:%S'));

filename="D:"+os.sep+"Tools"+os.sep+"svmlight"+os.sep+"jp-svm-fil-tf.txt";

fold=10;
file1=open(filename,"r");
filedata=file1.readlines();

filei={};
filee={};
for x in range(0,fold):
    filei[x]=open(re.sub('\.txt', ".i"+str(x), filename),"w");
    filee[x]=open(re.sub('\.txt', ".e"+str(x), filename),"w");
x=0;
for line in filedata:
    filei[x].writelines([line]);
    for y in range(0,fold):
        if (y!=x):filee[y].writelines([line]);
    x+=1;
    if(x>=fold) :x=0;

for x in range(0,fold):
    filei[x].close();
    filee[x].close();
file1.close();

#Fold
res=[];
for x in range(0,fold):
    print("TURN "+str(x)+"\n");
    os.system("D:\\Tools\\svmlight\\svm_learn.exe -t 1 "+re.sub('\.txt', ".i"+str(x), filename)+" D:\\tools\\svmlight\\model.txt");
    os.system("D:\\Tools\\svmlight\\svm_classify.exe "+re.sub('\.txt', ".e"+str(x), filename)+" D:\\tools\\svmlight\\model.txt D:\\Tools\\svmlight\\svm_predictions");
    filea=open(re.sub('\.txt', ".e"+str(x), filename),"r");
    fileb=open("D:\\Tools\\svmlight\\svm_predictions","r");
    filedataa=filea.readlines();
    filedatab=fileb.readlines();

    result=[[0,0],[0,0]];
    print (str(len(filedataa))+" "+str(len(filedatab))+"\n");
    for i in range(0,len(filedatab)):
        sec=0;fir=0;
        if (float(filedatab[i].rstrip('\n'))>=0.5): sec=1;
        temp=str.split(filedataa[i]);
        if (int(temp[0])>=0): fir=1;
        result[fir][sec]+=1;
    print ("|"+str(result[0][0])+"|"+str(result[0][1])+"|\n");
    print ("|"+str(result[1][0])+"|"+str(result[1][1])+"|\n");
    if (result[0][0]==0):result[0][0]=0.0001;
    if (result[0][1]==0):result[0][1]=0.0001;
    if (result[1][0]==0):result[1][0]=0.0001;
    if (result[1][1]==0):result[1][1]=0.0001;
    p1=result[1][1]/(result[1][1]+result[0][1]);
    p0=result[0][0]/(result[1][0]+result[0][0]);
    r1=result[1][1]/(result[1][1]+result[1][0]);
    r0=result[0][0]/(result[0][1]+result[0][0]);
    f1=(2*p1*r1)/(p1+r1);
    f0=(2*p0*r0)/(p0+r0);
    print ("Pfor1:"+str(p1)+"\n");
    print ("Rfor1:"+str(r1)+"\n");
    print ("Pfor0:"+str(p0)+"\n");
    print ("Rfor0:"+str(r0)+"\n");
    print ("F1fr1:"+str(f1)+"\n");
    print ("F1fr0:"+str(f0)+"\n");
    res.append([p1,p0,r1,r0,f1,f0]);
    filea.close();
    fileb.close();
    
ap1=0;ap0=0;ar1=0;ar0=0;af1=0;af0=0;
for x in range(0,fold):
    ap1+=p1;
    ap0+=p0;
    ar1+=r1;
    ar0+=r0;
    af1+=f1;
    af0+=f0;
ap1/=fold;ap0/=fold;ar1/=fold;ar0/=fold;af1/=fold;af0/=fold;

print ("======");
print ("Pfor1:"+str(ap1)+"\n");
print ("Rfor1:"+str(ar1)+"\n");
print ("Pfor0:"+str(ap0)+"\n");
print ("Rfor0:"+str(ar0)+"\n");
print ("F1fr1:"+str(af1)+"\n");
print ("F1fr0:"+str(af0)+"\n");

