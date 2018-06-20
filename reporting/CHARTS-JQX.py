#VTZOUM	
#START - OK
# Label Func
def label(t, status):
    if status==0:
        ls='0'
    elif status==1:
        ls='1'
    elif status==2:
        ls='2'
    if t==0:
        lt='A'
    elif t==1:
        lt='B'
    elif t==2:
        lt='C'
    return lt+ls
    	
#test
label (0,1)

####################################################
# Sample Data - to START
#OK
DictL = [{'Lesson': 'A', 'type': 0, 'status': 0, 'count': 6, 'AB':20 }, 
	{'Lesson': 'A', 'type': 0, 'status': 1, 'count': 4 , 'AB':20 }, 
	{'Lesson': 'A', 'type': 1, 'status': 0, 'count': 4 , 'AB':20 }, 
	{'Lesson': 'A', 'type': 1, 'status': 1, 'count': 5 , 'AB':20 }, 
	{'Lesson': 'A', 'type': 1, 'status': 2, 'count': 1 , 'AB':20 }, 
]	



DictLB = [{'Lesson': 'A', 'type': 0, 'status': 0, 'count': 6, 'AB':20 }, 
	{'Lesson': 'A', 'type': 0, 'status': 1, 'count': 4 , 'AB':20 }, 
	{'Lesson': 'A', 'type': 1, 'status': 0, 'count': 4 , 'AB':20 }, 
	{'Lesson': 'A', 'type': 1, 'status': 1, 'count': 5 , 'AB':20 }, 
	{'Lesson': 'A', 'type': 1, 'status': 2, 'count': 1 , 'AB':20 }, 

    {'Lesson': 'B', 'type': 0, 'status': 0, 'count': 3, 'AB':30 }, 
	{'Lesson': 'B', 'type': 0, 'status': 1, 'count': 4 , 'AB':30 }, 
	{'Lesson': 'B', 'type': 1, 'status': 0, 'count': 12 , 'AB':30 }, 
	{'Lesson': 'B', 'type': 1, 'status': 1, 'count': 5 , 'AB':30 }, 
	{'Lesson': 'B', 'type': 1, 'status': 2, 'count': 6 , 'AB':30 }, 
	
]	


#################################################
# Tranforms Dict from Django Aggregates -> 
# JQX Chart Data
#################################################
def makeDict4ChartData(aDict):
    #A.Get unique lesson names
    keys = [i['Lesson'] for i in aDict]
    keys = list(set(keys))
    #print keys
    
    #B.init DictL2 
    nullDict = dict.fromkeys(['AB ','A0','A1','A2', 'B0','B1','B2', 'C0','C1','C2'], 0)
    iDict = {}
    for k in keys:
        iDict[k] = nullDict
    
    #populate 
    for i in aDict:
        key = label(i['type'], i['status'])
        l, iDict[l][key] = i['Lesson'], i['count']
        #DictL2[l]['AB'] = i['AB']
    #print iDict
    
    
    fDict = []
    for k, v in iDict.iteritems():
        d={}
        d['Lesson'], d['data'] = k, v
        fDict.append(d)
    #print fDict
        
    #Final form
    for i in fDict:
        i.update(i['data'])
        i.pop('data')
        print i
    
    #print fDict
    return fDict

#TEst 
fDict = makeDict4ChartData(DictLB)


    """    
    DictL2 = [{'Lesson': 'A', 'AB':30,'A0':8,'A1':5,'A2':0, 'B0':6,'B1':4,'B2':7, 'C0':1,'C1':1,'C2':0}, 
              {'Lesson': 'B', 'AB':22,'A0':4,'A1':5,'A2':0, 'B0':4,'B1':4,'B2':5, 'C0':0,'C1':2,'C2':1},
              ]
    """   

"""   
{'A': {'AB ': 0, 'A1': 4, 'A0': 3, 'A2': 0, 'B0': 12, 'B1': 5, 'B2': 6, 'C2': 0, 'C1': 0, 'C0': 0}, 'B': {'AB ': 0, 'A1': 4, 'A0': 3, 'A2': 0, 'B0': 12, 'B1': 5, 'B2': 6, 'C2': 0, 'C1': 0, 'C0': 0}}
[{'Lesson': 'A', 'data': {'AB ': 0, 'A1': 4, 'A0': 3, 'A2': 0, 'B0': 12, 'B1': 5, 'B2': 6, 'C2': 0, 'C1': 0, 'C0': 0}}, {'Lesson': 'B', 'data': {'AB ': 0, 'A1': 4, 'A0': 3, 'A2': 0, 'B0': 12, 'B1': 5, 'B2': 6, 'C2': 0, 'C1': 0, 'C0': 0}}]
{'AB ': 0, 'A1': 4, 'A0': 3, 'A2': 0, 'B0': 12, 'B1': 5, 'B2': 6, 'C2': 0, 'Lesson': 'A', 'C0': 0, 'C1': 0}
{'AB ': 0, 'A1': 4, 'A0': 3, 'A2': 0, 'B0': 12, 'B1': 5, 'B2': 6, 'C2': 0, 'Lesson': 'B', 'C0': 0, 'C1': 0}
[{'AB ': 0, 'A1': 4, 'A0': 3, 'A2': 0, 'B0': 12, 'B1': 5, 'B2': 6, 'C2': 0, 'Lesson': 'A', 'C0': 0, 'C1': 0}, {'AB ': 0, 'A1': 4, 'A0': 3, 'A2': 0, 'B0': 12, 'B1': 5, 'B2': 6, 'C2': 0, 'Lesson': 'B', 'C0': 0, 'C1': 0}]
    """   





        


####################################################
# Get unique lesson names
#OK
keys = [i['Lesson'] for i in DictL]
keys = list(set(keys))
print keys 


####################################################
#works > remove dups
#OK
keys = []
for i in DictL: 
    if not i['Lesson'] in keys:
        keys.append(i['Lesson'])
        
        
print keys 


#######################################################
#SCRIPT To transform DICTL -> DictL2
#init DictL2
nullDict = dict.fromkeys(['AB ','A0','A1','A2', 'B0','B1','B2', 'C0','C1','C2'], 0)
DictL2 = {}
for k in keys:
    DictL2[k] = nullDict
    #DictL2['Lesson'] = key
    #DictL2['data'] = nullDict

print DictL2


#######################################################
#SEARCH key by value
for a, b in DictL.iteritems():    # for name, age in list.items():  (for Python 3.x)
    if age == search_age:
        print name
       
       
####################################################
# Null Dicst for JQXChart data
nullDict = dict.fromkeys(['AB ','A0','A1','A2', 'B0','B1','B2', 'C0','C1','C2'], 0)

        
#######################################################        
 #populate DictL2
for i in DictL:
    #print k, v
    key = label(i['type'], i['status'])
    l = i['Lesson']
    DictL2[l][key] = i['count']
    #DictL2[l]['AB'] = i['AB']
    print l, key, i['count']

print DictL2


#######################################################        
# Sample Data for JQXChart data - to END
DictL2 = [{'Lesson': 'A', 'data':{'AB':30,'A0':8,'A1':5,'A2':0, 'B0':6,'B1':4,'B2':7, 'C0':1,'C1':1,'C2':0}}, 
		  {'Lesson': 'B', 'data':{'AB':22,'A0':4,'A1':5,'A2':0, 'B0':4,'B1':4,'B2':5, 'C0':0,'C1':2,'C2':1}}
		  ]


#END-OK
#######################################################




#VTZOUM	 > KEYS OF LIST OF KEYS
all_keys = set().union(*(d.keys() for d in DictL))	#OK
[d.values()[0] for d in DictL]


