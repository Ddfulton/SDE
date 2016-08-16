#!/usr/bin/python

"""
/*  (    (           
 *  )\ ) )\ )        
 *  (()/((()/(   (    
 *  /(_))/(_))  )\   
 *  (_)) (_))_  ((_)  
 *  / __| |   \ | __| 
 *  \__ \ | |) || _|  
 *  |___/ |___/ |___| 
 *
 * Project: SOAP Python Connection
 * Author: Sam Andersen
 * Version: 20160808
 * TODO: Continue adding functionality
 *
 */
"""

__author__ = 'Sam Andersen'
__version = '20160808'

import zeep

if __name__ == '__main__':
	wsdl = 'SDE.wsdl'
	client = zeep.Client(wsdl = wsdl)

	SDEKey_type = client.get_type('ns0:SDEKey')
	SDEKey = SDEKey_type(sessionKey = '123')

	#print(client.service.getLoginInfo(session = SDEKey, desiredOnyen = 'swa8'))

	for ClassId in client.service.getRegisteredClasses(session = SDEKey, desiredOnyen = 'swa8'):
		print("Found class: %s" % ClassId)

	print(client.service.addOnyen(session = SDEKey_type(sessionKey = '123'), desiredOnyen = 'test', desiredPassword = 'password'))