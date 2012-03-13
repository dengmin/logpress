#!/usr/bin/env python
# *_* encoding=utf-8*_*

import os,re
import json

IDENTIFIER = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

class Theme(object):
    
    def __init__(self, path):
        self.path = os.path.abspath(path)
        with open(os.path.join(self.path, 'metadata.json')) as fd:
            content = fd.read()
            self.info = json.loads(content)
        
        self.name = self.info.get('name')
        self.id = self.info.get('id')
        self.description = self.info.get('description')
        self.author = self.info.get('author','logpress')
        self.website=self.info.get('website',"#")
        self.tags = self.info.get('tags')
        self.screenshot=self.info.get('screenshot')
        self.options = self.info.get('options',{})

    def __str__(self):
        return 'name:%s\nid:%s\ndescription:%s\nauthor:%s\nwebsite:%s'%(self.name,self.id,self.description,\
                                                                        self.author,self.website)


def list_folders(path):
    return [name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name))]

def load_themes_from(path):
    themes = []
    for basename in (b for b in list_folders(path) if IDENTIFIER.match(b)):
        try:
            t = Theme(os.path.join(path, basename))
            themes.append(t)
        except:
            pass
    return themes