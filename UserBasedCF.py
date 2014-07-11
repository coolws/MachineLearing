#coding:utf-8
import random
import math

class UserBasedCF:

    #The constructor function
    def __init__(self,filename):
        self.filename=filename
        #self.N=N
        self.loadData()
        self.userSimilarityBest()
        
    #read in the data file
    def loadData(self):
        
        filename=self.filename
        self.train=dict()
        self.test=dict()
        #insert
        self.itemCount=dict()
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
                self.itemCount.setdefault(i,0)
                self.itemCount[i] += 1
                #end
                
            elif time >= 1176596847 and time <= 1177201647:
                self.test.setdefault(u,{})
                self.test[u].setdefault(i,[])
                self.test[u][i].append(t)
        fi.close()
        print "The total records is %d." % (lineNum)
        print "The total train number is %d." % (len(self.train))
        print "The total test number is %d." % (len(self.test))
        print "###################################################\n"
    
     

    def userSimilarityBest(self):
      records=self.train
      self.userSimBest = dict()
      reverse_user_items = dict() # 倒查表
      for u,items in records.items():
          for i in items.keys():
              reverse_user_items.setdefault(i,set())
              if u in reverse_user_items[i]:
                  continue
              else:
                  reverse_user_items[i].add(u)

      user_item_count = dict()
      count = dict()
      for item,users in reverse_user_items.items():
          for u in users:
              user_item_count.setdefault(u,0)
              user_item_count[u] += 1
              for v in users:
                  if u == v:continue
                  count.setdefault(u,{})
                  count[u].setdefault(v,0)
                  # insert
                  #两个用户对冷门电影采取过相同的行为更能说
                  #明他们兴趣的相似度。某电影的受欢迎程度越高，则分子取值越低。
                  count[u][v] += 1.0/(1.0*math.log(1.0+self.itemCount[item])) 
                  #count[u][v] += 1
                  #end
                  

      for u ,related_users in count.items():
          self.userSimBest.setdefault(u,dict())
          for v, cuv in related_users.items():
            #self.userSimBest[u][v] = (1.0/(1.0*math.log(1.0+cuv))) / math.sqrt(user_item_count[u] * user_item_count[v] * 1.0) 
            self.userSimBest[u][v] = cuv / math.sqrt(user_item_count[u] * user_item_count[v] * 1.0)


     

    def recommend(self,user,k = 8,nitem = 40):
        train = self.train
        rank = dict()
        interacted_items = train.get(user,{})
        for v ,wuv in sorted(self.userSimBest[user].items(),key = lambda x : x[1],reverse = True)[0:k]:
            for i , rvi in train[v].items():
                if i in interacted_items:
                    continue
                rank.setdefault(i,0)
                rank[i] += wuv
        return sorted(rank.items(),key = lambda x :x[1],reverse = True)[0:nitem]

 

    def precisionAndRecall(self,N,nitem):
        
        hit=0
        h_recall=0
        h_precision=0
        for user,items in self.test.items():
            if user not in self.userSimBest.keys():
                continue
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


         
 

def testUserBasedCF():
  
  cf = UserBasedCF('movie.dat')

  cf.userSimilarityBest()

  print "%3s%20s%20s%20s" % ('K',"recall",'precision','F1')

  for k in [3,5,10,20,40,60,80,160]:
    
    recall,precision,F1 = cf.precisionAndRecall(N = k,nitem = 50)

    print "%3d%19.3f%%%19.3f%%%19.3f" % (k,recall * 100,precision * 100,F1 * 100)

 

if __name__ == "__main__":
  
  testUserBasedCF()
