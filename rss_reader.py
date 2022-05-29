# -*- coding: utf-8 -*-
"""
Created on Mon May  2 22:15:46 2022

@author: Arthur
"""
from html_parser import MyHTMLParser
import feedparser
import json

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
        self._rss_link_list = self.get_rss_link()
        self.html_parser = MyHTMLParser()
        
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
    
    def get_rss_feed(self, key=''):
        datas = []
        for i, rss_url in enumerate(self._rss_link_list):
            d = feedparser.parse(rss_url)
            entries = d.get(key,d)
            datas += entries
        
        return datas
    
    def get_information_list(self):
        entries = self.get_rss_feed('entries')        
        
        information_list = [None]*len(entries)
        
        for i, entrie in enumerate(entries):
            self.html_parser.feed(entrie["summary_detail"]["value"])
            information_list[i] = self.html_parser.get_data() + [entrie["title_detail"]["value"], entrie["link"]]
            self.html_parser.reset_data()
        return information_list
    
    def save_articles(self, articles, path=""):
        with open(path, 'a') as f:
            json.dump(articles, f)
            
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

    # url = "https://rss.sciencedirect.com/publication/science/13598368"
    
    # d = feedparser.parse(url)
    # headers = d.get('headers')
    
    # article_list = get_information(d)
    
    # regex = r"<p\s*>(.*?)</p\s*>"
    
    rssf = RSS_feeder('storage\RSS link.txt')