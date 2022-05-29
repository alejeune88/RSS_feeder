# -*- coding: utf-8 -*-
"""
Created on Sun May 29 12:04:47 2022

@author: ArthurAdmin
"""

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []
        self.p = False
        self.b = False
    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.p = True
        if tag == 'b':
            self.b = True

    def handle_endtag(self, tag):
        if tag == 'p':
            self.p = False
        if tag == 'b':
            self.b = False

    def handle_data(self, data):
        if self.p and not self.b:
            self.data.append(data.lstrip(" "))
    
    def get_data(self):
        return self.data
    
    def reset_data(self):
        self.data = []
   
if __name__ == '__main__': 
    parser = MyHTMLParser()
    
    string = '<p>Publication date: 1 July 2022</p><p><b>Source:</b> Composites Part B: Engineering, Volume 240</p><p>Author(s): Yanran Liu, Hanfang Zhang, Yihe Zhang, Ce Liang, Qi An</p>'
    parser.feed(string)
    data =  parser.get_data()
