from pymongo import MongoClient
import pickle

client = MongoClient()
db=client.muzmatch


trim=db.trim

d=pickle.load(open('../repos/dreal.pkl','rb'))
i=0
with open('alikesb.csv','w') as file:
    for key in d.keys():
        swipes=d[key]['realLikes']
        if swipes!=[] and swipes is not None and swipes!=0:
            for s in swipes:
                file.write('%s,%s\n'%(key,s))
        i+=1
        if i%10==0:
            print(i/len(d.keys())*100)

