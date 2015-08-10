import cx_Oracle
import arrow
import datetime
import os
import re
import pandas as pd
import json

def recusiveTree(tree):

	if('#text' not in tree and '@USERID' not in tree):
		for x in tree:
			recusiveTree(tree[x])
	else:
		print tree


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
	strTree = {'properties': {'ASSIGNED': {'properties': {'#text': {'index': 'not_analyzed', 'type': 'string'}, '@USERID': {'index': 'not_analyzed', 'type': 'string'}}}, 'CARBONCOPY': {'properties': {'#text': {'index': 'not_analyzed', 'type': 'string'}, '@USERID': {'index': 'not_analyzed', 'type': 'string'}}}}}
	recusiveTree(strTree)


if __name__ == "__main__":
	main()
