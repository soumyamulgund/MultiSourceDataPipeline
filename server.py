from bottle import request, response, template
from bottle import post, get, put, delete, route
import bottle
from dataSourceClasses import Mysql, csvFile, twipy
from operations import joinOperation, transform
import MySQLdb as mysql
from sqlalchemy import create_engine
import json
import glob


sqlobj = Mysql(database='test')
resDF=None


@route('/')
def index():
  return template('app.html')


@get('/get_db_names')
def getDbNames():
	tables = sqlobj.getTables()
	print tables
	dbs={}
	for table in tables:
			dbs[table] = sqlobj.getColumnNames(table)
	#response.headers['Content-Type'] = 'application/json'
	return json.dumps(dbs)



@get('/csv_files')
def getcsvnames():
	files = glob.glob("csv/"+"*.csv")
	csvs = {}
	for fl in files:
		csvfile = csvFile(fl)
		csvfile._open()
		csvs[fl.split('/')[1]] = csvfile.getHeader()
		csvfile._close()
	return json.dumps(csvs)



@post('/join')
def join_operation():
	data = dict(request.json)
	print data
	join_fields= [ str(f).strip() for f in data['fields'].split(',')]
	dfs=[]
	for key,fields in data['dfs'].iteritems():
		if('.csv' in key):
			fl =[ str(f).strip() for f in fields]
			#print fl
			csvfile = csvFile('csv/'+key)
			csvfile._open()
			df = csvfile.getDataFrame(fl)
			print df.head(5)
			dfs.append(df)
			csvfile._close()
		else:
			fl =[ str(f).strip() for f in fields]
			#print fl
			df = sqlobj.select(key,fl)
			print df.head(5)
			dfs.append(df)
		print '###########'
	global resDF
	if len(dfs)>1:
		resDF = joinOperation(dfs,join_fields,'outer')
	else :
		resDF = dfs[0]
	#print resDF.head(5)
	table_1 = resDF.head(20).to_html(classes='table',index=False,escape=False)
	#print table_1
	return table_1


@post('/transform')
def transform_fun():
	data = dict(request.json)
	print data
	_type = str(data['type'])
	_params =  [ str(p) for p in data['params'].split(',')]
	global resDF
	trdf = transform(resDF,_type,_params)
	table_1 = trdf.to_html(classes='table',index=False,escape=False)
	return table_1

@post('/twitter')
def getTweets():
	data = dict(request.json)
	topic = data['topic']
	twitter = twipy()
	global resDF
	resDF = twitter.topicSearch(topic)
	#print resDF
	table_1 = resDF.to_html(classes='table',index=False,escape=False)
	#print table_1
	return table_1










if __name__ == '__main__':
    bottle.run(host = '127.0.0.1', port = 8000)
