from dataSourceClasses import Mysql, csvFile, twipy
from operations import joinOperation, transform
import MySQLdb as mysql
from sqlalchemy import create_engine

def test():
   
    sqlobj = Mysql(database='test')
    #print sqlobj.getColumnNames('CUSTOMERS')
    df0 = sqlobj.select('CUSTOMERS',['CustomerID','CompanyName'])
    #print df0

    print "################################"
    csvfile = csvFile('orders.csv')
    csvfile._open()
    df1 = csvfile.getDataFrame()
    csvfile._close()
    #print df1

    print joinOperation([df0,df1],['CustomerID'],'outer').keys()
    '''
	mysqlobj = Mysql(database='test')
	df2 = mysqlobj.getAll('CUSTOMERS')
	#print df2
	twitter = twipy()
	res = twitter.topicSearch('IPHONE')
	res = transform(res,'wordcount')
	print res
	'''


test()

def filldb():
	cnx = mysql.connect(host='localhost', user='root', passwd='',
                                          db='test')
	engine =   create_engine("mysql+mysqldb://root:@localhost:3306/test")
	csvfile = csvFile('customers.csv')
	csvfile._open()
	df1 = csvfile.getDataFrame()
	csvfile._close()
	print df1
	df1.to_sql(con=engine, name='CUSTOMERS', if_exists='replace', index=False)





