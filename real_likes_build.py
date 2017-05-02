
from py2neo import Graph,authenticate,Relationship,Node
from pymongo import MongoClient
import pickle

G=Graph()

client = MongoClient()
db=client.muzmatch



d=pickle.load(open('../repos/dUK2.pkl','rb'))
collection=[db.n1,db.n2,db.n3,db.n4,db.n5]

def trim_likes(doc):
    likes = doc['who_i_liked']
    if 'who_i_viewed' in doc.keys():
        views=doc['who_i_viewed']

        trimmed_likes = []
        all_views=[]
        date = []
        for l in likes:
            mid = l['user_id1']
            date.append(l['timeStamp'].split(' ')[0])
            if mid in d.keys():
                trimmed_likes.append(mid)
        for v in views:
            mid=v['user_id1']
            if mid in d.keys():
                all_views.append(mid)

        slikes = set(trimmed_likes)
        sviews=set(all_views)
        real_likes=slikes.intersection(sviews)

        return real_likes
    else:
        return 0

d2={}
i=0
for col in collection:
    for doc in col.find({},{'memberID':1,'who_i_liked':1,'who_i_viewed':1}):
        if doc['memberID'] in d.keys():
            d2[doc['memberID']]={}
            d2[doc['memberID']]['realLikes']=trim_likes(doc)
            i+=1
            if i%10==0:
                print(i/len(d.keys())*100)




pickle.dump(d2,open('../repos/dreal.pkl','wb'))