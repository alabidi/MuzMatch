
from py2neo import Graph,authenticate,Relationship,Node
from pymongo import MongoClient
import pickle

G=Graph()

client = MongoClient()
db=client.muzmatch


trim=db.trim

d=pickle.load(open('../repos/dUK2.pkl','rb'))
pUK=pickle.load(open('../repos/pUK2.pkl','rb'))
pUK=pUK[pUK['likes']<300]
print(pUK)
max_likes=200
i = 0
for key in pUK.index:
	mid = key

	node0 = Node(d[mid]['gender'], mid=mid)
	node0['age'] = int(d[mid]['age'])
	node0['ethnic'] = d[mid]['ethnic']
	node0['status'] = d[mid]['SM']
	G.merge(node0)
	swipes = trim.find_one({'memberID': mid})
	if swipes != [] and swipes is not None:
		for s in swipes['who_i_liked']:
			mid = s
			if mid in d.keys():
				node1 = Node(d[mid]['gender'], mid=mid)
				node1['age'] = int(d[mid]['age'])
				node1['ethnic'] = d[mid]['ethnic']
				node1['status'] = d[mid]['SM']
				node01 = Relationship(node0, 'likes', node1)
				G.merge(node01)
	i += 1
	if i % 10 == 0:
		print(i / len(d.keys()) * 100)

