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
nrows = 104
#build dataframe
df = pd.read_csv('ICE-adaptation.csv',header=0,skiprows=[0,2],nrows=nrows)
df['MJ/kg'] = pd.Series(['MJ/kg']*nrows)
df['kgCO_2/kg'] = pd.Series(['kgCO_2/kg']*nrows)
df['kgCO_2e/kg'] = pd.Series(['kgCO_2e/kg']*nrows)
df['Form'] = df['Form'].fillna('')
df['Type'] = df['Type'].fillna('')
df = df.astype(str)
S = pd.Series(range(nrows))
S = S.astype(str)
f = open('ICE-MC-json.js','w')
## Section 1: Material,Type,Form,EE,MJ/kg,EC,kgCO_2/kg,ECe,kgCO_2e/kg
# Initial write
f.write('[\n')
f.writelines('{\"model\":\"NEMaterialClass\",\"pk\":\"'+S+'\",\"fields\":{\"name\":\"'+
        df['Material']+'\",\"subtype\":\"'+df['Type']+'\"}},\n')
f.write('@@@\n')
f.writelines('{\"model\":\"NEMaterial\",\"pk\":\"'+S+'\",\"fields\":{\"name\":\"'+
        df['Form']+'\",\"mclass\":\"'+S+'\"}},\n')
f.write('@@@\n')
f.writelines('{\"model\":\"NESurveyInfo\",\"pk\":\"'+S+'\",\"fields\":{\"resource\":\"'+
        S+'\",\"valuetype\":\"EE\",\"value\":\"'+df['EE']+'\",\"unit\":\"'+df['MJ/kg']+
        '\",\"startdate\":\"'+date+'\",\"infotype\":\"u\"}},\n')
f.writelines('{\"model\":\"NESurveyInfo\",\"pk\":\"'+S+'\",\"fields\":{\"resource\":\"'+
        S+'\",\"valuetype\":\"EC\",\"value\":\"'+df['EC']+'\",\"unit\":\"'+df['kgCO_2/kg']+
        '\",\"startdate\":\"'+date+'\",\"infotype\":\"u\"}},\n')
f.writelines('{\"model\":\"NESurveyInfo\",\"pk\":\"'+S+'\",\"fields\":{\"resource\":\"'+
        S+'\",\"valuetype\":\"ECe\",\"value\":\"'+df['ECe']+'\",\"unit\":\"'+df['kgCO_2e/kg']+
        '\",\"startdate\":\"'+date+'\",\"infotype\":\"u\"}},\n')   
## Section 2: Material,Type,Form,EE,MJ/kg,EC,kgCO_2/kg,EC,kgCO_2e/kg,FE,MJ/kg
# Create new dataframe
nrows = 29
skiprows = range(109)
skiprows += [112]
df = pd.read_csv('ICE-adaptation.csv',header=0,skiprows=skiprows,nrows=nrows)
df['MJ/kg'] = pd.Series(['MJ/kg']*nrows)
df['kgCO_2/kg'] = pd.Series(['kgCO_2/kg']*nrows)
df['kgCO_2e/kg'] = pd.Series(['kgCO_2e/kg']*nrows)
df['Form'] = df['Form'].fillna('')
df['Type'] = df['Type'].fillna('')
df = df.astype(str)
S = pd.Series(range(nrows))
S = S.astype(str)
# Initial write
f.writelines('{\"model\":\"NEMaterialClass\",\"pk\":\"'+S+'\",\"fields\":{\"name\":\"'+
        df['Material']+'\",\"subtype\":\"'+df['Type']+'\"}},\n')
f.write('@@@\n')
f.writelines('{\"model\":\"NEMaterial\",\"pk\":\"'+S+'\",\"fields\":{\"name\":\"'+
        df['Form']+'\",\"mclass\":\"'+S+'\"}},\n')
f.write('@@@\n')
f.writelines('{\"model\":\"NESurveyInfo\",\"pk\":\"'+S+'\",\"fields\":{\"resource\":\"'+
        S+'\",\"valuetype\":\"EE\",\"value\":\"'+df['EE']+'\",\"unit\":\"MJ/kg'+
        '\",\"startdate\":\"'+date+'\",\"infotype\":\"u\",\"location\":\"World\"}},\n')
f.writelines('{\"model\":\"NESurveyInfo\",\"pk\":\"'+S+'\",\"fields\":{\"resource\":\"'+
        S+'\",\"valuetype\":\"EC\",\"value\":\"'+df['EC']+'\",\"unit\":\"kgCO_2/kg'+
        '\",\"startdate\":\"'+date+'\",\"infotype\":\"u\",\"location\":\"World\"}},\n')
f.writelines('{\"model\":\"NESurveyInfo\",\"pk\":\"'+S+'\",\"fields\":{\"resource\":\"'+
        S+'\",\"valuetype\":\"ECe\",\"value\":\"'+df['ECe']+'\",\"unit\":\"kgCO_2e/kg\"'+
        ',\"startdate\":\"'+date+'\",\"infotype\":\"u\",\"location\":\"World\"}},\n')
f.writelines('{\"model\":\"NESurveyInfo\",\"pk\":\"'+S+'\",\"fields\":{\"resource\":\"'+
        S+'\",\"valuetype\":\"FE\",\"value\":\"'+df['FE']+'\",\"unit\":\"MJ/kg\"'+
        ',\"startdate\":\"'+date+'\",\"infotype\":\"u\",\"location\":\"World\"}},\n')
# Section 3:
# Create new dataframe
nrows = 67
skiprows = range(143)
skiprows += [145]
df = pd.read_csv('ICE-adaptation.csv',header=0,skiprows=skiprows,nrows=nrows)
df['MJ/kg'] = pd.Series(['MJ/kg']*nrows)
df['kgCO_2/kg'] = pd.Series(['kgCO_2/kg']*nrows)
df['kgCO_2e/kg'] = pd.Series(['kgCO_2e/kg']*nrows)
df['Product'] = df['Product'].fillna('')
df['Type'] = df['Type'].fillna('')
df = df.astype(str)
S = pd.Series(range(nrows))
S = S.astype(str)
# Initial write
f.writelines('{\"model\":\"NEMaterialClass\",\"pk\":\"'+S+'\",\"fields\":{\"name\":\"'+
        df['Material']+'\",\"subtype\":\"'+df['Type']+'\"}},\n')
f.write('@@@\n')
f.writelines('{\"model\":\"NEProduct\",\"pk\":\"'+S+'\",\"fields\":{\"name\":\"'+
        df['Product']+'\",\"mclass\":\"'+S+'\"}},\n')
f.write('@@@\n')
f.writelines('{\"model\":\"NESurveyInfo\",\"pk\":\"'+S+'\",\"fields\":{\"resource\":\"'+
        S+'\",\"valuetype\":\"EE\",\"value\":\"'+df['EE']+'\",\"unit\":\"MJ/kg\"'+
        ',\"startdate\":\"'+date+'\",\"infotype\":\"u\",\"location\":\"'+df['Location']+'\"}},\n')
f.writelines('{\"model\":\"NESurveyInfo\",\"pk\":\"'+S+'\",\"fields\":{\"resource\":\"'+
        S+'\",\"valuetype\":\"EC\",\"value\":\"'+df['EC']+'\",\"unit\":\"kgCO_2/kg\"'+
        ',\"startdate\":\"'+date+'\",\"infotype\":\"u\",\"location\":\"'+df['Location']+'\"}},\n')
f.writelines('{\"model\":\"NESurveyInfo\",\"pk\":\"'+S+'\",\"fields\":{\"resource\":\"'+
        S+'\",\"valuetype\":\"ECe\",\"value\":\"'+df['ECe']+'\",\"unit\":\"kgCO_2e/kg\"'+
        ',\"startdate\":\"'+date+'\",\"infotype\":\"u\",\"location\":\"'+df['Location']+'\"}},\n')
# Add dependency for recycled ____
f.write(']')

# Clean

f.close()
f = open('ICE-MC-json.js','r')
lines = f.readlines()
output = []
for line in lines:
    if line.count('\"name\":\"\"') < 1 and line.count('nan') < 1 and not line == '@@@\n':
        output += [line]
f.close()
f = open('ICE-MC-json.js','w')
f.writelines(output)
f.close()