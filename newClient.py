import pymysql.cursors

# Connect to the database with 'CX'
CX = pymysql.connect(host='gs-db-cluster1.cluster-clcutdgbykfx.us-east-1.rds.amazonaws.com',
                             user='derek',
                             password='bojangles1',
                             db='sde',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

"""
These are the methods we need to write. 
They all return different things to swap.py

"""
def getLoginInfo(_desiredOnyen):
    return None

def registerOnyen(_onyen, _password, _email):
    return None

def registerClass(_onyen, _course):
    return None

def getNextUser(_course):
    return None

def getRegisteredClasses(_onyen):
    return None

def markEnrollPass(_onyen, _course):
    return None

def deleteUser(_onyen, _password):
    return None

def getOnyenInfo(_onyen):
    return None
