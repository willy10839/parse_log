from prettytable import PrettyTable
import argparse
parser = argparse.ArgumentParser(description='Auth log parser')
parser.add_argument("filename",help='Log file path')
parser.add_argument('-u',help='Summary failed  login log and sort log by user',action='store_true')
parser.add_argument('-after',help='Filter log after date. format YYYY-MM-DD-HH:MM:SS')
parser.add_argument('-before',help='Filter log before date. format YYYY-MM-DD-HH:MM:SS')
parser.add_argument('-n',help='Show only the users of most N-th times',type=int,default=0)
parser.add_argument('-t',help='Show only the users of attacking equal or more than T times',type=int,default=0)
parser.add_argument('-r',help='Sort in reverse order',action='store_true')


args=parser.parse_args()
logfile=args.filename
log = open(logfile, "r+")
print ("Name of the file: ", log.name)
Ntime=args.n
Ttime=args.t


line = log.read()
#print(line)
timelist=[]
user=[]
countlist=[]
xyz = line.split('\n')
for i in xyz:
	word=i.split()
	position=word.index('from')
	user.append(word[position-1])
countlist.append(user[0])

for i in xyz:
	word=i.split()
	for j in range(3):
		timelist.append(word[j])
	position=word.index('from')
	timelist.append(word[position-1])
#print(timelist)



countList = {}

for i in user:
	if i not in countList:
		countList[i]=1
	else:
		countList[i]+=1

def dict2list(dic:dict):
    keys = dic.keys()
    vals = dic.values()
    lst = [(key, val) for key, val in zip(keys, vals)]
    return lst
#print(countList)

u=sorted(dict2list(countList), key=lambda x:x[0], reverse=False)#-u sort by user
default=sorted(dict2list(countList), key=lambda x:x[1], reverse=True)#default
reverse=sorted(dict2list(countList), key=lambda x:x[1], reverse=False)#reverse

# Close opened file
log.close()

def table(lst:list):
        y = PrettyTable()
        y.field_names=['user','count']
        for i in range (len(lst)):
                y.add_row(lst[i])
        print(y)

def table(lst:list):
	y = PrettyTable()
	y.field_names=['user','count']
	for i in range (len(lst)):
		y.add_row(lst[i])
	print(y)

def tableT(lst:dict,Ttime:int):
	a=lst
	for i in lst.copy():
		if lst[i] < Ttime:
			a.pop(i)
	T=sorted(dict2list(a), key=lambda x:x[1], reverse=True)
	table(T)
	return 0

def tableN(lst:dict,Ntime:int):
	a=lst
	for i in lst.copy():
		if lst[i]>Ntime:
			a[i]=Ntime
	N=sorted(dict2list(a), key=lambda x:x[1], reverse=True)
	table(N)
	return 0

if args.r==True:
	table(reverse)
elif args.u==True:
	table(u)
elif Ttime!=0:
	tableT(countList,Ttime)
elif Ntime!=0:
	tableN(countList,Ntime)
else:
	table(default)
