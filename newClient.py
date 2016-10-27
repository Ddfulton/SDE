import pymysql.cursors
import random

def DATABASE():
    connection = pymysql.connect(host='gs-db-cluster1.cluster-clcutdgbykfx.us-east-1.rds.amazonaws.com',
                                 user='derek',
                                 password='bojangles1',
                                 db='sde',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    return connection



def registerCourse(_onyen, _password, _course, _score, _success, _mobile, _referringOnyen=None):
    """
    Check if the user has already registered for this course. If so, 
    reject them. Get their score from this query to use later.
    If not, check their current score and add them with a new score.
    Finally, give more points to the referring onyen.
    """

    # Connect to the database with 'connection'
    connection = DATABASE()
    cursor = connection.cursor()

    cursor.execute("select * from sde.USERS where onyen = \"%s\" and course = \"%s\"" % (_onyen, _course))


    if len(cursor.fetchall()) != 0:
        print("INFO: %s is already registered for %s. Not adding shit." % (_onyen, _course))

        return False
    
    else:
        cursor = connection.cursor()
        sql = "insert into sde.USERS (onyen, password, course, score, success, mobile) VALUES (\"%s\", \"%s\", \"%s\", %s, %s, \"%s\");" % (_onyen, _password, _course, _score, _success, _mobile)
        cursor.execute(sql)
        connection.commit()

    connection.close()

    return True


def getNextUser(_course):
    """
    This method needs to be faster than greased lightning.
    Query all rows with the proper course and success == 0
    then use the weighting process to decide who gets the attempt. 
    Returns the onyen and password.
    """
    connection = DATABASE()

    cursor = connection.cursor()

    sql = "select * from sde.USERS where course = \"%s\" and success = \"0\"" % (_course)

    cursor.execute(sql)
    connection.commit()

    candidates = cursor.fetchall()

    hat = []

    if len(candidates) == 0:
        print("INFO: Zero candidates currently want %s" % _course)
        return None
    else:
        for candidate in candidates:
            score = candidate["score"]
            print("Adding %s %s times to the random hat" % (candidate["onyen"], candidate["score"]))    
            for i in range(0, score):
                hat.append(candidate["onyen"])

        print("INFO: Hat is %s" % hat)

        winner = random.choice(hat)
        print("INFO: Selecting %s for attempt of enrollment in %s!" % (winner, _course))

    for candidate in candidates:
        if candidate["onyen"] == winner:
            credentials = candidate
            break
        else:
            continue

    connection.close()

    print(credentials)
    return credentials

def markSuccess(_onyen, _course):
    """
    Change success from 0 to 1. E-mail them telling them they got in.
    # TODO: RESET REFERRAL COUNT
    """
    print("INFO: Marking enrollment success for onyen %s and course %s" % (_onyen, _course))
    
    connection = DATABASE()

    cursor = connection.cursor()

    sql = "update sde.USERS set success = 1 where onyen = \"%s\" and course = \"%s\"" % (_onyen, _course)

    cursor.execute(sql)
    connection.commit()
    connection.close()

    return None


