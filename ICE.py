import pandas as pd
"""
ICE.py

Generates a json file of the University of Bath's Inventory of Carbon and Energy
formatted according to the Natural Econ NESurveyValue specification.

Created on Fri Jan 10 16:58:20 2014

@author: acumen
"""
#JSON string format
lineending = '\",\n'
modelstring = '  {\n  \"model\":'
pkstring = '    \"pk\":'
fieldsstring = '    \"fields\":{'
modelending = '\"\n    }\n  },'
#JSON Data
model = ["NEMaterialClass","+","NEMaterial"]+["NESurveyInfo","+"]*3
pk = 0
date = '2011-01-01'
loc = 'World'
fields = ['name','subclass','name','valuetype','unit','valuetype','unit','valuetype','unit']
nrows = 107
#build dataframe
df = pd.read_csv('ICE-adaptation.csv',header=0,skiprows=[0,2],nrows=nrows)
df['MJ/kg'] = pd.Series(['MJ/kg']*nrows)
df['kgCO_2/kg'] = pd.Series(['kgCO_2/kg']*nrows)
df['kgCO_2e/kg'] = pd.Series(['kgCO_2e/kg']*nrows)
df['Form'] = df['Form'].fillna('')
df['Type'] = df['Type'].fillna('')
df = df.astype(str)
S = []
cols = df.columns
fc = zip(fields,cols)
st = '      \"'
mi = '\":\"'
en = '\",\n'
S = []
for f in fc:
    if f[0] == 'valuetype':
        S += [st+f[0]+mi+f[1]+en+st+'\"value'+mi+df[f[1]]+en]
    else:
        S += [st+f[0]+mi+df[f[1]]+en]
D = pd.DataFrame(S).transpose()

f = open('ICE-MC-json.js','w')
f.write('[\n')
f.writelines('{\"model\":\"NEMaterialClass\",\"pk\":\"###\",\"fields\":{\"name\":\"'+
        df['Material']+'\",\"subtype\":\"'+df['Type']+'\"}},\n')
f.write('@@@\n')
f.writelines('{\"model\":\"NEMaterial\",\"pk\"###\",\"fields\":{\"name\":\"'+
        df['Form']+'\",\"mclass\":\"###\"}},\n')
f.write(']')
f.close()
f = open('ICE-MC-json.js','r')
text = f.readlines()
i = 0
output = []
for t in text:
    if t == '@@@\n':
        i = 0
    elif t.count('\"name\":\"\"') !=1:
        output += [t.replace('###',str(i))]
    i += 1
f.close()
f = open('ICE-MC-json.js','w')
f.writelines(output)
f.close()
#f.write('      \"subtype\":\"'+df['Type'])
#dostuff
#Process entire file at once
#i = 0
#models = []
#pks = []
#fields = []
##nemc.name,nemc.child,nem.name,nesi.valuetype,nesi.unit,nesi.valuetype,nesi.unit,nesi.valuetype,nesi.unit
##get list of number of fields for each model present
#f = open('ICE-adaptation.csv','r')
#text = f.readlines()
#field_models = []
#models = text[text.str.contains('###')]
#models.index = pd.Index(range(models.count))
#models = models.str[4:-1]
#models = models.str.split(',')
#k = 0
