# -*- coding: utf-8 -*-
"""
Created on Tue May  3 20:19:07 2022

@author: Arthur
"""

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

import numpy as np
from rss_reader import get_information, Article
from kivy.uix.scrollview import ScrollView




class MainMenu(GridLayout):

    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        
        
        self.cols = 3
        article_button = Button(text='Article Review')
        article_sub = Button(text='RSS Subscribe')
        article_filter = Button(text='Filters')
        
        self.add_widget(article_button)
        self.add_widget(article_sub)
        self.add_widget(article_filter)
        
        article_button.bind(on_press=self.change_screen)
        
        
    def change_screen(self, obj):
        sm.current = 'article_screen'
    


class MainScreen(Screen):
    pass
class ArticleScreen(Screen):
    
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

class RssSubScreen(Screen):
    pass
class FilterScreen(Screen):
    pass

class Article_grid_layout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.size_hint = (1,None)
        # self.height = len(article_layout_list)*50
    
    def add_article_layout(self,article_layout_list):
        # self.height = len(article_layout_list)
        # self.rows = len(article_layout_list)
        # self.ids['0'] = article_layout_list[0]
        # self.ids['1'] =article_layout_list[1]

        self.add_widget(article_layout_list[0])
        self.add_widget(article_layout_list[1])        
        # self.add_widget(article_layout_list[2])
        # self.add_widget(article_layout_list[3])
        # self.add_widget(article_layout_list[4])        
        # self.add_widget(article_layout_list[5])
        
        # print(article_layout_list[0].id, article_layout_list[1].id)
        # for article_layout in article_layout_list:
        #     self.add_widget(article_layout)
            
class Article_layout(FloatLayout):
    def __init__(self, article_str, **kwargs):
        super().__init__(**kwargs)
        self.size_hint= (1,None)
        article_list = article_str.split(';')
        article_title = Label(text=article_list[0], size_hint=(0.5, 0.4), pos_hint={'x':0.0, 'top':1})
        # article_title.background_color = (0, 0, 1, 0.25)
        self.add_widget(article_title)
        article_authors = Label(text=article_list[1],size_hint=(.5, .3),pos_hint={'x':0.0, 'y':0.3})
        self.add_widget(article_authors)
        article_dop = Label(text=article_list[2],size_hint=(.5, .3),pos_hint={'x':0.0, 'y':0.0})
        self.add_widget(article_dop)
        article_source = Label(text=article_list[3],size_hint=(.5, .3),pos_hint={'right':1, 'top':1})
        self.add_widget(article_source)
        article_link = Button(text="Lien de l'article",size_hint=(.3, .3),pos_hint={'right':1, 'y':0})
        self.add_widget(article_link)

    
class testApp(App):
    def build(self):
        return Article_layout('article;authors;dop;source')

    
class MainApp(App):

    def build(self):
        # Create the manager
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main_screen"))
        sm.add_widget(ArticleScreen(name="article_screen"))
        sm.add_widget(RssSubScreen(name="rss_sub_screen"))
        sm.add_widget(FilterScreen(name="filters_screen"))
        return sm
    
    def update_article_scrollview(self):
        layout = GridLayout(cols=1, spacing=1, size_hint=(None, None))
        layout.bind(minimum_height=layout.setter('height'),
                     minimum_width=layout.setter('width'))
        for i in range(40):
            btn = Button(text=str(i), size_hint=(None, None),
                         size=(200, 100))
            layout.add_widget(btn)
        scrollview = ScrollView(scroll_type=['bars'],
                                 bar_width='9dp',
                                 scroll_wheel_distance=100)
        scrollview.add_widget(layout)
        root.add_widget(scrollview)

        
def generate_random_article(number_of_articles):
    random_array = np.random.randint(0,1000,[number_of_articles,4])
    
    article_list = np.array([Article(f'title{num[0]}', f'authors{num[1]}', f'date_of_publication{num[2]}', f'source{num[3]}') for num in random_array])
    
    return article_list

if __name__ == '__main__':
    Window.size = (1000, 500)
    Builder.load_file('RSS_kivy.kv')
    MainApp().run()


