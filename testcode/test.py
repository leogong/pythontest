#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

aDict = {}

aDict["我"] = "们"

print  json.dumps(aDict, encoding='UTF-8', ensure_ascii=False)