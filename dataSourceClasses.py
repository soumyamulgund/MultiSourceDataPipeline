import MySQLdb as mysql
import csv
from pandas import DataFrame
import pandas as pd
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import json



#Class to Interact with the MySQL DB 
class Mysql(object):
    __instance = None
    __host = None
    __user = None
    __password = None
    __database = None
    __session = None
    __connection = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Mysql, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self, host='localhost', user='root', password='', database=''):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database

    def _open(self):
        try:
            cnx = mysql.connect(host=self.__host, user=self.__user, passwd=self.__password,
                                          db=self.__database)
            self.__connection = cnx
            self.__session = cnx.cursor()
            print "successfully connected  to DB : "+self.__database+"! "
            return True
        except Exception:
            print 'Something is wrong with your user name or password'
            return False
            

    def _close(self):
        self.__session.close()
        self.__connection.close()



    def insert(self, table, *args, **kwargs):
        values = None
        query = "INSERT INTO %s " % table
        if kwargs:
            keys = kwargs.keys()
            values = kwargs.values()
            query += "(" + ",".join(["`%s`"]*len(keys)) % tuple(keys) + ") VALUES(" + ",".join(["%s"]*len(values)) + ")"
        elif args:
            values = args
            query += " VALUES(" + ",".join(["%s"]*len(values)) + ")"
        self._open()
        self.__session.execute(query, values)
        self.__connection.commit()
        self._close()
        return self.__session.lastrowid

    def select(self, table, columns,where=None):
        result = None
        query = "SELECT "
        keys = columns
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += "`"+key+"`"
            if i < l:
                query += ","
        query += " FROM %s" % table
        if where:
            query += " WHERE %" % where
        print query
        self._open()
        df = pd.read_sql(query, con=self.__connection)
        self._close()
        df = df.applymap(str)
        return df

    def getAll(self,table):
        self._open()
        df = pd.read_sql("SELECT * FROM "+table+";", con=self.__connection)
        self._close()
        return df

    def getColumnNames(self,table):
        self._open()
        self.__session.execute("desc "+table)
        col = [column[0] for column in self.__session.fetchall()]
        self._close()
        
        return col

    def getTables(self):
        self._open()
        self.__session.execute("show tables")
        col =  self.__session.fetchall()
        self._close()
        li=[]
        for row in col:
            li.append(row[0])
        return li


'''
#Assuming that our table have the fields id and name in this order.
#we can use this way but the parameter should have the same order that table
#connection.insert('table_name',parameters to insert)
connection.insert('test',1, 'Alejandro Mora')
#in this case the order isn't matter
#connection.insert('table_name', field=Value to insert)
connection.insert('test',name='Alejandro Mora', id=1)
#connection.select('Table', where="conditional(optional)", field to returned)
connection.select('test', where="name = 'Alejandro Mora' ")
connection.select('test', None,['id','name'])
#connection.update('Table', id, field=Value to update)
connection.update('test', 1, name='Alejandro')
#connection.delete('Table', id)
connection.delete('test', 1)
#connection.call_store_procedure(prodecure name, Values)
connection.call_store_procedure('search_users_by_name', 'Alejandro')
'''



#Class to Interact with the CSV FILE 
class csvFile(object):
    def __init__(self, file_name):
        self._filename = file_name
        self_file = None
        self._writer = None
        self._reader = None
        self._df = None 
        self._header = None

    def _open(self,writer=0,header=None):
        if writer == 1:
            self._file = open(self._filename,'wb')
            self._writer = csv._writer(self._file)
            if header:
                _writer.writerow(header)
        else:
            self._file = open(self._filename)
            self._reader =  csv.reader(self._file)
            self._header = self._reader.next()
            print 'opened file successfully'
            

    def _close(self):
        self._file.close()

    def readLine():
        try:
            return _reader.next()
        except:
            return 'EOF' 
    
    def setWriter(self,header):
        if self._writer == None:
            print "this is not a reader object , create a writer object!"
            return 0
        self._writer.writerow(header)

    def wrtieLine(self,row):
        self._writer.writerow(row)

    def writeDf(self,df):
        df.to_csv(self._filename, sep='\t', encoding='utf-8')

    def getHeader(self):
        return self._header

    def getDataFrame(self,fields):
        self._df = pd.read_csv(self._filename)
        new = self._df[fields]
        new = new.applymap(str)
        return new



#Twitter API consumer class

class twipy:
    _api = None
    _auth = None
    def __init__(self,Oauth_token=None,Oauth_token_sec=None,c_key=None,c_sec=None):
        print "calling constructor"
        if c_key == None:
            c_key="WLNqYRHIelUzBeRffk93NznLt"
            c_sec="c0MLYczAAA1qtyvSdbJXIhp52LqypwLzkMmdVk44810b0nc578"
            Oauth_token="2507891046-bTEMCZJPfAO6qITqu3BqQRIo8lth6U89XywtKzS"
            Oauth_token_sec="k5IyHUq4c5AErNcyBvuhr0rskcH6peIWmrwnQwgM0lsYt"
            self._auth = OAuth(Oauth_token,Oauth_token_sec,c_key,c_sec)

        else:
            self._auth = OAuth
        self._api = Twitter(auth=self._auth)
        

    def topicSearch(self,q,max_results=20):
        print "Searching for {}".format(q)
        c_key="WLNqYRHIelUzBeRffk93NznLt"
        c_sec="c0MLYczAAA1qtyvSdbJXIhp52LqypwLzkMmdVk44810b0nc578"
        Oauth_token="2507891046-bTEMCZJPfAO6qITqu3BqQRIo8lth6U89XywtKzS"
        Oauth_token_sec="k5IyHUq4c5AErNcyBvuhr0rskcH6peIWmrwnQwgM0lsYt"
        self._auth = OAuth(Oauth_token,Oauth_token_sec,c_key,c_sec)
        self._api = Twitter(auth=self._auth)
        search_results = self._api.search.tweets(q=q,count=20, lang='en')
        statuses=search_results['statuses']
        df = DataFrame(columns = ['user_id','userName','userScreenName','tweet'])
        res = tweet
        for tweet in statuses:
            try:
                df.loc[len(df.index)]=[tweet['user']['id'],tweet['user']['name'],tweet['user']['screen_name'],tweet['text']]
            except:
                pass
        print res
        df.applymap(str)
        return df






