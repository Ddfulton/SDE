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
def registerCourse(_onyen, _password, _email, _course _referringOnyen=None):
    """
    Check if the user has already registered for this course. If so, 
    reject them. Get their score from this query to use later.
    If not, add them with the proper score.
    Finally, give more points to the referring onyen.
    """
    return None

def getNextUser(_course):
    """
    This method needs to be faster than greased lightning.
    Query all rows with the proper _course and success == 0
    then use the weighting process to decide who gets the attempt. 
    Returns the onyen and password.
    """
    return None

def getRegisteredClasses(_onyen):
    """
    Query for all the classes for which an onyen is currently registered.
    """
    return None

def markEnrollPass(_onyen, _course):
    """
    Change success from 0 to 1. E-mail them telling them they got in.
    """
    return None

def deleteUser(_onyen, _password):
    """
    Delete the bitch.
    """
    return None

def getOnyenInfo(_onyen):
    return None
