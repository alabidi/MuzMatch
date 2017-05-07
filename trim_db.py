from pymongo import MongoClient
import pickle

collections=[db.n1,db.n2,db.n3,db.n4,db.n5]


client = MongoClient()
db=client.muzmatch

db.trim.drop()
trim=db.trim

data='../repos/'

d=pickle.load(open(data+'d.pkl','rb'))


def trim_likes(d ,doc):

    likes=doc[ 'who_i_liked']
    if 'who_i_passed' in doc.keys():
        passes=doc[ 'who_i_passed']

    else:
        passes=[]
    trimmed_likes=[]
    passed=[]
    date=[]
    for l in likes:
        mid=l[ 'user_id1']
        date.append(l['timeStamp'].split(' ')[0])
        if mid in d.keys():
            trimmed_likes.append(mid)
    if passes!=[]:

        for p in passes:
            try:
                mid=p[ 'user_id1']

                if mid in d.keys():
                    passed.append(mid)
            except:
                continue
    doc['who_i_liked']= trimmed_likes
    doc['who_i_passed']=passed

    doc['activeSince']=min(date )
    return doc

for coll in collections:
    for doc in coll.find({}, {'memberID': 1, "who_i_liked": 1, 'who_i_passed': 1}):
        if 'who_i_liked' in doc.keys():
            doc = trim_likes(d, doc)
            if doc['who_i_liked'] != [] and doc[
                'who_i_liked'] is not None:  # ensure that user only likes active users, otherwise assume user effectively inactive

                trim.insert_one(doc)