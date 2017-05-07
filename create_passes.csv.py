from pymongo import MongoClient
import pickle

client = MongoClient()
db=client.muzmatch


trim=db.trim

d=pickle.load(open('dUK.pkl','rb'))
i=0
with open('apassedb.csv','w') as file:
    for key in d.keys():
        swipes=trim.find_one({'memberID':key})
        if 'who_i_passed' in swipes.keys():
            if swipes['who_i_passed']!=[] and swipes['who_i_passed'] is not None:
                for s in swipes['who_i_passed']:
                    print(s)
                    file.write('%s,%s\n'%(key,s))
        i+=1
        if i%10==0:
            print(i/len(d.keys())*100)

