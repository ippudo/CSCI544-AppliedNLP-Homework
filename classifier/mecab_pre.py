import os;
import re;
import unicodedata;
import sys;
import random;
import time;

if (len(sys.argv)>1):
    traindir=sys.argv[1];
else:
    traindir="D:"+os.sep+"Tools"+os.sep+"csci544";

hamfilelist=[];
spamfilelist=[];

print ("AVG_PER_START");
print (time.strftime('%Y-%m-%d %H:%M:%S'));

for dir in os.walk(traindir):
    if (str(dir[0]).split(os.sep)[-1]=="jp-critical"):
        hamfilelist+=map(lambda x: dir[0]+os.sep+x,dir[2]);
        #print("Find ham path at:"+dir[0]);
    if (str(dir[0]).split(os.sep)[-1]=="jp-positive"):
        spamfilelist+=map(lambda x: dir[0]+os.sep+x,dir[2]);
        #print("Find spam path at:"+dir[0]);

dict={};
avgdict={};
countword={};
countfile=[0,0];

doctokens=[];

print ("AVG_PER_READ_START");
print (time.strftime('%Y-%m-%d %H:%M:%S'));

for filegroup in [[hamfilelist,0],[spamfilelist,1]]:
    counter4p2=0;
    #print("Collecting "+hamfilelist[0]);
    for filename in filegroup[0]:
        counter4p2+=1;
        #if (counter4p2%10!=1) :continue;
        if (counter4p2%100==99) :print(100*counter4p2);
        file1=open(filename, "r",encoding="utf8");
        file2=open(re.sub('\.txt', '.kai', filename), "w",encoding="utf8");
        linelist=file1.readlines();
        newlinelist=[];

        for line in linelist:
            newline=line.strip();
            newline=re.sub("[\n\r\s]+","",newline);
            newline=re.sub('[\s\u00a0\u3000]+',"",newline);
            newline=re.sub('[\u2010\u058A\u2013\u2011\u02D7\u2012\u207B\u2043\u2212\u208B-]+',"-",newline);
            newline=re.sub('[\u2014\u2500\u2015\uFF0D\uFE63\uFF70]+',"\u30FC",newline);
            newline=re.sub("<.+?>","",newline);
            newlinelist.append(newline);
            file2.writelines(newlinelist);

        file1.close();
        file2.close();
        #print("Collecting "+filename);
