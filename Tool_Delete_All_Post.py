import urllib, urllib2, cookielib, hashlib
from BeautifulSoup import BeautifulSoup
import re
import time
post_link = []

#modify
username = 'username'
password = "password	"
search_post_link = "https://vozforums.com/search.php?searchid=bab85b4e65b55ed19048bdcf1c4814ae" 




#Other function
def find_security_token(resp):
 s = str(resp.read())
 p = s.find('SECURITYTOKEN')
 security_token = s[p+17:p+68]
 return security_token

def find_post(resp):
 global post_link
 soup = BeautifulSoup(resp.read())
 for link in soup.findAll('a', attrs={'href': re.compile("#post")}):
  post_link.append(link.get('href'))

def delete_post(opener, post_list):
 for link in post_link :
  #get p param
  s = link.find("p=")
  e = link.find("#")
  p = link[s+2:e]
  #delete post
  resp = opener.open('https://vozforums.com/editpost.php?do=editpost&p=' + p)
  securitytoken = find_security_token(resp)
  #delete param
  delete_data = {
   "deletepost" : "delete",
   "do" : "deletepost",
   "p" : p,
   "reason" : "Tool Delete All Post",
   "s" : "",
   "securitytoken" : securitytoken,
   "url" : ("https://vozforums.com/showthread.php?p=" + p)
   }
 
  try :
   opener.open("https://vozforums.com/editpost.php", urllib.urlencode(delete_data))
  except :
   print "Cannot delete " + p
   time.sleep(1)
   pass #just 503, lol voz database is shit
  else :
   print "Delete " + p
 
 print "Done"


#MAIN
#cookie for login
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
#login parameter
login_data = {
 "do" : "login",
 "s" : "",
 "securitytoken" : "guest",
 "vb_login_password" : password,
 "vb_login_username" : username
}
opener.open('https://vozforums.com/login.php', urllib.urlencode(login_data))

#Get all post link
for i in range(0, 20):
 resp = opener.open(search_post_link + "&pp=20&page=" + str(i))
 find_post(resp)

#remove duplicate link before delete each of them
post_link = list(set(post_link))

delete_post(opener, post_link)
