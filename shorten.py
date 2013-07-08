#!/usr/bin/env python
'''
url shortener script
'''

import os,sys,cgi,cgitb,random,string,re
cgitb.enable()

gVars = {}
httpsre = re.compile('^https://')
httpre = re.compile('^http://')
SHORTURL = None
APIURL = None
gVars['NAMECOUNT'] = 10
LEN = 5
POP = ['a','A','b','B','c','C','d','D','e','E','f','F','g','G','h','H','i','I','j','J','k','K','l','L','m','M','n','N','o','O','p','P','q','Q','r','R','s','S','t','T','u','U','v','V','w','W','x','X','y','Y','z','Z','0','1','2','3','4','5','6','7','8','9']
DIR = '/home/hax/web/urlw.us/'
TMPL = 'main.tmpl'
ERROR = [False,'wut error?']

def uri_type(url):
   if httpsre.search(url):
      return url
   elif httpre.search(url):
      return url
   else:
      return 'http://'+url

def clean_url(url):
   cleanurl = url.replace('"','').replace('/','').replace('{','').replace('(','').replace('[','').replace('|','')
   return cleanurl

def get_short_name(gVars):
   short = ''.join(str(x) for x in random.sample(POP,LEN))
   if gVars['NAMECOUNT'] == 0:
      return short
   elif os.path.exists(DIR+short+'.html'):
      gVars['NAMECOUNT'] += 1
      short = get_short_name(gVars)
   return short

output = open(DIR+TMPL,'r').read()

output = output.replace('<!--ACTION-->',os.environ['SCRIPT_NAME'])

form = cgi.FieldStorage()
if form.has_key('shorturl'):
   if not form['shorturl'].value:
         shorturl = get_short_name(gVars)
   else:
      shorturl = clean_url(form['shorturl'].value)
      if os.path.exists(DIR+shorturl+'.html'):
         shorturl = get_short_name(gVars)
         ERROR = [True,'Name Taken']
else:
   shorturl = get_short_name(gVars)

if form.has_key('longurl'):
   longurl = uri_type(form['longurl'].value)
   redirect = '<html><head><meta http-equiv="refresh" content="0;url='+longurl+'" /></head><body /></html>'
   open(DIR+shorturl+'.html','w').write(redirect)
   SHORTURL = os.environ['HTTP_HOST']+'/'+shorturl

if form.has_key('url'):
   longurl = uri_type(form['url'].value)
   redirect = '<html><head><meta http-equiv="refresh" content="0;url='+longurl+'" /></head><body /></html>'
   open(DIR+shorturl+'.html','w').write(redirect)
   APIURL = os.environ['HTTP_HOST']+'/'+shorturl
   
if SHORTURL and not ERROR[0]:
   output = output.replace('<!--RESULT-->','<div id="shorturl"><a href="http://'+SHORTURL+'">http://'+SHORTURL+'</a></div>')

if APIURL and not ERROR[0]:
   output = APIURL

if ERROR[0]:
   output = output.replace('<!--ERROR-->','ERROR: '+ERROR[1])

print('Content-type: text/html\r\n\r\n')
print(output)
