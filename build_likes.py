from pymongo import MongoClient
import pickle


client = MongoClient()
db=client.muzmatch


trim=db.trim

dUK=pickle.load(open('../repos/dUK.pkl','rb'))
i=0

trim = db.trim
dlikesMUK = {}
dlikesFUK = {}
for key in dUK.keys():
    if dUK[key]['age']>20 and dUK[key]['age']<60:
        t = trim.find({'memberID': key}, {"who_i_liked": 1})
        a = trim.find({'memberID': key}, {"activeSince": 1})
        try:
            dUK[key]['activeSince'] = a[0]['activeSince']
        except:
            continue

        for tt in t:
            if 'who_i_liked' in tt.keys():
                likes = len(tt['who_i_liked'])
                if dUK[key]['gender'] == 'M':
                    dlikesMUK[key] = likes
                else:
                    dlikesFUK[key] = likes
        i+=1
        if i%100==0:
            print(i/len(dUK.keys()))

#pickle.dump(dlikesFUK,open('../repos/dlikesFUK.pkl','wb'))
#pickle.dump(dlikesMUK,open('../repos/dlikesMUK.pkl','wb'))
pickle.dump(dUK,open('../repos/dUK.pkl','wb'))