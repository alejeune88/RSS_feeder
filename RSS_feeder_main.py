# -*- coding: utf-8 -*-
"""
Created on Sat May  7 16:04:51 2022

@author: Arthur
"""
import numpy as np

# from gui_rss_reader import MainApp
from rss_reader import get_information, Article


def generate_random_article(number_of_articles):
    random_array = np.random.randint(0,1000,[number_of_articles,4])
    
    article_list = np.array([Article(f'title{num[0]}', f'authors{num[1]}', f'date_of_publication{num[2]}', f'source{num[3]}') for num in random_array])
    
    return article_list

def save_article_list(article_list):
    with open("article_list.txt", 'w') as f:
        for article in article_list:
            f.write(str(article))
    

if __name__ == '__main__':
    article_list = generate_random_article(number_of_articles=100)
    save_article_list(article_list)
    # MainApp(article_list).run()
