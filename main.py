import webapp2
import jinja2
import os
import urllib2
import json
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

class MainHandler(BaseHandler):
    def get(self):
        self.render('welcome.html')
    def post(self):
        zipp = self.request.get('zip')
        result_json = urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?q=%s' %(zipp))
        data = json.load(result_json)
        country = data['sys']['country']
        town = data['name']
        weather = data['weather'][0]['description']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        temparature = data['main']['temp']
        temp = temparature-273
        temp_min = data['main']['temp_min'] - 273
        temp_max = data['main']['temp_max'] - 273
        self.render('weather.html',country=country,temp=temp,temp_min=temp_min,temp_max=temp_max,weather=weather,town=town,pressure=pressure,humidity=humidity)
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
