#!/usr/bin/python
'''
url shortener script
'''

import os,sys,cgi,cgitb,random,string
cgitb.enable()

SHORTURL = None
NAMECOUNT = 10
LEN = 5
POP = ['a','A','b','B','c','C','d','D','e','E','f','F','g','G','h','H','i','I','j','J','k','K','l','L','m','M','n','N','o','O','p','P','q','Q','r','R','s','S','t','T','u','U','v','V','w','W','x','X','y','Y','z','Z','0','1','2','3','4','5','6','7','8','9']
SCRIPT_NAME = os.environ['SCRIPT_NAME']
DIR = '/var/www/'
FORM_STR = '''<div style="text-align:center">
<b>Enter the long url and the short name you want.</b><br/><br/>
<form action='''+SCRIPT_NAME+''' method="POST" enctype="multipart/form-data">
Long URL: <input name="longurl" type="text"/><br/>
Short Name: <input name="shorturl" type="text"/><br/>
<input type="submit" value="submit"/>
</form>
</div>'''
ERROR = [False,'wut error?']

def clean_url(url):
   cleanurl = url.replace('/','').replace('{','').replace('(','').replace('[','').replace('|','')
   return cleanurl

def get_short_name():
   short = ''.join(str(x) for x in random.sample(POP,LEN))
      if NAMECOUNT == 0:
         return short
      elif os.path.exists(DIR+short):
         NAMECOUNT += 1
         short = get_short_name()

form = cgi.FieldStorage()
if form.has_key('shorturl'):
   if not form['shorturl'].value:
         shorturl = get_short_name()
   else:
      shorturl = clean_url(form['shorturl'].value)
      if os.path.exists(DIR+shorturl):
         shorturl = get_short_name()
         ERROR = [True,'Name Taken']
else:
   shorturl = get_short_name()

if form.has_key('longurl'):
   longurl = form['longurl'].value
   redirect = '<html><head><meta http-equiv="refresh" content="0;url='+longurl+'" /></head><body /></html>'
   open('/var/www/'+shorturl+'.html','w').write(redirect)
   SHORTURL = os.environ['SERVER_NAME']+'/'+shorturl

print('Content-Type: text/html\n\n\n')

print('<table><tr><td>')
print(FORM_STR)

if SHORTURL and not ERROR[0]:
   print('<p>Here is you shortened url:')
   print(SHORTURL)
   print('</p>')

if ERROR[0]:
   print('<div>ERROR: '+ERROR[1]+'</div>')

print('</td></tr></table>')
