import pymysql.cursors
import random


chickfila = "Tq8eGl70L0MFTSB0ywWFtits"



def DATABASE():
    connection = pymysql.connect(host='sdecheap.clcutdgbykfx.us-east-1.rds.amazonaws.com',
                                 port=3306,
                                 user='swapdropenroll', # TODO: Make this better
                                 password='d3!!29d@dapDeA@45gii24!*d', # TODO: Make this better
                                 db='SDECheap',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    return connection

def boostScore(_onyen):
    connection = DATABASE()
    cursor = connection.cursor()
    sql = "update SDECheap.USERS set score = score + 1 where onyen = \"%s\";" % (_onyen)
    cursor.execute(sql)
    connection.commit()
    connection.close()
    return None


def registerCourse(_onyen, _password, _course, _score, _success, _referringOnyen=None):
    """
    Check if the user has already registered for this course. If so, 
    reject them. Get their score from this query to use later.
    If not, check their current score and add them with a new score.
    Finally, give more points to the referring onyen.
    """
    # TODO: See if they have a higher score than 0
    # Connect to the database with 'connection'
    # TODO: Encrypt onyen and password
    connection = DATABASE()
    cursor = connection.cursor()

    # Encrypts the onyen. It looks like this b'\x23 etc'
    #TODO _score = getScore(_onyen)
    # _password = bojangles.encrypt_password(_password, chickfila)

    cursor.execute("select * from SDECheap.USERS where onyen = \"%s\" and course = \"%s\"" % (_onyen, _course))


    if len(cursor.fetchall()) != 0:
        print("INFO: %s is already registered for %s. Not adding shit." % (_onyen, _course))
        return False
    
    else:
        cursor = connection.cursor()
        sql = "insert into SDECheap.USERS (onyen, password, course, score, success, mobile) VALUES (\"%s\", \"%s\", \"%s\", %s, %s, \"NO MOBILE\");" % (_onyen, _password, _course, _score, _success)
        cursor.execute(sql)
        connection.commit()

        if _referringOnyen == None: 
            pass  
        else: 
            boostScore(_referringOnyen)

    connection.commit()
    connection.close()

    return True

# registerCourse("Bojangles", "bojangles6'", "AAAD 101-002", 1, 0)


def getNextUser(_course):
    """
    This method needs to be faster than greased lightning.
    Query all rows with the proper course and success == 0
    then use the weighting process to decide who gets the attempt. 
    Returns the onyen and password.
    """
    connection = DATABASE()

    cursor = connection.cursor()

    sql = "select * from SDECheap.USERS where course = \"%s\" and success = 0" % (_course)

    cursor.execute(sql)
    connection.commit()

    candidates = cursor.fetchall()



    hat = []

    if len(candidates) == 0:
        print("INFO: Zero candidates currently want %s" % _course)
        return None
    
    else:
        for candidate in candidates:

            for i in range(0, candidate["score"]):
                hat.append(candidate["onyen"])


        winner = random.choice(hat)
        print("INFO: Selecting %s for attempt of enrollment in %s!" % (winner, _course))

    for candidate in candidates:
        if candidate["onyen"] == winner:
            nextUser = candidate
            break
        else:
            continue

    connection.close()

    print(nextUser)

    return nextUser
# getNextUser("AAAD 101-001")


def markSuccess(_onyen, _course):
    """
    Change success from 0 to 1. E-mail them telling them they got in.
    # TODO: RESET REFERRAL COUNT
    """
    print("INFO: Marking enrollment success for onyen %s and course %s" % (_onyen, _course))
    
    connection = DATABASE()

    cursor = connection.cursor()

    sql = "update SDECheap.USERS set success = 1 where onyen = \"%s\" and course = \"%s\"" % (_onyen, _course)

    cursor.execute(sql)
    connection.commit()
    connection.close()

    return None


def removeClass(_onyen, _password, _course):
    """
    Removes the row with the provided _onyen 
    and _course.
    #TODO: If they're not tracking the course, do nothing
    """
    print("INFO: Marking success on %s for onyen %s" % (_course, _onyen))

    connection = DATABASE()

    cursor = connection.cursor()

    sql = "update SDECheap.USERS set success = 1 where onyen = \"%s\" and password = \"%s\"and course = \"%s\";" % (_onyen, _password, _course)

    cursor.execute(sql)
    connection.commit()
    connection.close()

    return None


def unregister(_onyen, _password):
    """
    Completely removes the given
    onyen from Swap Drop Enroll.
    # TODO: If they aren't in the database, do nothing
    """
    print("INFO: Removing %s from the database" % _onyen)

    connection = DATABASE()

    cursor = connection.cursor()

    sql = "update SDECheap.USERS set success = 1 where onyen = \"%s\" and pasword = \"%s\"" % (_onyen, _password)

    cursor.execute(sql)
    connection.commit()
    connection.close()

    return None




