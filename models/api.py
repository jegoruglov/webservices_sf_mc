import simplejson as json
import urllib
import urllib2

class SFApi(object):
	def __init__(self, sftokenuri, sfendpoint, sfclientid, sfclientsecret,
		sfusername, sfpassword, sfsecuritytoken):
		self.endpoint = sfendpoint
		data = {
			"client_id":		sfclientid,
			"client_secret":	sfclientsecret,
			"username":			sfusername,
			"password":			sfpassword+sfsecuritytoken,
			"grant_type":		"password"
		}
		data = urllib.urlencode(data)
		response = urllib2.urlopen(sftokenuri, data).read()
		response = json.loads(response)
		self.access_token = response.get('access_token', None)
	
	def create_lead(self, fname, lname, email, company, phone):
		data = {
			"FirstName":	fname,
			"LastName":		lname,
			"Company":		company,
			"Phone":		phone,
			"Email":		email
		}
		data = json.dumps(data)
		headers = {
			"Authorization": "OAuth "+self.access_token,
			"Content-type": "application/json",
		}
		request = urllib2.Request(self.endpoint+"/sobjects/Lead", data=data, headers=headers)
		try:
			response = urllib2.urlopen(request).read()
			response = json.loads(response)
			if response['success'] is True:
				return 201
			else:
				return response
		except urllib2.HTTPError, e:
			if e.code == 201:
				return 201
			else:
				raise e

class MCApi(object):
	def __init__(self, mcendpoint, mcapikey, mclistid):
		self.endpoint = mcendpoint
		self.apikey = mcapikey
		self.listid = mclistid
		
	def add_to_list(self, fname, lname, email, company, phone, listid=None,
		double_optin=False, send_welcome=True):
		if listid is None:
			listid = self.listid
		bool_converter = lambda x: str(x).lower()
		data = {
			"merge_vars[FNAME]":	fname,
			"merge_vars[LNAME]":	lname,
			"merge_vars[CMPNY]":	company,
			"merge_vars[PNMBR]":	phone,
			"email_address":		email,
			"apikey":				self.apikey,
			"id":					listid,
			"double_optin":			bool_converter(double_optin),
			"send_welcome":			bool_converter(send_welcome)
		}
		data = urllib.urlencode(data)
		response = urllib2.urlopen(self.endpoint+"/?method=listSubscribe", data).read()
		try:
			response = json.loads(response)
			return response['code']
		except:
			if response is True:
				return 201
			else:
				return response

	def list_members(self, status="subscribed"):
		data = {
			"apikey":	self.apikey,
			"id":		listid,
			"status":	status
		}
		data = urllib.urlencode(data)
		return urllib2.urlopen(self.endpoint+"/?method=listMembers", data).read()