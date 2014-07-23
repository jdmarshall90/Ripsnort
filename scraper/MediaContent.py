#!/usr/bin/env python
# -*- coding: utf-8 -*-


class MediaContent:
    def __init__(self):
        self.content_type = None
        self.production_year = -1
        self.title = None
        self.durationS = 0
        self.scrape_source = None
        self.unique_id = None
        
        
    def __repr__(self):
        retStr = "<MediaContent "
        retStr += "content: " + self.content_type + ", "
        retStr += "year: " + str(self.production_year) + ", "
        retStr += "title: " + self.title + ", "
        retStr += " >"
        
        return retStr