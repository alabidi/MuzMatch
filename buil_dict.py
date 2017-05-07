from pymongo import MongoClient
import pickle


client = MongoClient()
db=client.muzmatch

collections=[db.n1,db.n2,db.n3,db.n4,db.n5]

def retro_dictify(d, doc, grumps,dUK):
    mid = doc['memberID']
    age = doc['age']

    if age is not None and 'who_i_liked' in doc.keys():

        ethnic = doc['ethnicGroupingName']
        gender = doc['gender']
        status = doc['statusMessage']
        lD = doc['longDescription']
        country = doc['countryName']
        age = int(age)
        d[mid] = {}
        d[mid]['age'] = age

        d[mid]['gender'] = gender
        d[mid]['ethnic'] = ethnic
        d[mid]['SM'] = status
        d[mid]['LD'] = lD
        d[mid]['country'] = country
        d[mid]['numLikes']=len(doc['who_i_liked'])
        if 'who_i_passed' in doc.keys():
            d[mid]['passed']=get_passes(doc['who_i_passed'])
        else:
            d[mid]['passed']=[]

        if country=='United Kingdom':
            dUK[mid]=d[mid]
    elif age is not None and 'who_i_liked' not in doc.keys():
        grumps.append(mid)
    return d,dUK, grumps

def get_passes(d):
    p=[]
    for pp in d:
        p.append(pp.keys())
    return p


d={}
dUK={}
grumps=[] #grumps are people who dont like anyone
for coll in collections:
    print(coll)
    for doc in coll.find({},{'memberID':1,'age':1,'ethnicGroupingName':1,'ethnicOriginCountryName':1,'gender':1,'statusMessage':1,'longDescription':1,'countryName':1,'who_i_liked':1,'who_i_passed':1}):
        d,dUK,grumps=retro_dictify(d,doc,grumps,dUK)


print('we have %s grumps\n'%len(grumps))
pickle.dump(d,open('d.pkl','wb'))
pickle.dump(dUK,open('dUK.pkl','wb'))

print('we have %s global active users of which %s are in the UK\n'%(len(d.keys()),len(dUK.keys())/len(d.keys())))
