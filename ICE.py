import pandas as pd
"""
ICE.py

Generates a json file of the University of Bath's Inventory of Carbon and Energy
formatted according to the Natural Economics RDb specification.

Created on Fri Jan 10 16:58:20 2014

@author: acumen
"""
class ICE_translator():
    source_file = 'Initial-Data/ICE-adaptation.csv'
    delim_s ='###\n'
    delim_e ='!!!\n'
    __dataframes__ = []
    __models__ = []
    __ilist__ = []
    __dlist__ = []
    __st__ = '###,,,,,,,,,,,,,,,\n'
    __en__ = '!!!,,,,,,,,,,,,,,,\n'
    __defaults__ = {'date':'2011-01-01','startdate':'2011-01-01','location':'World','ref':'1',
            'infotype':'u'}
    __modelnames__ = { 
                'ner':('NEResource',('name')),'ned':('NEDependency',('parent_resource','dependency')),
                'nemc':('NEMaterialClass',('classname')),   'nem':('NEMaterial',('name')),
                'neprdc':('NEProductClass',('classname')),  'neprd':('NEProduct', ('name')),
                'neprpc':('NEPropertyClass',('classname')), 'neprp':('NEProperty',('.resource','.actor','.process','name','unit')),
                'nepro':('NEProcess', ('pname','ptype')),   'nepio':('NEProcessIO', ('pid','argid','argtype')),
                'necit':('NECitation', ('title','ctype')),  'neicit':('NEInfoCitation',('iid','cid')),
                'nesv':('NESurveyValue',('.resource','.actor','.process','date','valuetype','value','unit','location','ref')),
                'nesi':('NESurveyInfo',  ('.resource','.actor','.process','startdate','valuetype','value','infotype','location')),
                'neac':('NEActor',  ('name'))
            }    
            
    def get_index(self):
        f = open(self.source_file,'r')
        text = f.readlines()
        f.close()
        i = text.index(self.delim_s)
        self.__ilist__ = [i]
        while True:
            try:
                i = text.index(self.delim_s,i+1)
                self.__ilist__ += [i]
            except:
                break
        return self.__ilist__
    def index_csv(self,lines):
        idx = lines.index(self.__st__)
        ilist = [idx]
        dlist = []
        for i in range(len(lines)):
            jdx = lines.index(self.__st__,idx+1)
            ilist += [jdx]
            d = jdx - idx
            dlist += [d]
        self.__ilist__ = ilist
        self.__dlist__ = dlist
            
        
    def process_csv(self):
        f = open(self.source_file,'r')
        lines = f.readlines()
        f.close()
        # generate index
        self.index_csv(lines)
        # create dataframes
        i = 0
        for index in self.__ilist__:
            skiprows = range(index) + [index,index+2,index+3]
            nrows = self.__dlist__[i]
            self.__dataframes__ += pd.read_csv('Initial-Data/ICE-adaptation.csv',skiprows=skiprows,nrows=nrows).dropna(thresh=nrows,axis=1)
        
        
    def get_model(self):
        f = open(self.source_file,'r')
        text = f.readlines()
        f.close()
        for i in self.__ilist__:
            model = text[i+1]
            model = model[:-1]
            model = model.split(',')
            model = map(lambda x: x.split('.'),model)
            self.__models__ += [model]
        return self.__models__
        
    def parse_model(self,model):
        
        
    def serialize_section(self,dataframe):
        filebeginning = '[\n'
        modelbeginning = '{\"model\"'
        colon = ':\"'
        pk = '\"pk\"'
        fields = '\"fields\":{'
        lineending = '\",'
        modelending = '\"}},\n'
        fileending = '\"}}\n'
    
    def csv_to_json(self):
        #get index
        self.get_index()
        #get models
        self.get_model()
        #set state to model
        self.parse_model(model)
        #get data
        df = self.process_csv()
        #serialize data
        text = self.serialize_section(self,df)
        #write to file
        f = open(self.outputfile,'w')
        f.write()
        f.close()
i = ICE_translator()
model = 'nemc.name,nepc.name,nemd.dep_num,nesi.valuetype,nesi.unit,nesi.valuetype,nesi.unit,nesi.valuetype,nesi.unit,nesi.location'.split(',')
model = map(lambda x: x.split('.'),model)
i.parse_model(model)