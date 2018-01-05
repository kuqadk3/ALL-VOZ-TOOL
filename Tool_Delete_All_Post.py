import urllib, urllib2, cookielib, hashlib
from BeautifulSoup import BeautifulSoup
import re
import time
import requests

#modify
username = "username"
password = "password"


#Other function
def find_security_token(resp):
 s = str(resp.read())
 p = s.find('SECURITYTOKEN')
 security_token = s[p+17:p+68]
 return security_token

def find_post(resp):
 post_link = []
 soup = BeautifulSoup(resp.read())
 for link in soup.findAll('a', attrs={'href': re.compile("#post")}):
  post_link.append(link.get('href'))
 return post_link

def get_user_id(opener):
 resp = opener.open('https://vozforums.com/')
 soup = BeautifulSoup(resp.read())
 for link in soup.findAll('a', attrs={'href': re.compile("member.php")}):
  return link.get('href')[13:]

def delete_post(opener):
 search_post_link = opener.open('https://vozforums.com/search.php?do=finduser&u=' + get_user_id(opener)).geturl() #get redirected all post link
 post_link = []
 #Get all post link
 for i in range(0, 20):
  resp = opener.open(search_post_link + "&pp=20&page=" + str(i))
  post_link.extend(find_post(resp))

 #remove duplicate in post_link
 post_link = list(set(post_link))

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
   "reason" : "Tool Delete All Post at https://github.com/kuqadk3/ALL-VOZ-TOOL/blob/master/Tool_Delete_All_Post.py",
   "s" : "",
   "securitytoken" : securitytoken,
   "url" : ("https://vozforums.com/showthread.php?p=" + p)
   }
  edit_thread_data = {
   "do" : "updatepost",
   "emailupdate" : "9999",
   "message" : "Tool Delete All Post at [url]https://github.com/kuqadk3/ALL-VOZ-TOOL/blob/master/Tool_Delete_All_Post.py[/url]",
   "p" : p, #get only ID
   "parseurl" : "1",
   "reason" : "",
   "s" : "",
   "sbutton" : "Save Changes",
   "securitytoken" : securitytoken,
   "signature" : "1",
   "title" : "Deleted",
   "wysiwyg" : "0"
 }
  try :
   opener.open("https://vozforums.com/editpost.php", urllib.urlencode(edit_thread_data)) #edit both thread and post
   opener.open("https://vozforums.com/editpost.php", urllib.urlencode(delete_data)) #delete if it is not thread
  except :
   print "Cannot delete " + p
   time.sleep(1)
   pass #just 503, lol voz database is shit
  else :
   print "Delete post " + p
 
 print "Done"

def login(username, password):
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
 return opener



#MAIN
opener = login(username, password) #cookie for login
delete_post(opener)

