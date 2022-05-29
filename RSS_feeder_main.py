# -*- coding: utf-8 -*-
"""
Created on Sat May  7 16:04:51 2022

@author: Arthur
"""
import numpy as np
import json
# from gui_rss_reader import MainApp
from rss_reader import get_information, Article, RSS_feeder


def generate_random_article(number_of_articles):
    random_array = np.random.randint(0,1000,[number_of_articles,4])
    
    article_list = np.array([Article(f'title{num[0]}', f'authors{num[1]}', f'date_of_publication{num[2]}', f'source{num[3]}') for num in random_array])
    
    return article_list

def save_article_list(article_list):
    with open("article_list.txt", 'w') as f:
        for article in article_list:
            f.write(str(article))
  
def save_articles(articles, path=""):
    with open(path, 'a') as f:
        json.dump(articles, f)

if __name__ == '__main__':
    # article_list = generate_random_article(number_of_articles=100)
    # save_article_list(article_list)
    # MainApp(article_list).run()
    
    rssf = RSS_feeder('storage\RSS link.txt')
    entries = rssf.get_rss_feed('entries')
    information_list = rssf.get_information_list()
    
    information_dict = {key:{'title':information[3],'date_of_publication':information[0]\
                             ,'source':information[1],'authors':information[2], 'link':information[4]}\
                        for key, information in enumerate(information_list)}

    save_article_list(information_dict, "storage/articles.json")