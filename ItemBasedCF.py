#coding:utf-8

import random
import math

class ItemBasedCF:

    #The constructor function
    def __init__(self,filename):
        self.filename=filename
        #self.N=N
        self.loadData()
        self.itemSimilarityBest()
        
    #read in the data file
    def loadData(self):
        
        filename=self.filename
        self.train=dict()
        self.test=dict()
        #insert
        #self.itemCount=dict()
        #end
        fi=open(filename)
        lineNum=0
        for line in fi:
            lineNum+=1
            if lineNum==1:
                continue
            uid,iid,t,timestamp=line.split('::')
            u=int(uid)
            i=int(iid)
            tag=t
            time=int(timestamp)
            if time >= 1135313387 and time < 1176596847:
                self.train.setdefault(u,{})
                self.train[u].setdefault(i,[])
                self.train[u][i].append(t)
                
                # insert
                #self.itemCount.setdefault(i,0)
                #self.itemCount[i] += 1
                #end
                
            elif time >= 1176596847 and time <= 1177201647:
                self.test.setdefault(u,{})
                self.test[u].setdefault(i,[])
                self.test[u][i].append(t)
        fi.close()
        print "Load data success.The total records is %d." % (lineNum)
        print "The total train number is %d." % (len(self.train))
        print "The total test number is %d." % (len(self.test))
        print "##################load data end#######################\n"
    
     

    def itemSimilarityBest(self):
      records=self.train
      self.itemSimBest = dict()
      item_user_count = dict() # 倒查表
      #count{i:{j:value}} the number of users who both like item i and j
      count = dict()

      for user,item in records.items():
          for i in item.keys():
              item_user_count.setdefault(i,0)
              item_user_count[i] += 1
              for j in item.keys():
                  if i == j:continue
                  count.setdefault(i,{})
                  count[i].setdefault(j,0)
                  count[i][j] += 1
    
      for i,related_items in count.items():
          self.itemSimBest.setdefault(i,dict())
          for j,cuv in related_items.items():
              self.itemSimBest[i].setdefault(j,0)
              self.itemSimBest[i][j] = cuv / math.sqrt(item_user_count[i] * item_user_count[j] * 1.0)
     

    def recommend(self,user,k = 8,nitem = 40):
        train = self.train
        rank = dict()
        interacted_items = train.get(user,{})
        for i,pi in interacted_items.items():
            for j,wj in sorted(self.itemSimBest[i].items(),key = lambda x : x[1],reverse = True)[0:k]:
                if j in interacted_items :
                    continue
            rank.setdefault(j,0)
            rank[j] +=wj
        return sorted(rank.items(),key = lambda x :x[1],reverse = True)[0:nitem]
 

    def precisionAndRecall(self,N,nitem):
       
        hit=0
        h_recall=0
        h_precision=0
        
        for user,items in self.test.items():
        
            rank=self.recommend(user,N,nitem)
            for item,rui in rank:
                if item in items:
                    hit+=1
           
            h_recall+=len(items)
            h_precision+=len(rank)
       
        recall =(hit/(h_recall*1.0))
        precision = (hit/(h_precision*1.0))
        F1 = 2*precision*recall/(precision+recall)
        return recall,precision,F1
        
         
 

def testItemBasedCF():
  
  cf = ItemBasedCF('movie.dat')

  cf.itemSimilarityBest()

  print "%3s%20s%20s%20s" % ('K',"recall",'precision','F1')

  for k in [3,5,10,20,40,60,80,160]:
    
    recall,precision,F1 = cf.precisionAndRecall(N = k,nitem = 50)

    print "%3d%19.3f%%%19.3f%%%19.3f" % (k,recall * 100,precision * 100,F1 * 100)

 

if __name__ == "__main__":
  
  testItemBasedCF()
