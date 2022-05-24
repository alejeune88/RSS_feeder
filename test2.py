# -*- coding: utf-8 -*-
"""
Created on Sat May 14 10:24:41 2022

@author: Arthur
"""

from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder

class EndEventScroll(ScrollView):

    def on_scroll_stop(self, *args, **kwargs):
        result = super(EndEventScroll, self).on_scroll_stop(*args, **kwargs)

        if self.scroll_y < 0 and hasattr(self, 'on_end_event'):
            self.on_end_event()
        return result


if __name__ == '__main__':
    from kivy.app import App

    from kivy.uix.gridlayout import GridLayout
    from kivy.uix.button import Button
    from kivy.properties import ObjectProperty
    from kivy.uix.label import Label
    from kivy.uix.floatlayout import FloatLayout
    
    class Article_layout(FloatLayout):
        def __init__(self, article_str, **kwargs):
            super().__init__(**kwargs)
            self.size= (1,1)
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
        
    class CustomScrollView(EndEventScroll):

        layout1 = ObjectProperty(None)

        def on_end_event(self):
            height = 0.0

            for i in range(40):
                btn = Button(text=str(i), size_hint=(None, None),
                             size=(200, 100))
                self.layout1.add_widget(btn)
                height += btn.height
            height = float(height / self.layout1.cols)
            procent = (100.0 * height)/float(self.layout1.height)
            self.scroll_y += procent/100.0


    class ScrollViewApp(App):

        def build(self):
            article_layout_list = self.get_article_layout()
            layout2 = GridLayout(cols=1, spacing=10, size=(250, 300))
            # layout2.bind(minimum_height=layout2.setter('height'),
            #              minimum_width=layout2.setter('width'))
            for i, article_layout in enumerate(article_layout_list[:4]):
                
                btn = Button(text=str(i), size_hint=(None, None),
                              size=(200, 100))
                # layout2.add_widget(article_layout)
            scrollview2 = ScrollView(scroll_type=['bars'],
                                     bar_width='9dp',
                                     scroll_wheel_distance=100,
                                     size= (300,500))
            scrollview2.add_widget(layout2)
            
            return scrollview2
        
        def get_article_list(self):
            article_list_path = 'article_list.txt'
            with open(article_list_path,'r') as f:
                article_list = f.readlines()
            return article_list
    
        def get_article_layout(self):
            article_list = self.get_article_list()
            article_layout_list = [Article_layout(article_str, size=(200,100)) for i, article_str in enumerate(article_list)]
            return article_layout_list
    
    Builder.load_file('test2.kv')
    ScrollViewApp().run()