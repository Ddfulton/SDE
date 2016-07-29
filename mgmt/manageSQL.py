#!/bin/python

__author__ = 'Sam Andersen'
__version__ = '20160729'

import MySQLdb
import sys

### DEFINE CONNECTION PARAMETERS ###

SQL_HOST = "us-cdbr-iron-east-04.cleardb.net"
SQL_USER = "bbea41a94fb106"
SQL_SCHEMA = "heroku_5160d72946064c2"

class SQLManager:
	# SQLM CONFIGURATION #
	sqlHost = None
	sqlUser = None
	sqlPass = None
	sqlSchema = None

	# SQLM CONTEXTS #
	sql = None
	c = None

	def __init__(self):
		print("Launching SQLManager...")

		# Check the configuration outside of the class, if empty, prompt user for input #
		
		if SQL_HOST == None:
			sys.stdout.write("Enter a host: ")
			self.sqlHost = raw_input()

		else:
			self.sqlHost = SQL_HOST

		if SQL_USER == None:
			sys.stdout.write("Enter a username: ")
			self.sqlUser = raw_input()

		else:
			self.sqlUser = SQL_USER

		if SQL_SCHEMA == None:
			sys.stdout.write("Enter a schema (db): ")
			self.sqlSchema = raw_input()

		else:
			self.sqlSchema = SQL_SCHEMA

		# Password can't be stored in this file; always prompt user #

		sys.stdout.write("Password: ")
		self.sqlPass = raw_input()

	def openConnection(self):
		print("DEBUG: Opening connection")

		# Make sure the connection is open before attempting any operations #

		try:
			self.sql = MySQLdb.connect(host = self.sqlHost, user = self.sqlUser, passwd = self.sqlPass, db = self.sqlSchema)

		except MySQLdb.Error, e:
			print "WARN: Error %d: %s" % (e.args[0], e.args[1])
			sys.exit(1)

		print("INFO: Connection successful\nINFO: Creating cursor context")

		self.c = self.sql.cursor()

	def showOnyenClassRequests(self, desiredOnyen):
		print("INFO: Requesting classes for onyen %s" % desiredOnyen)

		baseQuery = """SELECT 
				DB.Onyen,
				RQ.ClassId,
				RQ.`Status`
			FROM `onyendb` AS DB 
			INNER JOIN `requestedclasses` AS RQ ON DB.InternalId = RQ.ParentId
			WHERE
				`Onyen` LIKE %s"""

		self.c.execute(baseQuery, (desiredOnyen,))

		rows = self.c.fetchall()
		for row in rows:
			print row

	def addOnyen(self, newOnyen, onyenPassword):
		print("INFO: Adding new onyen")

		baseStatement = """REPLACE INTO `onyendb` (`Onyen`, `Password`)
			VALUES (%s, %s)"""

		try:
			self.c.execute(baseStatement, (newOnyen, onyenPassword))
			self.sql.commit()
			print("INFO: Request successful")

		except MySQLdb.Error, e:
			if sql:
				sql.rollback()

			print "WARN: Error %d: %s" % (e.args[0], e.args[1])
			sys.exit(1)

	def addClassRequest(self, onyen, classId):
		print("INFO: Adding request for user %s to class %s" % (onyen, classId))

		# Acquire the Id for this Onyen, or let user know it doesn't exist #

		baseQuery = """SELECT
				`InternalId`
			FROM
				`onyendb`
			WHERE
				`Onyen` LIKE %s"""

		try:
			self.c.execute(baseQuery, (onyen,))

		except MySQLdb.Error, e:
			print "WARN: Error %d: %s" % (e.args[0], e.args[1])
			sys.exit(1)

		internalId = self.c.fetchone()

		# Begin insertion of record into requestedclasses #

		baseStatement = """REPLACE INTO `requestedclasses` (`ParentId`, `ClassId`)
			VALUES (%s, %s)"""

		try:
			self.c.execute(baseStatement, (internalId, classId))
			self.sql.commit()
			print("INFO: Request successful")

		except MySQLdb.Error, e:
			if sql:
				sql.rollback()

			print "WARN: Error %d: %s" % (e.args[0],e.args[1])
			sys.exit(1)

if __name__ == '__main__':

	SQLM = SQLManager()
	SQLM.openConnection()

	# Sample of query execution from SQLM

	SQLM.c.execute("SELECT COUNT(*) FROM `requestedclasses`")

	# Retrieve the result; know there is only one

	x = SQLM.c.fetchone()
	print("Total records: %d" % x)

	SQLM.showOnyenClassRequests("swa8")

	SQLM.addOnyen("Sam", "OtherPassword")

	SQLM.addClassRequest("swa8", "CHIN305")


	SQLM.sql.close()
	


