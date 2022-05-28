# -*- coding: utf-8 -*-
"""
Created on Fri May 13 22:29:31 2022

@author: Arthur
"""
import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from functools import partial

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
kv = '''
BoxLayout:
    orientation: 'vertical'
    Button:
        text: 'add'
        on_release: app.add_new_widget()
    ScrollView:
        id: scroll
        BoxLayout:
            id: box
            spacing:10
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
'''

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
        
class TestApp(App):
    def build(self):
        self.count = 0
        return Builder.load_string(kv)

    def add_new_widget(self):
        vp_height = self.root.ids.scroll.viewport_size[1]
        sv_height = self.root.ids.scroll.height

        # add a new widget (must have preset height)
        label = Label(text='Widget #' + str(self.count), size_hint=(1, None), height=50)
        article_layour = Article_layout(article_str='article;authors;dop;source'+ str(self.count), size_hint=(1, None), height=100)
        self.root.ids.box.add_widget(article_layour)
        self.count += 1

        if vp_height > sv_height:  # otherwise there is no scrolling
            # calculate y value of bottom of scrollview in the viewport
            scroll = self.root.ids.scroll.scroll_y
            bottom = scroll * (vp_height - sv_height)

            # use Clock.schedule_once because we need updated viewport height
            # this assumes that new widgets are added at the bottom
            # so the current bottom must increase by the widget height to maintain position
            Clock.schedule_once(partial(self.adjust_scroll, bottom+label.height), -1)

    def adjust_scroll(self, bottom, dt):
        vp_height = self.root.ids.scroll.viewport_size[1]
        sv_height = self.root.ids.scroll.height
        self.root.ids.scroll.scroll_y = bottom / (vp_height - sv_height)

TestApp().run()