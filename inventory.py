from kivy.uix.image import Image
import os


class Inventory():
    def __init__(self, inventory=[], **kwargs):
        self.inventory=inventory
        
        for filename in os.listdir('data'):
            if filename.startswith('id_'):
                id,type,name=filename.split('_')
                name=name.replace('.png','')
                self.add(type,name)
        
        for cat in ('body','hair','eyes','nose','mouth'):
            self.get_by_type(cat)[0].equipped=True
        
                
    def add(self, type, name):
        self.inventory.append(Disguise(type, name, allow_stretch=True, keep_ratio=False))
    
    def take(self, name):
        self.get_by_name(name).inventory = True
        
    def equip(self, name):
        disguise=self.get_by_name(name)
        if disguise<>None:
            for d in self.get_by_type(disguise.type):
                d.equipped=False
            disguise.equipped=True
        

    def get_by_type(self, type):
        return [i for i in self.inventory if i.type==type]
    
    def get_by_name(self, name):
        disguise=[i for i in self.inventory if i.name==name]
        if len(disguise)==1:
            return disguise[0]
        else:
            return None
            
    def get_equipped(self):
        return [i for i in self.inventory if i.equipped==True]
        
        
        
        
class Disguise(Image):
    def __init__(self, type, name, inventory=True, equipped=False, **kwargs):
        self.type = type
        self.name = name
        self.inventory = inventory
        self.equipped = equipped
        self.risk = 0
        sh=None,None
        ph={}  
        
        if type == 'body':
            sh=(1, 1)
            ph={'center_x': 0.5, 'y': 0}
        elif type == 'hair':
            sh=(1, 0.5)
            ph={'center_x': 0.5, 'y': 0.5}
        elif type == 'eyes':
            sh=(180/300., 60/300.)
            ph={'center_x': 0.5, 'y': 0.62}
        elif type == 'nose':
            sh=(180/300., 40/300.)
            ph={'center_x': 0.5, 'y': 0.58}
        elif type == 'mouth':
            sh=(180/300., 40/300.)
            ph={'center_x': 0.5, 'y': 0.48}

                
        self.source = os.path.join('data','id_{}_{}.png'.format(type, name))

        super(Disguise, self).__init__(size_hint=sh, pos_hint=ph,**kwargs)
                

    def __repr__(self):
        return str([self.type, self.name, self.inventory, self.equipped])+'\n'
        