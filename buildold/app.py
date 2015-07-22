import mimetypes
import webapp2
import os

# ---

mimetypes.add_type('image/svg+xml', '.svg')
mimetypes.add_type('application/font-woff', '.woff')

# ---

true = True
false = False
config = {"locals":{"url":"http://localhost:8080","name":"Evellia","owner":"Evellia","description":"Ramblings of an immor(t)al demigod"},"plugins":["./plugins/paginator.coffee","wintersmith-appengine"],"require":{"moment":"moment","_":"underscore","typogr":"typogr"},"jade":{"pretty":True},"markdown":{"smartLists":True,"smartypants":True},"paginator":{"perPage":3,"template":"index.jade","articles":"articles","first":"index.html","filename":"page/%d/index.html"},"appengine":{"application":"evelliacom","version":1},"contents":"./contents","ignore":[],"templates":"./templates","views":None,"output":"./build","baseUrl":"/","hostname":None,"port":8080,"_fileLimit":40,"_restartOnConfChange":True,"__filename":"/Users/sylvain/Sources/EvelliaCom/config.json","_cliopts":{}}

# ---

if 'appengine' not in config:
	config['appengine'] = {}
	
# ---

class RequestHandler(webapp2.RequestHandler):
	root = os.path.dirname(__file__)
	
	# ---
	
	def get(self):
		path_parts = [self.root] + self.request.path.split('/')
		final_path = os.path.join(*path_parts)
		
		# ---
		
		if not os.path.exists(final_path):
			if 'notFoundPage' in config['appengine'] and config['appengine']['notFoundPage']:
				if 'notFoundPageIsRedirect' in config['appengine'] and config['appengine']['notFoundPageIsRedirect']:
					self.redirect(config['appengine']['notFoundPage'])
					
					# ---
					
					return
					
				# ---
				
				path_parts = [self.root] + config['appengine']['notFoundPage'].split('/')
				final_path = os.path.join(*path_parts)
				
				# ---
				
				if not os.path.exists(final_path):
					return
					
				# ---
				
				self.response.set_status(404)
				
			else:
				return
				
		# ---
		
		if os.path.isdir(final_path):
			path_parts = path_parts + ['index.html']
			final_path = os.path.join(*path_parts)
			
		# ---
		
		self.response.headers['Content-Type'] = mimetypes.guess_type(os.path.basename(final_path))[0] or 'application/octet-stream'
		self.response.headers['X-Frame-Options'] = 'SAMEORIGIN'
		
		# ---
		
		self.response.cache_control.no_cache = None
		self.response.cache_control.public = True
		self.response.cache_control.max_age = 86400
		
		# ---
		
		if not os.path.exists(final_path):
			if 'notFoundPage' in config['appengine'] and config['appengine']['notFoundPage']:
				if 'notFoundPageIsRedirect' in config['appengine'] and config['appengine']['notFoundPageIsRedirect']:
					self.redirect(config['appengine']['notFoundPage'])
					
					# ---
					
					return
					
				# ---
				
				path_parts = [self.root] + config['appengine']['notFoundPage'].split('/')
				final_path = os.path.join(*path_parts)
				
				# ---
				
				if not os.path.exists(final_path):
					return
					
				# ---
				
				self.response.set_status(404)
				
			else:
				return
				
		# ---
		
		file = open(final_path)
		
		self.response.write(file.read())
		
		file.close()
		
# ---

routes = []

# ---

if 'permanents' in config['appengine']:
    for route, url in config['appengine']['permanents'].iteritems():
        routes.append(webapp2.Route(route, webapp2.RedirectHandler, defaults={'_code': 301, '_uri': url}))
		
# ---

if 'redirects' in config['appengine']:
    for route, url in config['appengine']['redirects'].iteritems():
        routes.append(webapp2.Route(route, webapp2.RedirectHandler, defaults={'_code': 302, '_uri': url}))
    		
# ---

routes.append(('/.*', RequestHandler))

# ---

application = webapp2.WSGIApplication(routes, debug=False)