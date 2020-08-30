import numpy as np
import pickle
from collections import OrderedDict

def getIndex(s):
	_, headers = get_filters_headers()
	return headers.index(s)

def dumpPickle(name,data):
	pickle.dump(data,open('pickles/{}.pickle'.format(name),'wb'))
	
def loadPickle(name):
	return pickle.load(open('pickles/{}.pickle'.format(name),'rb'))

def get_filters_headers():
	filters=open('filters.txt','r').readline().strip().split('|')
	file="pipeFormat.csv"
	f=open(file,"r")
	headers=f.readline().strip().split('|')
	f.close()
	return filters,headers

def setplot(plt,ax):

    ax.spines["top"].set_visible(False)  
    ax.spines["bottom"].set_visible(False)  
    ax.spines["right"].set_visible(False)  
    ax.spines["left"].set_visible(False)

    ax.get_xaxis().tick_bottom()    
    ax.get_yaxis().tick_left()  
    return plt,ax

def get_basic_stats(list_lt):
	
	return (len(list_lt),np.mean(list_lt),np.percentile(list_lt,10),np.percentile(list_lt,50),np.percentile(list_lt,90))

def get_basic_statsv2(list_lt):
	response = OrderedDict()
	response['n'] = len(list_lt)
	response['Mean'] = np.mean(list_lt)
	response['10th P'] = np.percentile(list_lt,10)
	response['25th P'] = np.percentile(list_lt,25)
	response['50th P'] = np.percentile(list_lt,50)
	response['75th P'] = np.percentile(list_lt,75)
	response['90th P'] = np.percentile(list_lt,90)
	return response