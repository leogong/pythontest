# coding=utf-8
from lxml import etree
from lxml.html import soupparser

__author__ = 'leo'

html = soupparser.fromstring("<div><a href> aa </a></div>")
html_findall = html.findall(".//a")
for a in html_findall:
    print etree.tostring(a, encoding="utf-8", method="html", pretty_print=True)
