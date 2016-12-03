import os;
import re;
import unicodedata;
import sys;
import random;
import time;
import math;

if (len(sys.argv)>1):
    traindir=sys.argv[1];
else:
    traindir="D:"+os.sep+"Tools"+os.sep+"csci544";

hamfilelist=[];
spamfilelist=[];

print ("AVG_PER_START");
print (time.strftime('%Y-%m-%d %H:%M:%S'));

for dir in os.walk(traindir):
    if (str(dir[0]).split(os.sep)[-1]=="jp-critical-pre1"):
        hamfilelist+=map(lambda x: dir[0]+os.sep+x,dir[2]);
        #print("Find ham path at:"+dir[0]);
    if (str(dir[0]).split(os.sep)[-1]=="jp-positive-pre1"):
        spamfilelist+=map(lambda x: dir[0]+os.sep+x,dir[2]);
        #print("Find spam path at:"+dir[0]);

wdict={};
ofreq={};
docs=[[],[]];
countword={};
countfile=[0,0];

doctokens=[];

print ("AVG_PER_READ_START");
print (time.strftime('%Y-%m-%d %H:%M:%S'));

#Read SELECTION
fslist=[];
filefs=open("D:"+os.sep+"Tools"+os.sep+"csci544"+os.sep+"fs.txt","r");
fsline=filefs.readlines();
for fs in fsline:
    wordx=str.rstrip(fs,"\n");
    fslist.append(wordx);
filefs.close();


for filegroup in [[hamfilelist,0],[spamfilelist,1]]:
    counter4p2=0;
    #print("Collecting "+hamfilelist[0]);
    for filename in filegroup[0]:
        counter4p2+=1;
        #if (counter4p2%100!=99) :continue;
        #if (filegroup[1]==1 and counter4p2%5!=4) :continue;
        if (counter4p2%2!=1) :continue;
        if (counter4p2%100==99) :print(str(100*counter4p2));
        #print (filename);

        os.system("D:\\tools\\MeCab\\bin\\mecab.exe "+filename+" > D:\\tools\\MeCab\\bin\\out.txt -b 20000");   

        file1=open("D:\\tools\\MeCab\\bin\\out.txt", "r",encoding="utf8");
        linelist=file1.readlines();

        docdict={};
        for line in linelist:
            word=str.split(line,"\t");
            if (len(word)<2):
                continue;
            wordzokusei=str.split(word[1],",");
            #if not((wordzokusei[0] in fslist)):
            #    continue;
            if (not(word[0] in wdict)):
                wdict[word[0]]=len(wdict);
            if (word[0] in docdict):
                docdict[word[0]]+=1;
            else:
                docdict[word[0]]=1;
            if (word[0] in ofreq):
                ofreq[word[0]]+=1;
            else:
                ofreq[word[0]]=1;

        list.append(docs[filegroup[1]],docdict);

        file1.close();
        #print("Collecting "+filename);

print ("AVG_PT3_START");
print (time.strftime('%Y-%m-%d %H:%M:%S'));


#Normalization for idf
kyori=0;
idf={};
for val in ofreq.values():
    kyori+=val*val;
kyori=math.sqrt(kyori);
for key in ofreq.keys():
    idf[key]=ofreq[key]/kyori;

docs2=[[],[]];
#Normalization for tf
for type in range(0,2):
    for doc in docs[type]:
        #type2
        docs2[type].append(dict(doc));
        #for key in docs2.keys():
        #    docs2[key]*=idf[key];
        #type1
        kyori=0;
        for val in doc.values():
            kyori+=val*val;
        kyori=math.sqrt(kyori);
        for key in doc.keys():
            doc[key]/=kyori;
            
#Normalization for tfidf
for type in range(0,2):
    for doc in docs2[type]:
        for key in doc.keys():
            doc[key]*=idf[key];
        kyori=0;
        for val in doc.values():
            kyori+=val*val;
        kyori=math.sqrt(kyori);
        for key in doc.keys():
            doc[key]/=kyori;


file2=open("D:"+os.sep+"Tools"+os.sep+"csci544"+os.sep+"jp-svm-fil-tf.txt", "w",encoding="utf8");
outputlist=[];
for type in range(0,2):
    for doc in docs[type]:
        outputfeaturedict={};
        for word in dict.keys(doc):
            outputfeaturedict[wdict[word]]=doc[word];
        sortedoutputfeaturelist=sorted(outputfeaturedict.items(),key=lambda d:d[0], reverse = False);
            
        output="";
        if (type==1):
            output="+1 ";
        else:
            output="-1 ";
        if (len(outputfeaturedict))<1 :continue;
        #print (sortedoutputfeaturelist);
        for i in range(0,len(sortedoutputfeaturelist)):
            output+=str(sortedoutputfeaturelist[i][0]+1)+":"+str(round(sortedoutputfeaturelist[i][1],8))+" ";

        output+="\n";
        outputlist.append(output);
file2.writelines(outputlist);
file2.close();

file2=open("D:"+os.sep+"Tools"+os.sep+"csci544"+os.sep+"jp-svm-fil-tfidf.txt", "w",encoding="utf8");
outputlist2=[];
for type in range(0,2):
    for doc in docs2[type]:
        outputfeaturedict={};
        for word in dict.keys(doc):
            outputfeaturedict[wdict[word]]=doc[word];
        sortedoutputfeaturelist=sorted(outputfeaturedict.items(),key=lambda d:d[0], reverse = False);
            
        output="";
        if (type==1):
            output="+1 ";
        else:
            output="-1 ";
        if (len(outputfeaturedict))<1 :continue;
        #print (sortedoutputfeaturelist);
        for i in range(0,len(sortedoutputfeaturelist)):
            output+=str(sortedoutputfeaturelist[i][0]+1)+":"+str(round(sortedoutputfeaturelist[i][1],8))+" ";

        output+="\n";
        outputlist2.append(output);
file2.writelines(outputlist2);
file2.close();

sortedwdict=sorted(wdict.items(),key=lambda d:d[1], reverse = False);
file2=open("D:"+os.sep+"Tools"+os.sep+"csci544"+os.sep+"jp-svm1-words.txt", "w",encoding="utf8");
for i in range(0,len(sortedwdict)):
    file2.writelines([str(sortedwdict[i][1]+1)+":"+str(sortedwdict[i][0])+"\n"]);
file2.close();

