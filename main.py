import os, random, sys
import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
from kivy.core import audio
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
from kivy.properties import BooleanProperty, NumericProperty
from kivy.vector import Vector
from kivy.clock import Clock

from identikit import Identikit
from inventory import Inventory
import scenes


Builder.load_file('camouflage.kv')




class SceneManager(ScreenManager):
    def __init__(self, source='', **kwargs):
        super(SceneManager, self).__init__(**kwargs)
        self.inventory = Inventory()

        
class CamouflageApp(App):
    def build(self):
        self.icon = ''
        self.title = 'Camouflage'
        
        
        self.game=FloatLayout()
        
        self.scene_manager = SceneManager(transition=FadeTransition())        
        
        self.debug_menu=GridLayout(rows=1, pos_hint={'top':1,'right':1./6}, size_hint_y=0.1)
        for text in ('logo','car','cockpit','mex','usa','debug'):
            but=Button(text=text)
            but.bind(on_release=lambda but: self.debug_clicked(but.text))
            self.debug_menu.add_widget(but)
        
        self.game.add_widget(self.scene_manager)
        self.game.add_widget(self.debug_menu)
        
        return self.game
        
    
    def on_start(self):
        print 'app on_start', self.root_window.size
        
        #game is supposed to be 4:3 ratio
        if self.root_window.width>=self.root_window.height*4/3:
            min_size=[self.root_window.height*4/3, self.root_window.height]
        else:
            min_size=[self.root_window.width, self.root_window.width*3/4]        
        #save debug menu position
        
        self.numof_intro_drawings=6
        self.next_country='mex'
        self.scene_manager.add_widget(scenes.LogoScene(size=(min_size)))
        self.scene_manager.add_widget(scenes.IntroScene(min_size, self.numof_intro_drawings, self.next_country))
        self.scene_manager.add_widget(scenes.MexScene(min_size, self.scene_manager.inventory))
        self.scene_manager.add_widget(scenes.UsaScene(min_size, self.scene_manager.inventory))
        self.scene_manager.add_widget(scenes.CarScene(min_size))
        self.scene_manager.add_widget(scenes.Cockpit(min_size, self.scene_manager.inventory, self.next_country))
        self.scene_manager.current='logo'
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        
        
    def update(self, arg):
        self.scene_manager.current_screen.update()

    def debug_clicked(self, name):
        if name=='debug':
            if self.debug_menu.x<0:
                self.debug_menu_x=self.debug_menu.x
                self.debug_menu.pos_hint={'top':1}

                anim = Animation(x=0, duration=.5)
                anim.start(self.debug_menu)
                return
        else:
            #self.scene_manager.current_screen.pause_on()
            self.scene_manager.current=name
            #self.scene_manager.current_screen.pause_off()        

        anim = Animation(x=self.debug_menu_x, duration=.5)
        anim.start(self.debug_menu)
            


        
if __name__ in ('__main__', '__android__'):
    CamouflageApp().run() 
    
#nexus --size=1776x1080    
    
