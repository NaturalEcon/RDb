import json
import csv
"""
ICE.py

Generates a json file of the University of Bath's Inventory of Carbon and Energy
formatted according to the Natural Economics RDb specification.

Created on Fri Jan 10 16:58:20 2014

@author: acumen
"""
class json_generator():
    directory = '/home/acumen/Documents/Sage/NatEcon/Initial-Data/'
    # 'nesi.csv'
    source_files = ('nem.csv',
                    'ner.csv',
                    'nep.csv',
                    
                    'necol.csv',
                    'nesc.csv',
                    'ned.csv'
                    )
    __defaults__ = {'date':'2011-01-01','startdate':'2011-01-01','location':'World','ref':'1',
            'infotype':'u'}
    prefix = 'RDb'
    __modelnames__ = { 
                'nem':'NEResource','ned':'NEDependency','nep':'NEResource','ner':'NEResource',
                'neprp':'NEProperty','nepro':'NEProcess','nepio':'NEProcessIO','nec':'NECitation',
                'neicit':'NEInfoCitation','nesv':'NESurveyValue','nesi':'NESurveyInfo',
                'neac':'NEActor','necol':'NECollection','nesc':'NESubclass'
            }    
    # Needs to fix date formatting.        
    def json_dump(self,filename):
        f = open(self.directory+filename,'r')
        fields = f.readline()
        fields = fields[:-1].split('\t')
        if fields[0][0] == '\'' or fields[0][0] == '\"':
            fields = map(lambda x: x[1:-1],fields)
        reader = csv.DictReader(f,fieldnames=fields,delimiter='\t')
        out = json.dumps([row for row in reader])
        f.close()
        model = self.prefix+'.'+self.__modelnames__[filename[:-4]]
        out = out.replace('{','{\"model\":\"'+model+'\",\"fields\":{')
        out = out.replace('}','}}')
        f = open(self.directory+filename[:-3]+'json','w')
        f.write(out)
        f.close()
    
    
    def dump_files(self):
        for filename in self.source_files:
            self.json_dump(filename)
            
    def load_data(self):
        from django.core.management import execute_from_command_line
        command = 'loaddata'
        for filename in self.source_files:
            f = filename[:-3]+'json'
            execute_from_command_line(command+' '+f)
            
j = json_generator()            
j.dump_files()
