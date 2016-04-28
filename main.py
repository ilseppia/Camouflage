import os, random
import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.vector import Vector
from kivy.clock import Clock


Builder.load_file('camouflage.kv')


class Camouf(RelativeLayout):
    def __init__(self, values=[1]*5, **kwargs):
        super(Camouf, self).__init__(**kwargs)   
        
        self.body=Image(size_hint=(1, 1), pos_hint=({'center_x': 0.5, 'y': 0}), source='camouf_body_{0:02d}.png'.format(values['body']))
        self.add_widget(self.body)

        self.hair=Image(size_hint=(1, 0.5), pos_hint=({'center_x': 0.5, 'y': 0.5}), source='camouf_hair_{0:02d}.png'.format(values['hair']))
        self.add_widget(self.hair)

        self.eyes=Image(size_hint=(180/300., 60/300.), pos_hint=({'center_x': 0.5, 'y': 0.62}), source='camouf_eyes_{0:02d}.png'.format(values['eyes']))
        self.add_widget(self.eyes)

        self.nose=Image(size_hint=(180/300., 40/300.), pos_hint=({'center_x': 0.5, 'y': 0.58}), source='camouf_nose_{0:02d}.png'.format(values['nose']))
        self.add_widget(self.nose)

        self.mouth=Image(size_hint=(180/300., 40/300.), pos_hint=({'center_x': 0.5, 'y': 0.48}), source='camouf_mouth_{0:02d}.png'.format(values['mouth']))
        self.add_widget(self.mouth)        

       

        
#class Button_Camouf(ButtonBehavior, Image):
class Button_Camouf(Image):
    def __init__(self, text, **kwargs):
        self.text=text
        super(Button_Camouf, self).__init__(**kwargs)
        
        
    def on_touch_down(self, touch):
        #if self.collide_point(*touch.pos):
        if Vector(self.center).distance(touch.pos) <= self.height/2:
            self.parent.change_camouf(self.text)
            self.source='button_red.png' if self.parent.dangerous[self.text]==self.parent.equipment[self.text]+1 else 'button_green.png'
            return True
        return False

class Identikit():
    def __init__(self, inventory, **kwargs):
        self.inventory=inventory
        
            
        
class GameLayout(RelativeLayout):
    def __init__(self, **kwargs):

        super(GameLayout, self).__init__(**kwargs)   


        self.inventory = {}
        self.inventory['body']=[f for f in os.listdir('.') if f.startswith('camouf_body')]
        self.inventory['hair']=[f for f in os.listdir('.') if f.startswith('camouf_hair')]
        self.inventory['eyes']=[f for f in os.listdir('.') if f.startswith('camouf_eyes')]
        self.inventory['nose']=[f for f in os.listdir('.') if f.startswith('camouf_nose')]
        self.inventory['mouth']=[f for f in os.listdir('.') if f.startswith('camouf_mouth')]
        #print self.inventory
        self.equipment = {'body':1, 'hair':1, 'eyes':1, 'nose':1, 'mouth':1}
        self.equipment = {k:random.randrange(1,5) for k in self.equipment.keys()}
        
        self.camouf = Camouf(size_hint=(300/800., 300/600.), pos_hint=({'x':360/800., 'y':150/600.}), values=self.equipment)
        self.add_widget(self.camouf)

        self.add_widget(Image(source='screen_border_front.png'))

        self.dangerous={k:random.randrange(1,5) for k in self.equipment.keys()}
        self.identikit=Camouf(size_hint=(150/800., 150/600.), pos_hint=({'right':1, 'y':0}), values=self.dangerous)
        self.add_widget(self.identikit)
        
        button_positions={'body':(0.5,0.4), 'hair':(0.7,0.65), 'eyes':(0.72,0.59), 'nose':(0.72,0.52), 'mouth':(0.7,0.46)}
        for key, val in button_positions.iteritems():
            button_color='button_red.png' if self.dangerous[key]==self.equipment[key] else 'button_green.png'
            self.add_widget(Button_Camouf(size_hint=(0.05, 0.05), pos_hint={'x':val[0], 'y':val[1]}, text=key, source=button_color))
        

        
    def update(self, dt):
        pass  
    
    def add_camouf(self, type, value):
        self.inventory[type].append(value)

    def change_camouf(self, type):
        self.equipment[type] = (self.equipment[type]+1)%len(self.inventory[type])
        self.camouf.__dict__[type].source=self.inventory[type][self.equipment[type]]


        
class CamouflageApp(App):
    def build(self):
        self.icon = ''
        self.title = 'Camouflage'    
        game = GameLayout()    
        print game.size

       
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

        
if __name__ in ('__main__', '__android__'):
    CamouflageApp().run() 
    
    
    
