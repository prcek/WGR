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
    order_value = db.IntegerProperty(default=0)


class MainPage(webapp.RequestHandler):
    def post(self):
	a = self.request.get('action')
	logging.info('action='+a)
	if (a == 'add'):
		gift = Gift(url='xxx',name='tddd')
		gift.url='xxx'	
		gift.name='tsss'
		gift.put()


	self.redirect('/')

    def get(self):

        user = users.get_current_user()

	gifts = Gift.all().order('order_value')


	template_values = {
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
