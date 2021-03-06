#!/usr/bin/env python
#
# Hacker News Droid API: returns best articles in JSON or XML using HTML Parser
# Gleb Popov. September 2011
#

import os
import re
import logging
from UserString import MutableString
from django.utils import simplejson
from google.appengine.ext import webapp 
from google.appengine.ext import db
from google.appengine.ext.webapp import util
import Formatter
import AppConfig
import GAHelper
from xml.sax.saxutils import escape
import APIContent
import GAHelper
from BeautifulSoup import BeautifulSoup

class HackerNewsBestHandler(webapp.RequestHandler):
	
	#controller main entry		
	def get(self,format='json',page=''):
		#set content-type
		self.response.headers['Content-Type'] = Formatter.contentType(format)
		
		referer = ''
		if ('HTTP_REFERER' in os.environ):
			referer = os.environ['HTTP_REFERER']
		
		returnData = APIContent.getHackerNewsBestContent(page,format,self.request.url, referer, self.request.remote_addr)
		if (not returnData or returnData == None or returnData == '' or returnData == 'None'):
			#call the service again this time without the pageID
			returnData = APIContent.getHackerNewsBestContent('',format,self.request.url, referer, self.request.remote_addr)
					
		#track this request
		GAHelper.trackGARequests('/best', self.request.remote_addr, referer)
		
		#output to the browser
		self.response.out.write(Formatter.dataWrapper(format, returnData))