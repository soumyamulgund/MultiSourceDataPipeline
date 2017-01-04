import pandas as pd
from pandas import DataFrame
import pandas as pd



def joinOperation(dataFrames, keys, joinType):
	print keys
	joinedDF = pd.merge(dataFrames[0], dataFrames[1], on=keys, how=joinType)
	for i in range(2,len(dataFrames)):
		joinedDF = pd.merge(joinedDF, dataFrames[i], on=keys, how=joinType)
	return joinedDF



def transform(df, _type , args):
	print args
	if _type == 'sort':
		dfres = df.sort(columns=args)
	if _type == 'group':
		dfres = df.groupby(args).count()
	if _type == 'wordcount':
		df['uniqueWords'] = [ len(set(words.split())) for words in df['tweet'] ]
		dfres = df
	return dfres



