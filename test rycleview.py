# -*- coding: utf-8 -*-
"""
Created on Sun May 29 21:34:58 2022

@author: ArthurAdmin
"""
import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout

Builder.load_string('''
<StatefulLabel>:
    active: stored_state.active
    CheckBox:
        id: stored_state
        active: root.active
        on_release: root.store_checkbox_state()
    Label:
        text: root.text
    Label:
        id: generate_state
        text: root.generated_state_text

<RV>:
    viewclass: 'Article_layout'
    RecycleBoxLayout:
        size_hint_y: None
        size_hint_x: 1
        height: self.minimum_height
        orientation: 'vertical'

<Article_layout>:
    id: article_layout + root.index
    size_hint: 1, None
    height: 100
    
    # canvas.before:
    #     Color:
    #         rgba : Article_color
    #     Rectangle:
    #         pos: self.pos
    #         size: self.size
    
    ToggleButton:
        id: number
        text: root.index
        # background_color: {'normal': Button_color, 'down': article_selected_color} [self.state]
        size_hint: (0.1, 1)
        pos_hint: {'x':0, 'y':0}
        halign: "center"
        valign: "center"
        on_state:
            app.select_article(root.index)

    Label:
        id: title
        text: root.title
        size_hint: (0.5, 0.4)
        pos_hint: {'x':0.11, 'top':1}
        text_size: self.size
        halign: "left"
        valign: "center"

    Label:
        id: author
        text: root.authors
        size_hint: (0.5, 0.4)
        pos_hint: {'x':0.11, 'y':0.3}
        text_size: self.size
        halign: "left"
        valign: "center"

    Label:
        id: dop
        text: root.date_of_publication
        size_hint: (0.5, 0.4)
        pos_hint: {'x':0.11, 'y':0}
        text_size: self.size
        halign: "left"
        valign: "center"

    Label:
        id: source
        text: root.source
        size_hint: (0.5, 0.4)
        pos_hint: {'right':0.99, 'top':1}
        text_size: self.size
        halign: "right"
        valign: "center"

    Button:
        id: link
        text: "article link"
        font_size: 20
        size_hint: (0.2, 0.3)
        pos_hint: {'right':0.99, 'y':0.01}
        on_press:
            app.open_link(root.link)
''')

class StatefulLabel(RecycleDataViewBehavior, BoxLayout):
    text = StringProperty()
    generated_state_text = StringProperty()
    active = BooleanProperty()
    index = 0

    '''
    To change a viewclass' state as the data assigned to it changes,
    overload the refresh_view_attrs function (inherited from
    RecycleDataViewBehavior)
    '''
    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        if data['text'] == '0':
            self.generated_state_text = "is zero"
        elif int(data['text']) % 2 == 1:
            self.generated_state_text = "is odd"
        else:
            self.generated_state_text = "is even"
        super(StatefulLabel, self).refresh_view_attrs(rv, index, data)

    '''
    To keep state changes in the viewclass with associated data,
    they can be explicitly stored in the RecycleView's data object
    '''
    def store_checkbox_state(self):
        rv = App.get_running_app().rv
        rv.data[self.index]['active'] = self.active
        
class Article_layout(RecycleDataViewBehavior, FloatLayout):
    index = StringProperty()
    title = StringProperty()
    authors = StringProperty()
    date_of_publication = StringProperty()
    source = StringProperty()
    link = StringProperty()
    
    def set_index(self, new_index):
        index = str(new_index)
        
class RV(RecycleView, App):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'index': str(x), 'title': str(x),'authors': str(x),\
                      'date_of_publication': str(x),'source': str(x),'link': str(x)} for x in range(100)]
        App.get_running_app().rv = self

    def build(self):
        return self

if __name__ == '__main__':
    RV().run()