from google.appengine.ext import webapp
from config import conf
from google.appengine.ext.webapp import template
from models.api import SFApi, MCApi

class BaseHandler(webapp.RequestHandler):
	def __init__(self):
		self.settings = conf.__dict__

	@property
	def sf_api(self):
		if not hasattr(self, "_sf_api"):
			self._sf_api = SFApi(
				self.settings["sftokenuri"], 
				self.settings["sfendpoint"], 
				self.settings["sfclientid"], 
				self.settings["sfclientsecret"],
				self.settings["sfusername"], 
				self.settings["sfpassword"], 
				self.settings["sfsecuritytoken"]
			)
		return self._sf_api

	@property
	def mc_api(self):
		if not hasattr(self, "_mc_api"):
			self._mc_api = MCApi(
				self.settings["mcendpoint"], 
				self.settings["mcapikey"], 
				self.settings["mclistid"], 
			)
		return self._mc_api

	def render(self, file_name, kwargs={}):
		path = 'html/'+file_name
		self.response.out.write(template.render(path, kwargs))