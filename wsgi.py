#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, redirect, render_template
from blog.views import blog


application = Flask(__name__)
application.register_blueprint(blog, url_prefix = "/blog")
application.secret_key = "a\-9s../d\\_(*5203 ~psa"
@application.route("/")
def index():
    return redirect("/blog")

@application.errorhandler(404)
def hander404(error):
    return open("blog/templates/404.html").read()

if __name__ == "__main__":
    application.run(host="0.0.0.0",port=9898,debug = True)
