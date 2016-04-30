import os, random
import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.button import Button
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
from kivy.properties import BooleanProperty, NumericProperty
from kivy.vector import Vector
from kivy.clock import Clock


Builder.load_file('camouflage.kv')


class Camouf(RelativeLayout):
    def __init__(self, values=[1]*5, **kwargs):
        super(Camouf, self).__init__(**kwargs)   
        
        self.body=Image(size_hint=(1, 1), pos_hint=({'center_x': 0.5, 'y': 0}), source=os.path.join('data','camouf_body_{0:02d}.png'.format(values['body'])))
        self.add_widget(self.body)

        self.hair=Image(size_hint=(1, 0.5), pos_hint=({'center_x': 0.5, 'y': 0.5}), source=os.path.join('data','camouf_hair_{0:02d}.png'.format(values['hair'])))
        self.add_widget(self.hair)

        self.eyes=Image(size_hint=(180/300., 60/300.), pos_hint=({'center_x': 0.5, 'y': 0.62}), source=os.path.join('data','camouf_eyes_{0:02d}.png'.format(values['eyes'])))
        self.add_widget(self.eyes)

        self.nose=Image(size_hint=(180/300., 40/300.), pos_hint=({'center_x': 0.5, 'y': 0.58}), source=os.path.join('data','camouf_nose_{0:02d}.png'.format(values['nose'])))
        self.add_widget(self.nose)

        self.mouth=Image(size_hint=(180/300., 40/300.), pos_hint=({'center_x': 0.5, 'y': 0.48}), source=os.path.join('data','camouf_mouth_{0:02d}.png'.format(values['mouth'])))
        self.add_widget(self.mouth)        

       

        
#class Button_Camouf(ButtonBehavior, Image):
class Button_Camouf(Image):
    def __init__(self, text, **kwargs):
        self.text=text
        super(Button_Camouf, self).__init__(**kwargs)
        
        
    def on_touch_down(self, touch):
        #if self.collide_point(*touch.pos):
        if Vector(self.center).distance(touch.pos) <= self.height/2:
            self.parent.parent.change_camouf(self.text)
            self.source=os.path.join('data','button_red.png') if self.parent.parent.dangerous[self.text]==self.parent.parent.equipment[self.text]+1 else os.path.join('data','button_green.png')
            print 'button {}'.format(self.text)
            return True
        return False

class Identikit():
    def __init__(self, inventory, **kwargs):
        self.inventory=inventory
        
            
        
class CheckScene(ScatterLayout):
    pause = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(CheckScene, self).__init__(do_rotation=False, do_scale=False, do_translation=False, **kwargs)   
        self.next=next
        self.inventory = {}
        self.inventory['body']=[f for f in os.listdir('data') if f.startswith('camouf_body')]
        self.inventory['hair']=[f for f in os.listdir('data') if f.startswith('camouf_hair')]
        self.inventory['eyes']=[f for f in os.listdir('data') if f.startswith('camouf_eyes')]
        self.inventory['nose']=[f for f in os.listdir('data') if f.startswith('camouf_nose')]
        self.inventory['mouth']=[f for f in os.listdir('data') if f.startswith('camouf_mouth')]
        #print self.inventory
        self.equipment = {'body':1, 'hair':1, 'eyes':1, 'nose':1, 'mouth':1}
        self.equipment = {k:random.randrange(1,5) for k in self.equipment.keys()}
        self.dangerous={k:random.randrange(1,5) for k in self.equipment.keys()}

        
        #draw cockpit backside
        self.add_widget(Image(source=os.path.join('data','screen_car_back.png')))        
        #draw character
        self.camouf = Camouf(size_hint=(300/800., 300/600.), pos_hint=({'x':360/800., 'y':150/600.}), values=self.equipment)
        self.add_widget(self.camouf)
        #draw cockpit front
        self.add_widget(Image(source=os.path.join('data','screen_car_front.png')))
        #draw policeman
        self.policeman=Image(source=os.path.join('data','policeman.png'), size_hint=(250/800., 600/600.), pos_hint=({'x':1.1, 'y':-0.1}))
        self.add_widget(self.policeman)
        #draw identikit
        self.identikit=Camouf(size_hint=(150/800., 150/600.), pos_hint=({'x':1.1, 'y':0.3}), values=self.dangerous)
        self.add_widget(self.identikit)
        
        
        button_positions={'body':(0.5,0.4), 'hair':(0.7,0.65), 'eyes':(0.72,0.59), 'nose':(0.72,0.52), 'mouth':(0.7,0.46)}
        for key, val in button_positions.iteritems():
            button_color=os.path.join('data','button_red.png') if self.dangerous[key]==self.equipment[key] else os.path.join('data','button_green.png')
            self.add_widget(Button_Camouf(size_hint=(0.05, 0.05), pos_hint={'x':val[0], 'y':val[1]}, text=key, source=button_color))


    def on_pause(self, instance, value):
        print self.pause
        
    def update(self, dt):
        pass  
    
    def add_camouf(self, type, value):
        self.inventory[type].append(value)

    def change_camouf(self, type):
        self.equipment[type] = (self.equipment[type]+1)%len(self.inventory[type])
        self.camouf.__dict__[type].source=os.path.join('data',self.inventory[type][self.equipment[type]])
        #self._set_scale(1.2)
        
class LogoScene(Screen):
    def __init__(self, next, source, **kwargs):
        super(LogoScene, self).__init__(**kwargs)    
        self.next=next
        self.add_widget(Image(source=os.path.join('data',source)))
    
    def on_touch_down(self, touch):
        self.parent.current=self.next
        return True     
        
class CarScene(Screen):
    def __init__(self, next, source, **kwargs):
        super(CarScene, self).__init__(**kwargs)    
        self.next=next
        self.add_widget(Image(source=os.path.join('data',source)))
        self.sound = SoundLoader.load(os.path.join('data','vehicle_01.wav'))
        self.sound.bind(on_stop=self.next_scene) 

    def on_pre_enter(self):
        self.sound.play() 
        
    def on_touch_down(self, touch):
        if self.sound.state=='play':
            self.sound.stop()
        return True

    def next_scene(self, value):
        self.parent.current=self.next

        
class BoundaryScene(Screen):
    seconds = NumericProperty(3)
    def __init__(self, next, source='', **kwargs):
        self.next=next
        super(BoundaryScene, self).__init__(**kwargs)    
        self.cockpit=CheckScene()
        self.add_widget(self.cockpit)
        self.sound = SoundLoader.load(os.path.join('data','hello_01.wav'))
        self.go_button=Button(size_hint=(50/800., 50/600.), pos_hint={'x':0.5, 'y':0.5}, text='GO')
              
    
    def on_secconds(self):
        self.go_buttontext=str(self.seconds)  
    
    def on_enter(self):
        policeman_anim=Animation(pos_hint={'x':0.8, 'y':0}) 
        policeman_anim.start(self.cockpit.policeman)
        policeman_anim.bind(on_complete=self.check_identikit)
    
    def check_identikit(self, anim, value):
        self.sound.play()
        identity_anim=Animation(pos_hint={'x':0.85, 'y':0.5}) 
        identity_anim.start(self.cockpit.identikit)
        identity_anim.bind(on_complete=self.zoom_to_cockipt)
        
    def zoom_to_cockipt(self, anim, value):
        car_zoom = Animation(scale=1, d=1)+Animation(scale=1.5, d=2)
        car_zoom.start(self.cockpit)
        car_zoom.bind(on_complete=self.camouf_you)
        
    def camouf_you(self, anim, value):
        self.add_widget(self.go_button)
    
    def on_touch_down(self, touch):
        if self.go_button.collide_point(*touch.pos):
            print 'OK'
            return True

class SceneManager(ScreenManager):
    def __init__(self, source='', **kwargs):
        super(SceneManager, self).__init__(**kwargs)


        
class CamouflageApp(App):
    def build(self):
        self.icon = ''
        self.title = 'Camouflage'
        '''
        game = CheckScene()    
        game.bind(pause=game.on_pause) 

       
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game
        '''
        
        self.scene_manager = SceneManager(transition=FadeTransition())
       
        self.scene_manager.add_widget(LogoScene(name='logo', next='boundary', source='screen_forkedtaillogo.png'))
        self.scene_manager.add_widget(CarScene(name='boundary', next='car', source='screen_border_01.png'))
        self.scene_manager.add_widget(BoundaryScene(name='car', next='logo', source='screen_car_back.png'))
        
        return self.scene_manager
    
    def change_scene(self, name):
        self.scene_manager.current_screen.pause_on()
        self.scene_manager.current=name
        self.scene_manager.current_screen.pause_off()

        
if __name__ in ('__main__', '__android__'):
    CamouflageApp().run() 
    
    
    
