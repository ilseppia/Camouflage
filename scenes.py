import os

from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.bubble import Bubble
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy.clock import Clock
from identikit import Identikit
from bubbleimage import BubbleImage
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from disguise import DisguiseLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import *
from kivy.properties import StringProperty
from kivy.effects.scroll import ScrollEffect
from kivy.animation import Animation
from kivy.properties import ObjectProperty

class GameScene(Screen):
    #generic scene (do not use)
    background = StringProperty('')    
    def __init__(self, size, **kwargs):
        super(GameScene, self).__init__(size_hint=(None,None), size=size, pos_hint={'center_x':0.5, 'center_y':0.5}, **kwargs)
        
    def on_enter(self):
        print 'scene enter {}'.format(self.name), self.size
    
    def on_pre_enter(self):
        print 'scene pre_enter {}'.format(self.name)    
    
    def go_next(self, arg):
        self.parent.current=self.next_scene
        
    def update(self):
        #print 'update',self
        pass

class LogoScene(GameScene):
    #splashscreen showing forked tail logo.
    #change scene by click/touch
    #TODO: if savefile is missing, show intro, otherwise load game from latest savefile (mexico or USA)
    def __init__(self, size, **kwargs):
        self.background = os.path.join('data','screen_forkedtaillogo.png')
        self.name='logo'
        self.next_scene='intro'        
        super(LogoScene, self).__init__(size, **kwargs) 

    def on_touch_down(self, touch):
        self.parent.current=self.next_scene      

class IntroScene(GameScene):
    #scene showing game plot
    #change scene by click/touch or TODO: after couple of seconds 

    def __init__(self, size, total_draws, country, **kwargs):
        self.total_draws=total_draws
        self.draw_no=1
        self.name='intro'
        self.next_scene=country
        self.background = os.path.join('data','screen_story_{0:02d}.jpg'.format(self.draw_no))
        super(IntroScene, self).__init__(size, **kwargs) 
        

    def on_touch_down(self, touch):
        print 'clicked',touch.pos
        if self.draw_no < self.total_draws:
            self.draw_no+=1
            self.background = os.path.join('data','screen_story_{0:02d}.jpg'.format(self.draw_no))
        else:
            self.parent.current=self.next_scene

class Map(RelativeLayout):
    def __init__(self, **kwargs):    
        self.background = os.path.join('data','map_mex.png')    
        super(Map, self).__init__(**kwargs)
        
 
class MexScene(GameScene):
    #scene showing city from Mexico
    #TODO: change scene by click/touch on shops/car
    scroll=ObjectProperty()
    
    def __init__(self, size, inventory, **kwargs):
        #self.background = os.path.join('data','map_mex.png')
        self.name='mex'
        self.next_scene='car'
        scroll_size=[3*size[0], size[1]]
        super(MexScene, self).__init__(size, **kwargs) 
        
        self.scrollview=ScrollView(size=scroll_size, effect_cls=ScrollEffect)
        #self.scrollview.scroll_x=0
        #self.scrollview.scroll_y=0.5
        self.map=Map(size_hint=(None, None),size=scroll_size)
        self.paco=Image(source=os.path.join('data','paco_walk.zip'), pos=(100,100), size_hint=(None,None), size=(100,170))
        self.map.add_widget(self.paco)        
        self.scrollview.add_widget(self.map)
        self.add_widget(self.scrollview)
        
        
    def on_touch_down(self, touch):
        #print touch.pos, self.map.to_widget(*touch.pos)
        self.walk = Animation(pos=self.map.to_widget(*touch.pos)) 
        self.walk.start(self.paco)
        #print touch.pos[0],(touch.pos[0]<200 or touch.pos[0]>600),self.map.to_widget(*touch.pos)[0], self.map.to_widget(*touch.pos)[0]>400 and self.map.to_window(*touch.pos)[0]<2000
        '''if (touch.pos[0]<200 or touch.pos[0]>600) \
        and self.map.to_widget(*touch.pos)[0]>400 and self.map.to_widget(*touch.pos)[0]<2000:
            self.scroll=Animation(scroll_x=self.map.to_widget(*touch.pos)[0]/2400)
            self.scroll.start(self.scrollview)
            self.scroll.bind(on_complete=self.stop_scroll)
        '''

        self.scroll=Animation(scroll_x=(int(self.map.to_widget(*touch.pos)[0]/(3*self.size[0]/100)) - int(self.map.to_widget(*touch.pos)[0]/(3*self.size[0]/100))%16)/100.)
        self.scroll.start(self.scrollview)
        self.scroll.bind(on_complete=self.stop_scroll)        
        #self.walk.bind(on_complete=self.stop_scroll)
        
    def update(self):
        #print self.paco.pos
        screen_width=800
        map_width=2400
        #<=400 --> 0
        #400<=2000 --> ?
        #<2000 --> 1

        '''
        if self.map.to_window(*self.paco.pos)[0]<200 and self.scrollview.scroll_x>0 and not self.scroll:
            self.scroll=Animation(scroll_x=0)
            self.scroll.start(self.scrollview)
            self.scroll.bind(on_complete=self.stop_scroll)
        elif self.map.to_window(*self.paco.pos)[0]>600 and self.scrollview.scroll_x<1 and not self.scroll:
            self.scroll=Animation(scroll_x=1)
            self.scroll.start(self.scrollview)
            self.scroll.bind(on_complete=self.stop_scroll)
        '''

    def stop_scroll(self, arg, val):
        pass
        #self.parent.current=self.next_scene
        
        
class UsaScene(GameScene):
    #scene showing city from USA
    #TODO: change scene by click/touch on shops/car
    def __init__(self, size, inventory, **kwargs):
        self.background = os.path.join('data','map_usa.png')
        self.name='usa'
        self.next_scene='car'
        super(UsaScene, self).__init__(size, **kwargs) 
    
    def on_touch_down(self, touch):
        self.parent.current=self.next_scene       

class CarScene(GameScene):
    #scene showing car approaching to the border
    #change scene by click/touch or after couple of seconds 
    
    def __init__(self, size, **kwargs):
        self.background=os.path.join('data','screen_border_01.png')
        self.name='car'
        self.next_scene='cockpit'
        super(CarScene, self).__init__(size, **kwargs) 
        self.sound = SoundLoader.load(os.path.join('data','vehicle_01.wav'))
        #change scene bind to sound stop.... to be changed
        #self.sound.bind(on_stop=self.go_next_scene) 

    def on_pre_enter(self):
        self.sound.play() 
        self.clock_go_next=Clock.schedule_once(self.go_next, 2.0)        
        pass
        
    def on_touch_down(self, touch):
        if self.sound.state=='play':
            self.sound.stop()
            Clock.unschedule(self.clock_go_next)
        self.parent.current=self.next_scene       
        


class Cockpit(GameScene):
    #scene where policeman checks your camuflage
    #policeman enters on the screen showing wanted picture, then scene zooms on cockpit allowing you to change camouflage
    #scene changes at click on 'complete' button, or after some seconds
    
    def __init__(self, size, inventory, country, **kwargs):
        self.background=os.path.join('data','screen_car_back.png')
        self.name='cockpit'
        self.next_scene=country
        self.inventory=inventory
        super(Cockpit, self).__init__(size, **kwargs)
        
        self.identikit_size=300.0
        #self.driver = Identikit(self.get_equipped(), pos_hint={'center_x':(200.+self.identikit_size/2)/800, 'center_y':(600.-150.-self.identikit_size/2)/600}, size_hint=(self.identikit_size/800,self.identikit_size/600))
        self.driver = Identikit(self.get_equipped(), pos_hint={'x':0.25, 'y':0.25}, size_hint=(self.identikit_size/800,self.identikit_size/600))
        self.add_widget(self.driver)        

        #draw cockpit front
        self.frontimage=Image(source=os.path.join('data','screen_car_front.png'), allow_stretch=True)
        self.add_widget(self.frontimage)
        
        #draw disguise buttons
        self.button_bar=DisguiseLayout(rows=1, cols_minimum={0:100, 1:250}, pos_hint={'x':0.25+self.identikit_size/800, 'center_y':0.5}, size_hint=(self.identikit_size/800, self.identikit_size/400))
        self.add_widget(self.button_bar)

        #draw go button
        go_button=Button(text='GO!', pos_hint={'x':0.4, 'y':0.1}, size_hint=(0.2,0.15))
        go_button.bind(on_release=self.go_next)
        self.add_widget(go_button)

        

        
        #draw policeman
        #self.policeman=Image(source=os.path.join('data','policeman.png'), size_hint=(250/800., 600/600.), pos_hint=({'x':1.1, 'y':-0.1}))
        #self.add_widget(self.policeman)
        #draw identikit
        #self.identikit=Identikit(equipment=self.parent.dangerous, size_hint=(150/800., 150/600.), pos_hint=({'x':1.1, 'y':0.3}))
        #self.add_widget(self.identikit)        
        
        #self.sound = SoundLoader.load(os.path.join('data','hello_01.wav'))
        #self.go_button=Button(size_hint=(50/800., 50/600.), pos_hint={'x':0.5, 'y':0.5}, text='GO')
    

    
    def get_equipped(self):
        #return list of equipped camouflage
        return self.inventory.get_equipped()
        
    def get_risky(self):
        #return list of equipped camouflage
        risky = {}
        for inv_type,inv_value in self.inventory.items():
            risky[inv_type]=[key for key,value in inv_value.items() if value[1]=='1'][0]
        return risky        
        

    
    def on_pre_enter(self):
        print 'scene pre_enter', self.size
        #policeman_anim=Animation(pos_hint={'x':0.8, 'y':0}) 
        #policeman_anim.start(self.cockpit.policeman)
        #policeman_anim.bind(on_complete=self.check_identikit)
    
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
    
    def on_touch_downz(self, touch):
        print 'touch',self, self.pos, self.size, self.children
        for c in self.children:
            if c.collide_point(*self.to_local(*touch.pos)):
                c.on_touch_down(touch)

        #return super(Cockpit, self).on_touch_down(touch)
        #return True

   