from kivy.uix.relativelayout import RelativeLayout

class Identikit(RelativeLayout):
    def __init__(self, disguises, **kwargs):
        super(Identikit, self).__init__(**kwargs)
        self.disguises={}
        for d in disguises:
            self.disguises[d.type]=d
        
        for d in self.disguises.values():
            self.add_widget(d)
