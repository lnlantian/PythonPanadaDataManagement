import cx_Oracle
import arrow
import datetime
import os
import re
import pandas as pd
import json


####################################################################################
#This needs to be further tested, may exist flaws, correspond to the functions in PandaVisuilzation 
####################################################################################


def recusiveTree(tree, appendStr = '', appendList = []):

	if('#text' not in tree and '@USERID' not in tree):
		orgStr = appendStr

		for x in tree:
			if(x != 'properties'):
				appendStr += str(x)+'.'
			recusiveTree(tree[x],appendStr)
			appendStr = orgStr
	else:
		if(appendStr is not ''):
			for key in tree:
				appendList.append(appendStr+key)
			
	return appendList




'''
{u'properties': 
	{u'ASSIGNED': 
		{u'properties': 
			{u'#text': 
				{u'index': u'not_analyzed', u'type': u'string'
				},
				 u'@USERID': 
				 	{u'index': u'not_analyzed', u'type': u'string'
				 	}
			}
		}, 
	u'CARBONCOPY': 
		{u'properties': 
			{u'#text': 
				{u'index': u'not_analyzed', u'type': u'string'
				}, 
				 u'@USERID': 
				 {u'index': u'not_analyzed', u'type': u'string'
				 }
			}
		}
	}
}

'''

def main():
	strTree = {'people': {'properties': {'ASSIGNED': {'properties': {'#text': {'index': 'not_analyzed', 'type': 'string'}, '@USERID': {'index': 'not_analyzed', 'type': 'string'}}}, 'CARBONCOPY': {'properties': {'#text': {'index': 'not_analyzed', 'type': 'string'}, '@USERID': {'index': 'not_analyzed', 'type': 'string'}}}}}}
	abc = recusiveTree(strTree)
	print abc

if __name__ == "__main__":
	main()
