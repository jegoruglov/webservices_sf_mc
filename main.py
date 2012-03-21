from google.appengine.ext.webapp import WSGIApplication
from google.appengine.ext.webapp.util import run_wsgi_app
from handlers.home import HomeHandler
from handlers.customer import CustomerHandler

application = WSGIApplication(
    [('/?', HomeHandler),
     ('/customer', CustomerHandler)],
    debug=True)

def main():
    run_wsgi_app(application)
   

if __name__ == "__main__":
    main()
