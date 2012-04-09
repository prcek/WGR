from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os
from google.appengine.ext.webapp import template
import logging

class Gift(db.Model):
    name = db.StringProperty(required=True)
    url = db.StringProperty(required=True)	
    reserved = db.BooleanProperty(default=False)
    nores = db.BooleanProperty(default=False)
    order_value = db.IntegerProperty(default=0)
    


class MainPage(webapp.RequestHandler):
	def post(self):
		a = self.request.get('action')
		logging.info('action='+a)
		if (a == 'add'):
			gift = Gift(url='xxx',name='tddd')
			gift.url=self.request.get('url')
			gift.name=self.request.get('name')
			gift.order_value=int(self.request.get('order_value'))
			gift.nores = False
			gift.put()
			self.redirect('/?turin=1')
			return
		
		k = self.request.get('key')
		key = db.Key(k)	
		gift = Gift.get(key)	
		logging.info(gift.name)
		if a == 'res':
			gift.reserved=True	
			gift.put()
			self.redirect('/')
			return
			
		if a == 'unres':
			gift.reserved=False
			gift.put()
		if a == 'del':
			gift.delete()

		self.redirect('/')

	def get(self):
		logging.info('get')
		k = self.request.get('key')
		if k:
			logging.info(k)
			key = db.Key(k)
			gift = Gift.get(key)	
			logging.info(gift.name)
			gift.reserved=True	
			gift.put()
			logging.info('redir /')
			self.redirect('/')
			return


		user = users.get_current_user()

		gifts = Gift.all().order('order_value')

		auth = self.request.get('turin')

		template_values = {
#			'auth': users.is_current_user_admin(),
			'auth': auth,
			'user':user,
			'gifts': gifts
		}
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))
	

application = webapp.WSGIApplication( 
				     [ ('/', MainPage) ]
				     , debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
