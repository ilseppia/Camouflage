import os
import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.image import Image


Builder.load_file('camouflage.kv')


class Camouf(Image):
    def __init__(self, **kwargs):
        super(Image, self).__init__(**kwargs)
    
class Body(Camouf):
    def __init__(self, **kwargs):
        self.size_hint= 300/800., 300/600.
        self.pos= (360,150)    
        self.source= 'camouf_body_01.png'
        super(Camouf, self).__init__(**kwargs)

class Hair(Camouf):
    def __init__(self, **kwargs):
        self.size_hint= 300/800., 150/600.
        self.pos= (360,150)    
        self.source= 'camouf_hair_01.png'
        super(Camouf, self).__init__(**kwargs)          
        
class Eyes(Camouf):
    def __init__(self, **kwargs):
        self.size_hint= 180/800., 60/600.
        self.pos= (415,215)    
        self.source= 'camouf_eyes_01.png'
        super(Camouf, self).__init__(**kwargs)  

class Nose(Camouf):
    def __init__(self, **kwargs):
        self.size_hint= 180/800., 40/600.
        self.pos= (415,235)    
        self.source= 'camouf_nose_01.png'
        super(Camouf, self).__init__(**kwargs)          

class Mouth(Camouf):
    def __init__(self, **kwargs):
        self.size_hint= 180/800., 40/600.
        self.pos= (415,265)    
        self.source= 'camouf_mouth_01.png'
        super(Camouf, self).__init__(**kwargs)  
        
class GameLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(GameLayout, self).__init__(**kwargs)   

        self.inventory = {}
        self.inventory['body']=[f for f in os.listdir('.') if f.startswith('camouf_body')]
        self.inventory['hair']=[f for f in os.listdir('.') if f.startswith('camouf_hair')]
        self.inventory['eyes']=[f for f in os.listdir('.') if f.startswith('camouf_eyes')]
        self.inventory['nose']=[f for f in os.listdir('.') if f.startswith('camouf_nose')]
        self.inventory['mouth']=[f for f in os.listdir('.') if f.startswith('camouf_mouth')]
        print self.inventory
        self.equipment = {'body':0, 'hair':0, 'eyes':0, 'nose':0, 'mouth':0}
        
    def update(self, dt):
        pass  
    
    def add_camouf(self, type, value):
        self.inventory[type].append(value)

    def change_camouf(self, type):
        self.equipment[type] = (self.equipment[type]+1)%len(self.inventory[type])
        if type=='body':
            self.ids.body.source=self.inventory['body'][self.equipment['body']]
        elif type=='hair':
            self.ids.hair.source=self.inventory['hair'][self.equipment['hair']] 
        elif type=='eyes':
            self.ids.eyes.source=self.inventory['eyes'][self.equipment['eyes']]   
        elif type=='nose':
            self.ids.nose.source=self.inventory['nose'][self.equipment['nose']]
        elif type=='mouth':
            self.ids.mouth.source=self.inventory['mouth'][self.equipment['mouth']]            
        
class CamouflageApp(App):
    def build(self):
        self.icon = ''
        self.title = 'Camouflage'    
        game = GameLayout()    

       
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

        
if __name__ in ('__main__', '__android__'):
    CamouflageApp().run() 
    
    
    
