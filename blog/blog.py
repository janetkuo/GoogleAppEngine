#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2

# Jinja2 is a powerful templating engine modeled after Django's templating system. 
# The idea is to separate your logic from your presentation, and make your code clean and well-defined in the process.
# https://www.udacity.com/wiki/cs253/appendix_b
import jinja2

# from google.appengine.ext import db

# create an "environment" using which we can access the templating functions
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

def render_str(template, **params):
    # retrieve a template object using jinja_environment.get_template
    t = jinja_env.get_template(template)
    # render and write out the resulting HTML using template.render(template_values)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.write(*a, **kw)

class Rot13(BaseHandler):
    def get(self):
        self.render('rot13-form.html')

    def post(self):
        rot13 = ''
        text = self.request.get('text')
        if text:
            # do rot13 encode to the text
            rot13 = text.encode('rot13')
        self.render('rot13-form.html', text = rot13)

app = webapp2.WSGIApplication([
    ('/blog/rot13', Rot13)
], debug=True)
