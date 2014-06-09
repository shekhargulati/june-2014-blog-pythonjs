import tornado, tornado.web, tornado.ioloop
import os

PATHS = { 'webroot': './static'}

def get_main_page(server):
	local_path = os.path.join( PATHS['webroot'], "index.html" )
	data = open(local_path, 'r').read()
	data = convert_python_html_document( data )
	return data
					
def convert_python_html_document( data ):
	doc = list()
	script = None
	for line in data.splitlines():

		if line.strip().startswith('<script'):
			if 'type="text/python"' in line:
				doc.append( '<script type="text/javascript">')
				script = list()
			else:
				doc.append( line )

		elif line.strip() == '</script>':
			if script:
				#src = '\n'.join( script ) 
				src = chr(10).join(script)
				js = pythonjs.translator.to_javascript( src )
				doc.append( js )
			doc.append( line )
			script = None

		elif isinstance( script, list ):
			script.append( line )

		else:
			doc.append( line )

	return '\n'.join( doc )



class MainHandler( tornado.web.RequestHandler ):
	def get(self, path=None):
		print('path', path)

		if path == "":
			data = get_main_page()
			self.set_header("Content-Type", "text/html; charset=utf-8")
			self.write( get_main_page() )
		elif path == 'pythonjs.js':
			data = pythonjs.runtime.javascript
			self.set_header("Content-Type", "text/javascript; charset=utf-8")
			self.set_header("Content-Length", len(data))
			self.write(data)
		else:
			if path == 'favicon.ico':
				self.write('')
			else:
				self.write('File not found')


handlers = [
	('/', MainHandler)
]

app = tornado.web.Application( handlers )
ip   = 'localhost'
port = 8080
if os.environ.get('OPENSHIFT_NODEJS_IP'):
	ip = os.environ.get('OPENSHIFT_NODEJS_IP')
	port = int(os.environ.get('OPENSHIFT_NODEJS_PORT'))

app.listen(port,ip)
tornado.ioloop.IOLoop.instance().start()
print('App running on %s:%s' % (ip,port))