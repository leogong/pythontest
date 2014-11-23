#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lxml.html import soupparser

root = soupparser.fromstring("<a>aaaa</a>")

if not len(root.findall(".//b")):
    print "xxx"
