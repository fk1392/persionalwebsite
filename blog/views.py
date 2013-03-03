#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint, session, render_template, request, escape, redirect, url_for, abort
from db import Session 
from sqlalchemy import desc
from db import Blog, Base, engine
import blogsettings as config
import markdown

blog = Blueprint("blog", __name__, template_folder = "templates", static_folder = "static")


# 文章页展示
@blog.route("/", defaults = {"page" : 1})
@blog.route("/<page>")
def blogindex(page):
    try:
        page = int(page)
    except:
        page = 1
    if page <= 0:
        abort(404)
    s = Session()
    blogs = s.query(Blog).order_by(desc(Blog.date))
    try:
        if session["username"] != config.username or session["password"] != config.password:
            raise
    except:
        blogs = blogs.filter(Blog.visual == 0)
    catalog = {}
    for i in blogs:
        if i.catalog in catalog:
            catalog[i.catalog].append(i)
        else:
            catalog[i.catalog] = [i,]
    blog_count = blogs.count()
    #if blog_count == 0 :
    #    if "username" in session and "password" in session:
    #        return render_template("addpost.html",blog_count = 0)
    #    else:
    #        return render_template("login.html",message = u"你还没有一篇文章 先去登陆吧")
    page_count = (blog_count + config.blog_per_page - 1) / config.blog_per_page
    #blogs = s.query(Blog).order_by(desc(Blog.date)).offset((page - 1) * config.blog_per_page).limit(config.blog_per_page)
    blogs = blogs.offset((page - 1) * config.blog_per_page).limit(config.blog_per_page)

    return render_template("index.html", blogs = blogs, config = config,page = page, page_count = page_count, catalog = catalog)

# catalog展示
@blog.route("/catalog/<argument>",defaults = {"page":1})
@blog.route("/catalog/<argument>/<page>")
def showcatalog(argument,page):
    try:
        page = int(page)
    except:
        page = 1
    if page <= 0:
        abort(404)
    s = Session()
    blogs = s.query(Blog).order_by(desc(Blog.date))
    try:
        if session["username"] != config.username or session["password"] != config.password:
            raise
    except:
        blogs = blogs.filter(Blog.visual == 0)
    catalog = {}
    for i in blogs:
        if i.catalog in catalog:
            catalog[i.catalog].append(i)
        else:
            catalog[i.catalog] = [i,]
    blogs = blogs.filter(Blog.catalog == argument)
    blog_count = blogs.count()
    if blog_count == 1:
        return redirect(url_for("blog.showpost",pid = blogs.first().pid))
    page_count = (blog_count + config.blog_per_page - 1) / config.blog_per_page
    blogs = blogs.offset((page - 1) * config.blog_per_page).limit(config.blog_per_page)
    
    return render_template("catalog.html", blogs = blogs,title = argument, config = config,page = page, page_count = page_count, catalog = catalog,cat = argument)


# 博客展示
@blog.route("/post/<pid>")
def showpost(pid):
    s = Session()
    blogs = s.query(Blog).order_by(desc(Blog.date))
    try:
        if session["username"] != config.username or session["password"] != config.password:
            raise
    except:
        blogs = blogs.filter(Blog.visual == 0)
    catalog = {}
    for i in blogs:
        if i.catalog in catalog:
            catalog[i.catalog].append(i)
        else:
            catalog[i.catalog] = [i,]
    try:
        blog = s.query(Blog).filter_by(pid = pid).first()
    except:
        abort(404)
    return render_template("post.html",config = config ,blog = blog,catalog = catalog,title = blog.title)


# 增加文章
@blog.route("/post/add",methods = ["GET","POST"])
def addpost():
    if request.method == "GET":
        if "username" in session:
            if escape(session["username"]) == config.username and escape(session["password"]) == config.password:
                return render_template("addpost.html",config = config)
            else:
                render_template("login.html",config = config,message = u"你搞毛啊 伪造session？操蛋！")
        else:
            return render_template("login.html",config = config,message = u"你还没登陆！")
    elif request.method == "POST":
        try:
            blog = Blog(request.form["image"],request.form["title"],request.form["date"],request.form["content"],markdown.markdown(request.form["content"]),request.form["catalog"],int(request.form["visual"]), int(request.form["technology"]))
        except:
            abort(404)
        s = Session()
        s.add(blog)
        s.commit()
        return redirect(url_for("blog.blogindex"))
    else:
        abort(404)


# 编辑文章
@blog.route("/post/vim/<pid>",methods = ["GET","POST"])
def vimpost(pid):
    try:
        if escape(session["username"]) != config.username or escape(session["password"]) != config.password:
            raise
    except:
        abort(404)
    if request.method == "GET":
        s = Session()
        try:
            blog = s.query(Blog).filter_by(pid = pid).first()
        except:
            abort(404)
        return render_template("vimpost.html",blog = blog)
    elif request.method == "POST":
        s = Session()
        try:
            s.query(Blog).filter_by(pid = pid).update({"title":request.form["title"],"date":request.form["date"],"image":request.form["image"],"origin_content":request.form["content"],"content":markdown.markdown(request.form["content"]),"visual":int(request.form["visual"]),"technology":int(request.form["technology"])})
            s.commit()
        except:
            abort(404)
        return redirect(url_for("blog.blogindex"))
    else:
        abort(404)


# 删除文章
@blog.route("/post/rm/<pid>")
def rmpost(pid):
    try:
        if escape(session["username"]) != config.username or escape(session["password"]) != config.password:
            raise
    except:
        abort(404)
    s = Session()
    try:
        s.delete(s.query(Blog).filter_by(pid = pid).first())
        s.commit()
    except:
        abort(404)
    return redirect(url_for("blog.blogindex"))


# 登陆页面
@blog.route("/login",methods = ["GET","POST"])
def bloglogin():
    if "username" in session:
        if escape(session["username"]) == config.username and escape(session["password"]) == config.password:
            return redirect(url_for("blog.blogindex"))
        else:
            return render_template("login.html",config = config,title = u"登陆")
    else:
        if request.method == "GET":
            return render_template("login.html",config = config,title = u"登陆")
        elif request.method == "POST":
            if request.form["username"] == config.username and request.form["password"] == config.password:
                session["username"] = request.form["username"]
                session["password"] = request.form["password"]
                return redirect(url_for("blog.blogindex"))
    return render_template("login.html",config = config,title = u"登陆")


# 登出
@blog.route("/logout")
def bloglogout():
    if "username" in session and "password" in session:
        session.pop("username",None)
        session.pop("password",None)
    return redirect(url_for("blog.blogindex"))


# 数据库安装
@blog.route("/install")
def bloginstall():
    try:
        if "username" not in session or "password" not in session:
            raise
        Base.metadata.create_all(engine)
    except:
        return render_template("message.html",title = 500,config = config, message = u"数据库创建失败，原因未知")
    return render_template("message.html" ,config = config, message = u"数据库部署完成,你不需要运行2次")

@blog.errorhandler(404)
def hander404(error):
    return render_template("404.html")
