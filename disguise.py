from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.effects.scroll import ScrollEffect
import os
from kivy.lang import Builder

Builder.load_string('''
<DisguiseLayoutz>:
    canvas:
        Color:
            rgba: 1, 0, 0, 0.2
        Rectangle:
            size: self.size
            pos: self.pos

<ScrollViewz>:
    canvas:
        Color:
            rgba: 0, 1, 0, 0.5
        Rectangle:
            size: self.size
            pos: self.pos               
            
<GridLayoutz>:
    canvas:
        Color:
            rgba: 0, 0, 1, 0.2
        Rectangle:
            size: self.size
            pos: self.pos                  


<DisguiseButtonz>:
    canvas:
        Color:
            rgba: 0, 0, 0, 0.1
        Rectangle:
            size: self.size
            pos: self.pos
            
<DisguiseTypeButton>:
    Image:
        source: self.parent.source
        center_x: self.parent.center_x 
        center_y: self.parent.center_y
        allow_stretch: True        
            ''')
            
            


class DisguiseTypeButton(Button):        
    def __init__(self, typ, source, **kwargs):
        self.typ = typ
        self.name = None
        self.source=source
    
        super(DisguiseTypeButton, self).__init__(**kwargs)

        
class DisguiseButton(Button):
    def __init__(self, typ, name, **kwargs):
        super(DisguiseButton, self).__init__(**kwargs)
        self.typ = typ  
        self.name = name
            
class DisguiseLayout(GridLayout):
    def __init__(self, **kwargs):
        super(DisguiseLayout, self).__init__(**kwargs)
        self.disguise_size={'hair':(200,100),'eyes':(200,67),'nose':(200,44),'mouth':(200,44),'body':(200,200)}

        self.left_panel = GridLayout(cols=1, pos_hint=({'center_x':0.5, 'center_y':0.5}))
        self.right_panel = ScrollView(effect_cls=ScrollEffect)
        
        for id, typ in enumerate(self.disguise_size.keys()):
            but=DisguiseTypeButton(typ=typ, source=os.path.join('data','but_{}.png'.format(typ)))#, size_hint=(1,0.3))#, size=(50,50), pos_hint={'x':0, 'center_y':0.3+0.1*id})
            but.bind(on_release=self.show_hide_list)
            self.left_panel.add_widget(but)  
        
        self.add_widget(self.left_panel)  
        self.add_widget(self.right_panel)  

        #self.disguise_size={'hair':(200,100),'eyes':(200,67),'nose':(200,44),'mouth':(200,44),'body':(200,200)}
        self.disguise_size={'hair':(300,150),'eyes':(300,100),'nose':(300,67),'mouth':(300,67),'body':(300,300)}
        
        self.scroll_views={}
        self.max_texture_size=0
        for typ,siz in self.disguise_size.items():
            gridlayout = GridLayout(cols=1, spacing=10, padding=10, size_hint=(1,None))
            gridlayout.bind(minimum_height=gridlayout.setter('height'))
            
            for filename in os.listdir('data'):
                if filename.startswith('id_{}'.format(typ)):
                    id_trash, type_trash, name = filename.split('_')
                    name=name.replace('.png','')
                    btn = DisguiseButton(typ=typ, name=name, size_hint=(None, None), size=siz, background_normal=os.path.join('data',filename))
                    btn.bind(on_release=self.pick_from_list)
                    gridlayout.add_widget(btn)

                    img_size = Image(source=os.path.join('data',filename)).texture_size
                    if img_size > self.max_texture_size:
                        self.max_texture_size = img_size 
            
            self.scroll_views[typ] = ScrollView(effect_cls=ScrollEffect)
            self.scroll_views[typ].add_widget(gridlayout) 
            gridlayout.bind(minimum_width=self.scroll_views[typ].setter('width'))


    
        
    def show_hide_list(self, button):
        if self.scroll_views[button.typ] in self.right_panel.children:
            self.right_panel.remove_widget(self.scroll_views[button.typ])
        else:
            for child in self.right_panel.children:
                if child.__class__.__name__ == 'ScrollView':
                    self.right_panel.remove_widget(child)   
            self.right_panel.add_widget(self.scroll_views[button.typ])                        

                                  
                    
    def pick_from_list(self, button):    
        if button.typ and button.name != None:
            self.parent.driver.disguises[button.typ].source = button.background_normal
            self.right_panel.remove_widget(self.scroll_views[button.typ])    
        


            
            