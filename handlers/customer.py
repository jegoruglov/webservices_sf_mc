import re
import simplejson as json
from base import BaseHandler
from google.appengine.api import urlfetch
import urllib

class CustomerHandler(BaseHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        client_data = self.get_form_data()
        if client_data['error']:
            self.response.out.write("Invalid form data: %s"%(str(client_data['error'])))
        else:
            kwargs = client_data['data']
            mcresponse = self.mc_api.add_to_list(**kwargs)
            if mcresponse == 214:
                self.response.out.write("%s already subscribed"%(kwargs['email']))
                return
            sfresponse = self.sf_api.create_lead(**kwargs)
            if mcresponse == 201 and sfresponse == 201:
                self.response.out.write("<p>Data successfully sent</p>")
            else:
                self.response.out.write("<p>Saving data failed</p>")
            self.response.out.write("<p>Mailchimp response: %s, Salesforce response: %s</p>"%(str(mcresponse),str(sfresponse)))

    def post(self):
    	self.get()

    def get_form_data(self):
        data = {}
        remap = {
            "fname":    (1, "^[-A-Za-z' .]*$"),
            "lname":    (1, "^[-A-Za-z' .]*$"),
            "phone":    (1, "^[- +0-9]{4,16}$"),
            "email":    (1, "[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])"),
            "company":  (1, "^[-A-Za-z' .]*$"),
        }
        
        errors = []
        for field, regex in remap.iteritems():
            value = self.request.get(field, "")
            data[field] = value
            if not value and regex[0]:
                errors.append("Field %s is required"%(field))
            elif value and not re.match(regex[1], value):
                errors.append("Field %s is invalid"%(field))
        return {
            "error":    errors,
            "data":     data
        }