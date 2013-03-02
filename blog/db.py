#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, scoped_session
import blogsettings as config
import uuid

Base = declarative_base()
engine = create_engine(config.engine_string,echo = config.debug)
Session = scoped_session(sessionmaker())
Session.configure(bind = engine)

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key = True)
    pid = Column(String)
    image = Column(String)
    title = Column(String)
    date = Column(Integer)
    catalog = Column(String)
    origin_content = Column(String)
    content = Column(String)
    # viusal 0表示可见 1表示不可见 默认可见
    visual = Column(Integer)
    # technology 0表示技术博客 1表示非技术博客 默认技术
    technology = Column(Integer)

    def __init__(self,image,title,date,origin_content,content,catalog,visual = 0,technology = 0):
        self.image = image
        self.title = title
        self.date = date
        self.origin_content = origin_content
        self.content = content
        self.catalog = catalog
        self.visual = visual
        self.technology = technology
        self.pid = str(uuid.uuid4())
