from base import BaseHandler
from google.appengine.ext.webapp import template

class HomeHandler(BaseHandler):
    def get(self):
        self.render('home.html')