import urllib, urllib2, cookielib, hashlib
from BeautifulSoup import BeautifulSoup
import re
import time

#modify these link
username = 'username'
password = "password"
search_post_link = "https://vozforums.com/search.php?searchid=0b14297a5dd61664f5a9f17c9d6d9149" # các thím click vào user của các thím -> all post -> lấy link
#end of modify

md5 = hashlib.md5(password).hexdigest()
post_link = []

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


cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
login_data = "do=login&s=&securitytoken=guest&vb_login_md5password=" + md5 + "&vb_login_md5password_utf=" + md5 + "&vb_login_password=&vb_login_username=" + username
opener.open('https://vozforums.com/login.php', login_data)
for i in range(0, 20):
 resp = opener.open(search_post_link + "&pp=20&page=" + str(i))
 find_post(resp)

for link in post_link :
 s = link.find("p=")
 e = link.find("#")
 p = link[s+2:e]
 resp = opener.open('https://vozforums.com/editpost.php?do=editpost&p=' + p)
 securitytoken = find_security_token(resp)
 delete_data = "deletepost=delete&do=deletepost&p=" + p + "&reason=Tool%20Delete%20All%20Post&s=&securitytoken=" + securitytoken + "&url=https://vozforums.com/showthread.php?p=" + p
 try :
  opener.open("https://vozforums.com/editpost.php?do=deletepost&p=" + p, delete_data)
 except :
  print "Cannot delete " + p
  time.sleep(1)
  pass #just 503, lol voz database is shit
 else :
  print "Delete " + p

print "Done"
