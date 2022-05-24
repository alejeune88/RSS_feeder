# -*- coding: utf-8 -*-
"""
Created on Mon May  2 22:15:46 2022

@author: Arthur
"""

import feedparser

class Article:
    def __init__(self, title, authors, date_of_publication, source)->None:
        self.title, self.authors, self.date_of_publication, self.source = title, authors, date_of_publication, source
    
    def __str__(self):
        return f"title : {self.title}; authors : {self.authors}; date_of_publication : {self.date_of_publication}; source : {self.source} \n"
    
    def __repr__(self):
        return f"title : {self.title} \nauthors : {self.authors} \ndate_of_publication : {self.date_of_publication} \nsource : {self.source} \n"

    def get_title(self):
        return self.title
    def get_authors(self):
        return self.authors
    def get_date_of_publication(self):
        return self.date_of_publication
    def get_source(self):
        return self.source
    
class RSS_feeder():
    def __init__(self, link_path:str=None):
        self._link_path = link_path
        self._rss_link_list = self.get_RSS_link()
        
    def get_link_path(self):
        return self._link_path
    
    def set_link_path(self, new_link_path):
        self._link_path = new_link_path
        
    link_path = property(get_link_path, set_link_path) 
    
    def get_rss_link(self):
        file_path = self._link_path
        data_list = []
        if not (file_path is None):
            with open(file_path) as file:
                data_list = file.readlines()[1:]
            
            for i, data in enumerate(data_list):
                data_list[i] = data.rstrip('\n')
        return data_list
    
    def get_rss_feed(self):
        
        for rss_url in self._journal_link_list:
            d = feedparser.parse(rss_url)
            headers = d.get('headers')
        
        return headers
        
    
def get_information(d:dict)->list:
    
    information_list = ["title",""]
    
    entries = d.get("entries")
    n_article = len(entries)
    article_list = [None]*n_article
    
    for i,information in enumerate(entries):

        article = Article(information.get("title"), information.get("authors"), information.get("date_of_publication"), information.get("source"))
        article_list[i] = article
        
    return article_list



if __name__ == "__main__":

    url = "https://rss.sciencedirect.com/publication/science/13598368"
    
    
    
    d = feedparser.parse(url)
    headers = d.get('headers')
    
    article_list = get_information(d)
    
    regex = r"<p\s*>(.*?)</p\s*>"