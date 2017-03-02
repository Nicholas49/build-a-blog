import webapp2
import jinja2
import os

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class submyxen(db.Model):
    taitl = db.StringProperty(required = True)
    tekst = db.TextProperty(required = True)
    krieited = db.DateTimeProperty(auto_now_add = True)


class index(Handler):


    def get(self):
        self.render("newpost.html", taitl="", tekst="", eror="")

    def post(self):
        taitl = self.request.get("taitl")
        tekst = self.request.get("tekst")

        if taitl and tekst:
            a = submyxen(taitl = taitl, tekst = tekst)
            a.put()

            self.redirect("/blog/" + str(a.key().id()))
        else:
            eror = "Please enter a title and a message!"
            self.render("newpost.html", taitl=taitl, tekst=tekst, eror=eror)

class blaug(Handler):

    def get(self):
        teksts = db.GqlQuery("select * from submyxen order by krieited desc limit 5")
        self.render("blog.html", teksts=teksts)

class blaug_post(Handler):

    def get(self, id):

        stuf = submyxen.get_by_id(int(id))

        self.render("blog_post.html", dqunk=stuf)



app = webapp2.WSGIApplication([
    ('/', index),
    ('/blog', blaug),
    webapp2.Route('/blog/<id:\d+>', blaug_post)
], debug=True)
