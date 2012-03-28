from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os
from google.appengine.ext.webapp import template

class Gift(db.Model):
    name = db.StringProperty(required=True)
    url = db.StringProperty(required=True)	
    reserved = db.BooleanProperty(default=False)
    order_value = db.IntegerProperty(default=0)


class MainPage(webapp.RequestHandler):
    def get(self):

        user = users.get_current_user()


        self.response.headers['Content-Type'] = 'text/plain'
	gifts = Gift.all()
	for gift in gifts:
	    self.response.out.write('gift '+gift.desc) 
	    self.response.out.write(' ')

        if user:
            self.response.out.write('Hello, webapp World! '+user.nickname())
        else:
#            self.redirect(users.create_login_url(self.request.uri))
            self.response.out.write('Hello, webapp World!')

	template_values = {
		'val': 'test'
	}
	path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
	

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
