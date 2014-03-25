#http://janetk-app.appspot.com/
import webapp2
import cgi
import re

form_signup = """
<h2>Signup</h2>
<form method="post">
    <label> Username
        <input type="text" name="username" value="%(username)s"> <span style="color: red">%(error_username)s</span>
    </label>
    <br>
    <label> Password
        <input type="password" name="password"> <span style="color: red">%(error_pwd)s</span>
    </label>
    <br>
    <label> Verify Password
        <input type="password" name="verify"> <span style="color: red">%(error_verify)s</span>
    </label>
    <br>
    <label> Email (optional)
        <input type="text" name="email" value="%(email)s"> <span style="color: red">%(error_email)s</span>
    </label>
    <br>
    <input type="submit">
</form>
"""

form_welcome="""
<h2>Welcome, %(username)s</h2>
<form action="welcome">
</form>
"""

form_rob13 = """
<h2>Enter some text to ROT13:</h2>
<form method="post">
    <textarea name="text" style="height: 100px; width: 400px;">%(rob)s</textarea>
    <br>
    <input type="submit">
</form>
"""

form_birthday = """
<form method="post">
    What is your birthday?
    <br>

    <label> Month
        <input type="text" name="month" value="%(month)s">
    </label>

    <label> Day
        <input type="text" name="day" value="%(day)s">
    </label>
    
    <label> Year
        <input type="text" name="year" value="%(year)s">
    </label>
    <div style="color: red">%(error)s</div>
    <br>
    <br>
    <input type="submit">
</form>
"""

form2 = """
<form method="post" action="/testform">
    <input name="q">
    <input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):
    def write_form(self, error="", month="", day="", year=""):
        self.response.write(form_birthday % {"error": error, 
            "month": escape_html(month), 
            "day": escape_html(day), 
            "year": escape_html(year)})

    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        #default content-type is html
        #self.response.write('Hello, Udacity!!!!!!!!!')
        self.write_form()

    def post(self):
        user_month = self.request.get("month")
        user_day = self.request.get("day")
        user_year = self.request.get("year")

        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)

        if not(month and day and year):
            self.write_form("Looks like an invalid input.", user_month, user_day, user_year)
        else:
            self.response.write("Thanks!")

def escape_html(s):
    #for (i, o) in (('&', '&amp;'),('>', '&gt;'),('<', '&lt;'),('"', '&quot;')):
    #   s = s.replace(i, o)
    #return s
    return cgi.escape(s, quote=True)

class Rob13Handler(webapp2.RequestHandler):
    def write_form(self, rob13=""):
        self.response.write(form_rob13 % {"rob": escape_html(rob13)})

    def post(self):
        user_rob13 = self.request.get("text")
        self.write_form(rob13(user_rob13))
        
    def get(self):
        self.write_form()

def rob13(s):
    new_s = ""
    for c in s:
        if c.isalpha():
            final = ord(c)+13
            if (c.isupper() and not chr(final).isupper()) or (c.islower() and not chr(final).islower()):
                final = final - 26
            c = chr(final)
        new_s = new_s + c
    return new_s
    #pass

class SignupHandler(webapp2.RequestHandler):
    def write_form(self, err_u="", err_p="", err_v="", err_e="", username="", email=""):
        self.response.write(form_signup % {"error_username": err_u, 
            "error_pwd": err_p, "error_verify": err_v, "error_email": err_e, 
            "username": username, "email": email})

    def post(self):
        #self.write_form()
        self.redirect('welcome')

    def get(self):
        self.write_form()

class WelcomeHandler(webapp2.RequestHandler):
    def write_form(self, username=""):
        self.response.write(form_welcome % {"username": username})
    
    def get(self):
        username = self.request.get("username")
        self.write_form(username)

    def post(self):
        username = self.request.get("username")
        self.write_form(username)



class TestHandler(webapp2.RequestHandler):
    def post(self):
        q = self.request.get("q")
        #self.response.write(q)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(self.request)

    def get(self):
        q = self.request.get("q")
        self.response.write(q)

        # print out the content of the request 
        #self.response.headers['Content-Type'] = 'text/plain'
        #self.response.write(self.request)


application = webapp2.WSGIApplication([
    ('/', MainPage), #'/' will be handled by MainPage
    ('/testform', TestHandler),
    ('/rob13', Rob13Handler),
    ('/signup', SignupHandler),
    ('/welcome', WelcomeHandler),
], debug=True)