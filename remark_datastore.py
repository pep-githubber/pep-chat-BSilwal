from datetime import datetime
from google.appengine.api import memcache
from google.appengine.ext import ndb


_LAST_GET_KEY_PREFIX = 'lastget'
_LAST_POST_KEY = 'lastpost'


import random

 # Convert a decimal to a hex as a string 
def decimaltoHex(decimalValue):
    hex = ""
    while decimalValue != 0:
        hexValue = decimalValue % 16 
        hex = toHexChar(hexValue) + hex
        decimalValue = decimalValue // 16
    
    if (len(hex) < 2):
        return "0" + str(hex)
    return hex
 
 # Convert an integer to a single hex digit in a character 
def toHexChar(hexValue):
    if 0 <= hexValue <= 9:
        return chr(hexValue + ord('0'))
    else:  # 10 <= hexValue <= 15
        return chr(hexValue - 10 + ord('A'))

 
A = random.randrange(0,255)
B = random.randrange(0,255)
C = random.randrange(0,255)

randhexnm = "#" + str(decimaltoHex(A)) + str(decimaltoHex(B)) + str(decimaltoHex(C))


class Remark(ndb.Model):

  user = ndb.StringProperty(required=True) # ID of the user who sent this.
  text = ndb.StringProperty(required=True) # The text the user entered.

  timestamp = ndb.DateTimeProperty(auto_now_add=True, required=True)


def ReadRemarks(user_id):
  start_time = memcache.get(_MakeLastGetKey(user_id))

  LogLastGet(user_id)

  remark_infos = []
  for remark in Remark.query(
      Remark.timestamp >= start_time).order(Remark.timestamp).fetch():
    user = remark.user
    text = remark.text
    color = randomhexnm  # TODO(pep-students) Make messages appear a random color.
    remark_infos.append((user, text, color))
  return remark_infos


def PostRemark(user, text):
  Remark(user=user, text=text).put()


def _MakeLastGetKey(user_id):
  return ';'.join([_LAST_GET_KEY_PREFIX, user_id])


def LogLastGet(user_id):
  memcache.set(_MakeLastGetKey(user_id), datetime.now())
