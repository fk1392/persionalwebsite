#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json

site_title = u"樱宝宝のblog"
mysql = json.loads(os.getenv("VCAP_SERVICES"))["mysql-5.1"][0]["credentials"]
#engine_string = "postgresql://%s:%s@%s/%s"%(pg["username"],pg["password"],pg["hostname"],pg["name"])
engine_string = "mysql+mysqldb://%s:%s@%s/%s"%(mysql["username"],mysql["password"],mysql["hostname"],mysql["name"])
debug = False
blog_per_page = 8
username = "xuanmingyi"
password = "joyceandy098816"
