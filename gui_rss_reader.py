# -*- coding: utf-8 -*-
"""
Created on Tue May  3 20:19:07 2022

@author: Arthur
"""
#If OpenGL 2.0 is not supported
import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from functools import partial

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock

import numpy as np
from rss_reader import get_information, Article
from kivy.uix.scrollview import ScrollView

import json
import webbrowser

class MainScreen(Screen):
    state = 'normal'
    pass
class ArticleScreen(Screen):
    state = 'normal'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.article_grid_layout = Article_grid_layout()
        
    def get_height(self):
        article_list = self.get_article_list()
        return len(article_list)
    
    def get_article_list(self):
        article_list_path = 'article_list.txt'
        with open(article_list_path,'r') as f:
            article_list = f.readlines()
        return article_list
    
    def get_article_layout(self):
        article_list = self.get_article_list()
        article_layout_list = [Article_layout(article_str) for i, article_str in enumerate(article_list)]
        return article_layout_list
    
    def get_article_grid_layout(self):
        article_grid_layout = Article_grid_layout()
        # article_layout_list = self.get_article_layout()
        article_grid_layout.add_article_layout(self.get_article_layout())
        # article_grid_layout.add_widget(article_layout_list[0])
        # article_grid_layout.add_widget(article_layout_list[1])
        return  article_grid_layout
            
    pass

class MainLayout(BoxLayout):
    pass

class RssSubScreen(Screen):
    state = 'normal'
    pass

class FilterScreen(Screen):
    state = 'normal'
    pass

class Top_layout(GridLayout):
    pass

class Bottom_layout(GridLayout):
    pass

class MenuButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Article_layout(FloatLayout):
    def __init__(self, article_info, index, **kwargs):
        self.article_info = article_info
        self.index = str(index)
        super().__init__(**kwargs)
    def set_index(self, new_index):
        self.index = str(new_index)
        
    def __repr__(self):
        return f'article:{self.index}, {self.article_info}'
    
class RSS_link_layout(FloatLayout):
    def __init__(self, rss_link, index, **kwargs):
        self.rss_link = rss_link
        self.index = index
        super().__init__(**kwargs)
    
class MainApp(App):
    
    def __init__(self, articles_path, links_path, **kwargs):
        self.articles_path = articles_path
        self.links_path = links_path
        self.article_screen_state = 'normal'
        super().__init__(**kwargs)
        
    def build(self):
        self.article_list = self.get_article_list()
        self.rss_sub_list = self.get_rss_sub_list()
        self.article_layout_list = []
        self.rss_sub_layout_list = []
        self.last_deleted_link = None
        self.selected_article = set()
        Builder.load_file('RSS_kivy.kv')
        ML = MainLayout()
        # Create the manager
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name="main_screen"))
        self.sm.add_widget(ArticleScreen(name="article_screen"))
        self.sm.add_widget(RssSubScreen(name="rss_sub_screen"))
        self.sm.add_widget(FilterScreen(name="filters_screen"))
    
        ML.add_widget(self.sm)
        return ML
    
    def get_article_list(self):

        with open(self.articles_path,'r') as f:
            article_dict = json.load(f)
        article_list=[article_dict[key] for key in article_dict.keys()]
        
        return article_list
    
    def get_article_layout_list(self, article_list):
        article_layout_list = [None]*len(article_list)
        for i, article_info in enumerate(article_list):
            article_layout_list[i] = Article_layout(article_info=article_info, index=i)
        return article_layout_list
    
    def get_rss_sub_layout_list(self, rss_sub_list):
        rss_sub_layout_list = [None]*len(rss_sub_list)
        for i, rss_sub in enumerate(rss_sub_list):
            rss_sub_layout_list[i] = RSS_link_layout(rss_link=rss_sub, index=i)
        return rss_sub_layout_list
    
    def get_rss_sub_list(self):
        header = 1
        with open(self.links_path,'r') as f:
            links = f.readlines()
        rss_link = [link.rstrip('\n') for link in links[header:]]
        return rss_link
    
    
    def adjust_scroll(self, bottom, dt, screen_name):
        vp_height = self.sm.get_screen(screen_name).ids.scroll.viewport_size[1]
        sv_height = self.sm.get_screen(screen_name).ids.scroll.height
        self.sm.get_screen(screen_name).ids.scroll.scroll_y = bottom / (vp_height - sv_height)
    
    def update_scrollview(self, screen_name):
        
        self.sm.get_screen(screen_name).ids.box.clear_widgets()
        vp_height = self.sm.get_screen(screen_name).ids.scroll.viewport_size[1]
        sv_height = self.sm.get_screen(screen_name).ids.scroll.height
        
        if screen_name == "article_screen":
            if len(self.article_layout_list) == 0:
                self.article_layout_list = self.get_article_layout_list(self.article_list)
                
            for i, article_layout in enumerate(self.article_layout_list[::-1]):
                self.sm.get_screen(screen_name).ids.box.add_widget(article_layout, index=i)
                
        elif screen_name == "rss_sub_screen":
            if len(self.rss_sub_layout_list) == 0:
                self.rss_sub_layout_list = self.get_rss_sub_layout_list(self.rss_sub_list)
                
            for i, rss_sub_layout in enumerate(self.rss_sub_layout_list[::-1]):
                self.sm.get_screen(screen_name).ids.box.add_widget(rss_sub_layout)
                
        if vp_height > sv_height:  # otherwise there is no scrolling
            # calculate y value of bottom of scrollview in the viewport
            scroll = self.sm.get_screen(screen_name).ids.scroll.scroll_y
            bottom = scroll * (vp_height - sv_height)
            # use Clock.schedule_once because we need updated viewport height
            # this assumes that new widgets are added at the bottom
            # so the current bottom must increase by the widget height to maintain position
            Clock.schedule_once(partial(self.adjust_scroll, bottom, screen_name=screen_name), -1)
    
    def add_rss_sub_link(self):
        input_value = self.root.get_screen("rss_sub_screen").ids.input_rss_link.text
        self.rss_sub_list.append(input_value)
        index = len(self.rss_sub_list)-1
        self.rss_sub_layout_list.append(RSS_link_layout(rss_link=input_value, index=index))
        self.update_scrollview("rss_sub_screen")
    
    def delete_rss_sub_link(self, link_index):
        del self.rss_sub_list[link_index]
        self.last_deleted_link = self.rss_sub_layout_list.pop(link_index)
        self.update_scrollview("rss_sub_screen")
    
    def save(self):
        articles_dict = { key:article for key,article in enumerate(self.article_list)}
            
        with open(self.articles_path,'w') as f:
            json.dump(articles_dict, f)
        
        rss_sub_str = "##RSS LINK STORAGE FILE##\n"
        for rss_link in self.rss_sub_list:
            rss_sub_str+= f'{rss_link}\n'
        rss_sub_str.rstrip("\n")
        with open(self.links_path, 'w') as f:
            f.write(rss_sub_str)
        
    def close_application(self):
        # closing application
        App.get_running_app().stop()
        # removing window
        Window.close()
    
    def open_link(self, link):
        webbrowser.open(link)
    
    def select_article(self, article_index):
        article_index = int(article_index)
        if article_index in self.selected_article:
            self.selected_article.remove(article_index)
        else:
            self.selected_article.add(article_index)
    
    def delete_article(self):

        last_deleted_article_list = [None]*len(self.selected_article)
        
        article_array = np.array(self.article_list,dtype=object)
        article_layout_array = np.array(self.article_layout_list,dtype=object)
        delete_article_index = list(self.selected_article)
        
        self.article_list = list(np.delete(article_array, delete_article_index))
        last_deleted_article_list = list(article_layout_array[delete_article_index])
        self.article_layout_list = list(np.delete(article_layout_array, delete_article_index))
        
        for i, article in enumerate(self.article_layout_list):
            article.set_index(i)
            article.ids.number.text=article.index
        #     del self.article_list[article_index]
        #     last_deleted_article_list[i] = self.article_layout_list.pop(article_index)
        self.update_scrollview("article_screen")
        self.selected_article = set()
    
    def get_transition(self, start, end):
        d = {
            "main_screen":{"article_screen":"up", "rss_sub_screen":"up", "filters_screen":"up"},
            "article_screen":{"main_screen":"down", "rss_sub_screen":"left", "filters_screen":"left"},
            "rss_sub_screen":{"article_screen":"right", "main_screen":"down", "filters_screen":"left"},
            "filters_screen":{"article_screen":"right", "rss_sub_screen":"right", "main_screen":"down"}
            }
        try:
            transition = d[start][end]
        except:
            transition = 'up'
        return transition
def generate_random_article(number_of_articles):
    random_array = np.random.randint(0,1000,[number_of_articles,4])
    
    article_list = np.array([Article(f'title{num[0]};authors{num[1]};date_of_publication{num[2]};source{num[3]}') for num in random_array])
    
    return article_list

if __name__ == '__main__':
    Window.size = (1000, 500)
    links_path = "storage/RSS link.txt"
    articles_path = "storage/article_list.json"
    MainApp(articles_path=articles_path, links_path=links_path).run()


