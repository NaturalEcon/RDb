import json
import csv
"""
ICE.py

Generates a json file of the University of Bath's Inventory of Carbon and Energy
formatted according to the Natural Economics RDb specification.

Created on Fri Jan 10 16:58:20 2014

@author: acumen
"""
ROOT_PATH = os.path.join(os.path.dirname(__file__), '..')
class json_generator():
    directory = os.path.join(ROOT_PATH,'Initial-Data/')
    csv_dir = 'CSV/'
    json_dir = 'JSON/'
    # 'nesi.csv'
    source_files = ('nem.csv',
                    'ner.csv',
                    'nep.csv',
                    'nesc.csv',
                    'ned.csv',
                    'nec.csv',
                    'necol.csv',
                    'nesi.csv'
                    )
    __defaults__ = {'date':'2011-01-01','startdate':'2011-01-01','enddate':'2050-01-01','location':'World','ref':'1',
            'infotype':'u'}
    prefix = 'RDb'
    __modelnames__ = {
                'nem':'NEResource','ned':'NEDependency','nep':'NEResource','ner':'NEResource',
                'neprp':'NEProperty','nepro':'NEProcess','nepio':'NEProcessIO','nec':'NECitation',
                'neicit':'NEInfoCitation','nesv':'NESurveyValue','nesi':'NESurveyInfo',
                'neac':'NEActor','necol':'NECollection','nesc':'NESubclass'
            }
    __pk__ = { 'NEResource':'rid' }
    # Needs to fix date formatting.
    def json_dump(self,filename):
        f = open(self.directory+self.csv_dir+filename,'r')
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
        out = out.replace('\"date\": \"\"','\"date\": \"'+self.__defaults__['date']+'\"')
        out = out.replace('\"startdate\": \"\"','\"startdate\": \"'+self.__defaults__['startdate']+'\"')
        out = out.replace('\"enddate\": \"\"','\"enddate\": \"'+self.__defaults__['enddate']+'\"')
        f = open(self.directory+self.json_dir+filename[:-3]+'json','w')
        f.write(out)
        f.close()

    def json_dump_alt(self,filename):
        modelname = self.prefix+'.'+self.__modelnames__[filename[:-4]]
        ftext = '\",\"fields\":'
        short_name = '","short_name":"'
        end = '"}}'
        lines = []
        f = open(self.directory+self.csv_dir+filename,'r')
        fields = f.readline()
        fields = fields.replace('\"','')
        fields = fields[:-1].split('\t')
        reader = csv.DictReader(f,fieldnames=fields,delimiter='\t')

        pk = 'pk'
        for row in reader:
            line = '{\"model\":\"%s\",' % modelname
            try:
                line += '\"%s\":\"%s\",' % (pk,row[pk])
                del row[pk]
            except KeyError:
                pass
            line += '\"fields\": %s },' % unicode(row)
            lines += [line]
        f.close()
        text = '['
        text += ''.join(lines)
        text = text.replace('\'','\"')
        text = text[:-1] + ']'
        for f in fields:
			blank = '\"%s\": \"\",' % f
			text = text.replace(blank, '')
        f = open(self.directory+self.json_dir+filename[:-3]+'json','w')
        f.write(text)
        f.close()


    def dump_files(self):
        for filename in self.source_files:
            self.json_dump_alt(filename)

    def load_data(self):
        from django.core.management import execute_from_command_line
        command = 'loaddata'
        for filename in self.source_files:
            f = filename[:-3]+'json'
            execute_from_command_line(command+' '+f)

j = json_generator()
j.dump_files()
