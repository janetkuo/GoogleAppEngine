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
import re

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

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PWD_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PWD_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)

class Signup(BaseHandler):
    def get(self):
        self.render('signup-form.html')

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        error_username = ""
        error_pwd = ""
        error_verify = ""
        error_email = ""
        has_error = False

        if not valid_username(username):
            error_username = "That's not a valid username."
            has_error = True
        if not valid_password(password):
            error_pwd = "That wasn't a valid password."
            has_error = True
        if password != verify:
            error_verify = "Your passwords didn't match."
            has_error = True
        if email != "" and not valid_email(email):
            error_email = "That's not a valid email."
            has_error = True
        
        if has_error:
            self.render('signup-form.html', username=username, email=email, 
                error_username=error_username, error_pwd=error_pwd, error_verify=error_verify, error_email=error_email)
        else:
            # redirect to welcome page (get method) with username parameter 
            self.redirect('/blog/welcome?username=' + username)

class Welcome(BaseHandler):
    def get(self):
        username = self.request.get("username")
        if not valid_username(username):
            self.redirect('/blog/signup')
        else:
            self.render('welcome.html', username=username)

app = webapp2.WSGIApplication([
    ('/blog/rot13', Rot13), 
    ('/blog/signup', Signup),
    ('/blog/welcome', Welcome)
], debug=True)
