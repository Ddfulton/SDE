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
 * Project: SOAP Python Connection Sample
 * Author: Sam Andersen
 * Version: 20160812
 * TODO: Continue adding functionality
 *
 */
"""

__author__ = 'Sam Andersen'
__version = '20160813'

import zeep
from zeep.transports import Transport

SDE_TOKEN = '3e80d405613958ae8db48c3f4f21b1c0606657dc9a5af1b0b7e7ba994d8af682'

def getLoginInfo(_desiredOnyen):
    print("DEBUG: Launching getLoginInfo for %s" % _desiredOnyen)

    transport = Transport(verify = True)
    wsdl = 'SDE.wsdl'
    client = zeep.Client(wsdl = wsdl, transport = transport)

    SDEKey_type = client.get_type('ns0:SDEKey')

    return client.service.getLoginInfo(session = SDEKey_type(sessionKey = SDE_TOKEN), desiredOnyen = _desiredOnyen)

def registerOnyen(_onyen, _password, _email):
    print("DEBUG: Launching registerOnyen for %s" % _onyen)

    transport = Transport(verify = True)
    wsdl = 'SDE.wsdl'
    client = zeep.Client(wsdl = wsdl, transport = transport)

    SDEKey_type = client.get_type('ns0:SDEKey')

    return client.service.addOnyen(session = SDEKey_type(sessionKey = SDE_TOKEN), desiredOnyen = _onyen,
        desiredPassword = _password, desiredEmail = _email)

def registerClass(_onyen, _course):
    print("DEBUG: Launching registration for %s" % _onyen)

    transport = Transport(verify = True)
    wsdl = 'SDE.wsdl'
    client = zeep.Client(wsdl = wsdl, transport = transport)

    SDEKey_type = client.get_type('ns0:SDEKey')

    return client.service.registerClass(session = SDEKey_type(sessionKey = SDE_TOKEN), desiredOnyen = _onyen,
        desiredClass = _course)

def getNextUser(_course):
    print("DEBUG: Getting next user for course %s" % _course)

    transport = Transport(verify = True)
    wsdl = 'SDE.wsdl'
    client = zeep.Client(wsdl = wsdl, transport = transport)

    SDEKey_type = client.get_type('ns0:SDEKey')

    return client.service.getNextUser(session = SDEKey_type(sessionKey = SDE_TOKEN), 
        desiredClass = _course)

def getRegisteredClasses(_onyen):
    print("DEBUG: Getting registered courses for %s" % _onyen)

    transport = Transport(verify = True)
    wsdl = 'SDE.wsdl'
    client = zeep.Client(wsdl = wsdl, transport = transport)

    SDEKey_type = client.get_type('ns0:SDEKey')

    return client.service.getRegisteredClasses(session = SDEKey_type(sessionKey = SDE_TOKEN), desiredOnyen = _onyen)

def markEnrollPass(_onyen, _course):
    print("DEBUG: Marking enrollment pass for %s in class %s" % _onyen, _course)

    transport = Transport(verify = True)
    wsdl = 'SDE.wsdl'
    client = zeep.Client(wsdl = wsdl, transport = transport)

    SDEKey_type = client.get_type('ns0:SDEKey')

    return client.service.markEnrollPass(session = SDEKey_type(sessionKey = SDE_TOKEN), desiredOnyen = _onyen,
        desiredClass = _course)