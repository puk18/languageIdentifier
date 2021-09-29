#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 15:48:00 2018

@author: pulkitwadhwa
"""

import re
import codecs
import math

def preProcess(sentence):
        # strip line, break into words
        # extracting the text sentence from each line
        sentence = "".join(sentence.split())
        sentence = sentence.lower()   # to lower case
        sentence = re.sub(r"\d+", "", sentence) # remove digits
        sentence = re.sub(r'[^\w\s]','',sentence)  #remove punctutations
        sentence=re.sub(' +',' ',sentence)
        sentence=re.sub('\ |\?|\.|\!|\/|\;|\:|\_', '', sentence)
        return list(sentence)

def countNgram(tokens,order):
    pairs=dict()
    if len(tokens)<order:
        #print pairs
        return pairs

    for i in range( len(tokens) - (order+1) ):
        pair=tuple(tokens[i:i + order])
        if pair not in pairs:
            pairs[pair]=0
        pairs[pair]+=0.5
    return pairs

def ngramPrint(ngramDict):
    
    for key,val in sorted(ngramDict.iteritems()):
#        output="P("+''.join(key)+")="+str(val)+"\n"
#        file.write(output)
        print ''.join(key)+":"+str(val)


        
def ngramCount(ngramDict):
    sum = 0
    for key,val in sorted(ngramDict.iteritems()):
        sum+=val
#        print ''.join(key)+":"+str(val)
    print "Assorted Count : ", sum
    return sum

def combinedCounts(countList):
    merged=dict()
    for pairs in countList:
        for key, val in pairs.iteritems():
            if key not in merged:
                merged[key] = 0
            merged[key] += val
    return merged

def smoothen(assortedDict, ngram):
    for i in range(ord('a'), ord('z')+1):
        smoothenDict(assortedDict,  tuple(chr(i).decode('utf-8')), ngram)

absentLexemList = list()
def smoothenDict(assortedDict, lexem, iterIndex):
  if(iterIndex == 0):
    if(lexem not in assortedDict.keys()):
        assortedDict[lexem] = 0
        absentLexemList.append(lexem)
    assortedDict[lexem] +=1.0   
    return
  else:
      for i in range(ord('a'),ord('z')+1):
        searchStr = (lexem + tuple(chr(i).decode('utf-8')))
        smoothenDict(assortedDict, searchStr, iterIndex - 1)
        
        
def unigramProbab(unigramPair):
    probabList=dict()
    totalCount=ngramCount(unigramPair)
    for key,val in unigramPair.iteritems():
        probabList[key]=val/float(totalCount)
    return probabList    



def bigramProbab(bigramPair,unigramPair):
    probabList=dict()
#    totalCount=ngramCount(bigramPair,unigramPair)
    for key,val in bigramPair.iteritems():
        unigramItem=key[0]
        for key1,val1 in unigramPair.iteritems():
            if unigramItem==' '.join(key1):
#                print key1
#                print unigramItem
#                print ' '.join(key1)
#                print val1
                probabList[key]=val/float(val1+(0.5*26*26))
#                print probabList                
    return probabList 

def trigramProbab(trigramPair,bigramPair):
    probabList=dict()
#    totalCount=ngramCount(bigramPair,unigramPair)
    for key,val in trigramPair.iteritems():
        bigramItem=''.join(key[0:2])
#        print bigramItem
        for key1,val1 in bigramPair.iteritems():
            if bigramItem==''.join(key1):
#                print key
#                print key1
#                print bigramItem
                probabList[key]=val/float(val1+(0.5*26*26*26))
#                print probabList                
    return probabList         

def unigramProbabSentence(tokens,uniGramprobabList):
    probab=0
    for i in range(len(tokens)):
        char=' '.join(tokens[i])
        for key,val in uniGramprobabList.iteritems():            
            if char==' '.join(key):
                probab+=math.log(val)
                
    return probab            
def bigramProbabSentence(tokens,biGramprobabList):
    probab=0
    for i in range(len(tokens)):
        char=''.join(tokens[i])
        for key,val in biGramprobabList.iteritems(): 
            if char==''.join(key):
                probab+=math.log(val)
                
    return probab       
    
def trigramProbabSentence(tokens,triGramprobabList):
    probab=0
    for i in range(len(tokens)):
        char=''.join(tokens[i])
        for key,val in triGramprobabList.iteritems(): 
            if char==''.join(key):
                probab+=math.log(val)
                
    return probab                  
def unigramOutput(file,ngramDict):
    
    for key,val in sorted(ngramDict.iteritems()):
        output="P("+''.join(key)+")="+str(val)+"\n"
        file.write(output)
#        print ''.join(key)+":"+str(val)
    file.close()    
def bigramOutput(file,ngramDict):
    
    for key,val in sorted(ngramDict.iteritems()):
        unigramItem=''.join(key[0])
        output="P("+''.join(key[1])+"|"+unigramItem+")="+str(val)+"\n"
        file.write(output)                        
    file.close()
    
def sentenceOutput(file,token,listBigram,unigramDictEn,unigramDictFr,unigramDictOt,bigramDictEn,bigramDictFr,bigramDictGn):
    totalProbabuniEn=0
    totalProbabuniFr=0
    totalProbabuniGn=0
    totalProbabBiEn=0
    totalProbabBiFr=0
    totalProbabBiGn=0
    for i in range(len(token)):
        char=''.join(token[i])
        file.write("UNIGRAM :"+char+"\n")
        for key,val in unigramDictEn.iteritems(): 
            if char==''.join(key):
                totalProbabuniEn+=math.log(val)
                output="ENGLISH: P("+''.join(key)+")="+str(val)+"==>log probab of sentence so far"+str(totalProbabuniEn)+"\n"                
                file.write(output)
                
                
        for key,val in unigramDictFr.iteritems(): 
            if char==''.join(key):
                totalProbabuniFr+=math.log(val)
                output="FRENCH: P("+''.join(key)+")="+str(val)+"==>log probab of sentence so far"+str(totalProbabuniFr)+"\n"
                file.write(output)
               
#                totalProbabFr+=math.log(val)        
        for key,val in unigramDictOt.iteritems(): 
            if char==''.join(key):
                totalProbabuniGn+=math.log(val)
                output="OTHER: P("+''.join(key)+")="+str(val)+"==>log probab of sentence so far"+str(totalProbabuniGn)+"\n"
                file.write(output)              
#                totalProbabGn+=math.log(val) 
    if totalProbabuniEn==max(totalProbabuniEn,totalProbabuniFr,totalProbabuniGn):
        file.write("According to the unigram model, the sentence is in English\n")
        print "According to the unigram model, the sentence is in English"
    elif totalProbabuniFr==max(totalProbabuniEn,totalProbabuniFr,totalProbabuniGn) :
        file.write("According to the unigram model, the sentence is in French\n")
        print "According to the unigram model, the sentence is in French"
    else:
        file.write("According to the unigram model, the sentence is in German\n")
        print "According to the unigram model, the sentence is in German"
    file.write("---------------------\n")    
    for i in range(len(listBigram)):
        char=''.join(listBigram[i])
        file.write("BIGRAM :"+char+"\n")
        for key,val in bigramDictEn.iteritems(): 
            if char==''.join(key):
                totalProbabBiEn+=math.log(val)
                unigramItem=''.join(key[0])
                output="ENGLISH: P("+''.join(key[1])+"|"+unigramItem+")="+str(val)+"==>log probab of sentence so far"+str(totalProbabBiEn)+"\n"                
                file.write(output)
        for key,val in bigramDictFr.iteritems(): 
            if char==''.join(key):
                totalProbabBiFr+=math.log(val)
                unigramItem=''.join(key[0])
                output="FRENCH: P("+''.join(key[1])+"|"+unigramItem+")="+str(val)+"==>log probab of sentence so far"+str(totalProbabBiFr)+"\n"                
                file.write(output)
        for key,val in bigramDictGn.iteritems(): 
            if char==''.join(key):
                totalProbabBiGn+=math.log(val)
                unigramItem=''.join(key[0])
                output="GERMAN: P("+''.join(key[1])+"|"+unigramItem+")="+str(val)+"==>log probab of sentence so far"+str(totalProbabBiGn)+"\n"                
                file.write(output)
    if totalProbabBiEn==max(totalProbabBiEn,totalProbabBiFr,totalProbabBiGn):
        file.write("According to the bigram model, the sentence is in English")
        print "According to the bigram model, the sentence is in English"
    elif totalProbabBiFr==max(totalProbabBiEn,totalProbabBiFr,totalProbabBiGn) :
        file.write("According to the bigram model, the sentence is in French")
        print "According to the bigram model, the sentence is in French"
    else:
        file.write("According to the bigram model, the sentence is in German")
        print "According to the bigram model, the sentence is in German"            
#    return probab
    
    
#def finalizeCount(assortedDict):
#     for key in assortedDict.keys():
#         if key in absentLexemList:
#             assortedDict[key] += 1

if __name__ == "__main__":
    # English Language
    unigramEn=list()
    bigramEn=list()
    trigramEn = list()
    unigramPairsEn = dict()
    bigramPairsEn = dict()
    triGramPairsEn = dict()
    unigramprobabListEn = dict()
    bigramprobabListEn = dict()
    trigramprobabListEn = dict()
    for line in codecs.open('TrainEN.txt','r','utf-8'):
        tokens=preProcess(line)
        unigramEn.append(countNgram(tokens,1))
        bigramEn.append(countNgram(tokens,2))
        trigramEn.append(countNgram(tokens,3))
    unigramPairsEn=combinedCounts(unigramEn)
    bigramPairsEn=combinedCounts(bigramEn)
    smoothen(unigramPairsEn, 0)   # for smoothening
    smoothen(bigramPairsEn, 1)  # for smoothening

    

#    ngramPrint(unigramPairsEn)
#    ngramPrint(bigramPairsEn)
#    ngramPrint(triGramPairsEn)
    unigramprobabListEn=unigramProbab(unigramPairsEn)
    bigramprobabListEn=bigramProbab(bigramPairsEn,unigramPairsEn)
    trigramprobabListEn=trigramProbab(triGramPairsEn,bigramPairsEn)
    file1=open("output/unigramEN.txt","w")
    unigramOutput(file1,unigramprobabListEn)  #print file ooutput
    file2=open("output/bigramEN.txt","w")
    bigramOutput(file2,bigramprobabListEn)   #print file ooutput

#    ngramPrint(trigramprobabListEn)
#    ngramPrint(bigramprobabListEn)
    # French Language
    unigramFr=list()
    bigramFr=list()
    trigramFr = list()
    unigramPairsFr = dict()
    bigramPairsFr = dict()
    triGramPairsFr = dict()
    unigramprobabListFr = dict()
    bigramprobabListFr = dict()
    for line in codecs.open('TrainFR.txt','r','utf-8'):
        tokens=preProcess(line)
        unigramFr.append(countNgram(tokens,1))
        bigramFr.append(countNgram(tokens,2))
    unigramPairsFr=combinedCounts(unigramFr)
    bigramPairsFr=combinedCounts(bigramFr)
   
    smoothen(unigramPairsFr, 0)
    smoothen(bigramPairsFr, 1)

    


#    ngramPrint(unigramPairsFr)
#    ngramPrint(bigramPairsFr)
#    ngramPrint(triGramPairsFr)
    unigramprobabListFr=unigramProbab(unigramPairsFr)
    bigramprobabListFr=bigramProbab(bigramPairsFr,unigramPairsFr)

    file3=open("output/unigramFR.txt","w")
    unigramOutput(file3,unigramprobabListFr)  #print file ooutput
    file4=open("output/bigramFR.txt","w")
    bigramOutput(file4,bigramprobabListFr)   #print file ooutput
    # German Language
    unigramGn=list()
    bigramGn=list()
    trigramGn = list()
    unigramPairsGn = dict()
    bigramPairsGn = dict()
    triGramPairsGn = dict()
    unigramprobabListGn = dict()
    bigramprobabListGn = dict()
    for line in codecs.open('TrainOT.txt','r','utf-8'):
        tokens=preProcess(line)
        unigramGn.append(countNgram(tokens,1))
        bigramGn.append(countNgram(tokens,2))
        trigramGn.append(countNgram(tokens,3))
    unigramPairsGn=combinedCounts(unigramGn)
    bigramPairsGn=combinedCounts(bigramGn)
    
    smoothen(unigramPairsGn, 0)
    smoothen(bigramPairsGn, 1)
    
    

#    ngramPrint(unigramPairsGn)
#    ngramPrint(bigramPairsGn)
#    ngramPrint(triGramPairsGn)
    unigramprobabListGn=unigramProbab(unigramPairsGn)
    bigramprobabListGn=bigramProbab(bigramPairsGn,unigramPairsGn)
    

    file5=open("output/unigramOT.txt","w")
    unigramOutput(file5,unigramprobabListGn) #print file ooutput
    file6=open("output/bigramOT.txt","w")
    bigramOutput(file6,bigramprobabListGn)  #print file ooutput
    j=1
    for line in codecs.open('Test.txt','r','utf-8'):
        
        bigramList=list()
        trigramList=list()
        token=preProcess(line) 
        for i in range(len(token)-1):
            bigramList.append(''.join(token[i:i+2]))
       
        print line    
        fileoutPut=open("output/out"+str(j)+".txt","w")
        fileoutPut.write(line.encode('utf-8')+"\n")
        fileoutPut.write("UNIGRAM MODEL: \n")
        print "UniProbab for english"+str((unigramProbabSentence(token,unigramprobabListEn)))
        print "UniProbab for French"+str((unigramProbabSentence(token,unigramprobabListFr)))
        print "UniProbab for German"+str((unigramProbabSentence(token,unigramprobabListGn)))        
        print "biProbab for english"+str((bigramProbabSentence(bigramList,bigramprobabListEn)))
        print "biProbab for French"+str((bigramProbabSentence(bigramList,bigramprobabListFr)))
        print "biProbab for German"+str((bigramProbabSentence(bigramList,bigramprobabListGn)))
        
       

        sentenceOutput(fileoutPut,token,bigramList,unigramprobabListEn,unigramprobabListFr,unigramprobabListGn,bigramprobabListEn,bigramprobabListFr,bigramprobabListGn)
        j=j+1
        fileoutPut.close()
