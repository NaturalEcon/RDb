"""
ptable.py

Generates a json file of the periodic table formatted according to the Natural 
Econ NEResource specification.

Created on Fri Jan 10 12:39:22 2014

@author: acumen
"""

periodictable = (    "t", \
                     "H",                                                                                   "He", \
                     "Li","Be",                                                    "B", "C", "N", "O", "F", "Ne", \
                     "Na","Mg",                                                    "Al","Si","P", "S", "Cl","Ar", \
                     "K", "Ca",  "Sc","Ti","V", "Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr", \
                     "Rb","Sr",  "Y", "Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I", "Xe", \
                     "Cs","Ba", \
                     "La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb", \
                                 "Lu","Hf","Ta","W", "Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn", \
                     "Fr","Ra", \
                     "Ac","Th","Pa","U", "Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No", \
                                 "Lr","Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Uut","Fl","Uup","Lv","Uus","Uuo", \
                     "e"    )
e2elem = { "t":"Time",
    "H":"Hydrogen","He":"Helium","Li":"Lithium","Be":"Beryllium","B":"Boron","C":"Carbon","N":"Nitrogen","O":"Oxygen","F":"Fluorine","Ne":"Neon",
    "Na":"Sodium","Mg":"Magnesium","Al":"Aluminum","Si":"Silicon","P":"Phosphorous","S":"Sulfur","Cl":"Chlorine","Ar":"Argon",
    "K":"Potassium","Ca":"Calcium","Sc":"Scandium","Ti":"Titanium","V":"Vanadium","Cr":"Chromium","Mn":"Manganese","Fe":"Iron","Co":"Cobalt","Ni":"Nickel","Cu":"Copper","Zn":"Zinc","Ga":"Gallium","Ge":"Germanium","As":"Arsenic","Se":"Selenium","Br":"Bromine","Kr":"Krypton",
    "Rb":"Rubidium","Sr":"Strontium","Y":"Yttrium","Zr":"Zirconium","Nb":"Niobium","Mo":"Molybdenum","Tc":"Technetium","Ru":"Ruthenium","Rh":"Rhodium","Pd":"Palladium","Ag":"Gold","Cd":"Cadmium","In":"Indium","Sn":"Tin","Sb":"Antimony","Te":"Tellurium","I":"Iodine","Xe":"Xenon",
    "Cs":"Caesium","Ba":"Barium","La":"Lanthanum","Ce":"Cerium","Pr":"Praseodymium","Nd":"Neodymium","Pm":"Promethium","Sm":"Samarium","Eu":"Europium","Gd":"Gadolinium","Tb":"Terbium","Dy":"Dysprosium","Ho":"Holonium","Er":"Erbium","Tm":"Thulium","Yb":"Ytterbium",
    "Lu":"Lutetium","Hf":"Hafnium","Ta":"Tantalum","W":"Tungsten","Re":"Rhenium","Os":"Osmium","Ir":"Iridium","Pt":"Plutonium","Au":"Gold","Hg":"Mercury","Tl":"Thallium","Pb":"Lead","Bi":"Bismuth","Po":"Polonium","At":"Astatine","Rn":"Radon","Fr":"Francium","Ra":"Radium",
    "Ac":"Actinium","Th":"Thorium","Pa":"Protactinium","U":"Uranium","Np":"Neptunium","Pu":"Plutonium","Am":"Americium","Cm":"Curium","Bk":"Berkelium","Cf":"Californium","Es":"Einsteinium","Fm":"Fermium","Md":"Mendelevium","No":"Nobelium",
    "Lr":"Lawrencium","Rf":"Rutherfordium","Db":"Dubnium","Sg":"Seaborgium","Bh":"Bohrium","Hs":"Hassium","Mt":"Meitnerium","Ds":"Darmstadtium","Rg":"Roentgenium","Cn":"Copernicum","Uut":"Ununtrium","Fl":"Flerovium","Uup":"Ununpentium","Lv":"Livermorium","Uus":"Ununseptium","Uuo":"Ununoctium",
    "e":"Energy"}
atomicnum2uid = ('304a49c6-7f8e-11e3-bc66-f07bcb4eb64e','304a58e4-7f8e-11e3-bc66-f07bcb4eb64e','304a6794-7f8e-11e3-bc66-f07bcb4eb64e',
          '304a79fa-7f8e-11e3-bc66-f07bcb4eb64e','304a8954-7f8e-11e3-bc66-f07bcb4eb64e','304a9c14-7f8e-11e3-bc66-f07bcb4eb64e',
          '304aacb8-7f8e-11e3-bc66-f07bcb4eb64e','304abf46-7f8e-11e3-bc66-f07bcb4eb64e','304ad03a-7f8e-11e3-bc66-f07bcb4eb64e',
          '304adf30-7f8e-11e3-bc66-f07bcb4eb64e','304af038-7f8e-11e3-bc66-f07bcb4eb64e','304aff24-7f8e-11e3-bc66-f07bcb4eb64e',
          '304b0fbe-7f8e-11e3-bc66-f07bcb4eb64e','304b1e8c-7f8e-11e3-bc66-f07bcb4eb64e','304b2d28-7f8e-11e3-bc66-f07bcb4eb64e',
          '304b411e-7f8e-11e3-bc66-f07bcb4eb64e','304b5456-7f8e-11e3-bc66-f07bcb4eb64e','304b71a2-7f8e-11e3-bc66-f07bcb4eb64e',
          '304b8d68-7f8e-11e3-bc66-f07bcb4eb64e','304ba794-7f8e-11e3-bc66-f07bcb4eb64e','304bb9f0-7f8e-11e3-bc66-f07bcb4eb64e',
          '304bcbc0-7f8e-11e3-bc66-f07bcb4eb64e','304be826-7f8e-11e3-bc66-f07bcb4eb64e','304c0842-7f8e-11e3-bc66-f07bcb4eb64e',
          '304c2520-7f8e-11e3-bc66-f07bcb4eb64e','304c4096-7f8e-11e3-bc66-f07bcb4eb64e','304c5e64-7f8e-11e3-bc66-f07bcb4eb64e',
          '304c7980-7f8e-11e3-bc66-f07bcb4eb64e','304c9384-7f8e-11e3-bc66-f07bcb4eb64e','304cac20-7f8e-11e3-bc66-f07bcb4eb64e',
          '304cc804-7f8e-11e3-bc66-f07bcb4eb64e','304ce37a-7f8e-11e3-bc66-f07bcb4eb64e','304cfc02-7f8e-11e3-bc66-f07bcb4eb64e',
          '304d1570-7f8e-11e3-bc66-f07bcb4eb64e','304d2b5a-7f8e-11e3-bc66-f07bcb4eb64e','304d4310-7f8e-11e3-bc66-f07bcb4eb64e',
          '304d57d8-7f8e-11e3-bc66-f07bcb4eb64e','304d6ab6-7f8e-11e3-bc66-f07bcb4eb64e','304d80b4-7f8e-11e3-bc66-f07bcb4eb64e',
          '304d94e6-7f8e-11e3-bc66-f07bcb4eb64e','304daaee-7f8e-11e3-bc66-f07bcb4eb64e','304dbdf4-7f8e-11e3-bc66-f07bcb4eb64e',
          '304dd1f4-7f8e-11e3-bc66-f07bcb4eb64e','304de4d2-7f8e-11e3-bc66-f07bcb4eb64e','304df8f0-7f8e-11e3-bc66-f07bcb4eb64e',
          '304e0be2-7f8e-11e3-bc66-f07bcb4eb64e','304e20e6-7f8e-11e3-bc66-f07bcb4eb64e','304e33ec-7f8e-11e3-bc66-f07bcb4eb64e',
          '304e488c-7f8e-11e3-bc66-f07bcb4eb64e','304e5b74-7f8e-11e3-bc66-f07bcb4eb64e','304e6fa6-7f8e-11e3-bc66-f07bcb4eb64e',
          '304e8284-7f8e-11e3-bc66-f07bcb4eb64e','304e99b8-7f8e-11e3-bc66-f07bcb4eb64e','304eb754-7f8e-11e3-bc66-f07bcb4eb64e',
          '304ed13a-7f8e-11e3-bc66-f07bcb4eb64e','304eed32-7f8e-11e3-bc66-f07bcb4eb64e','304f09fc-7f8e-11e3-bc66-f07bcb4eb64e',
          '304f234c-7f8e-11e3-bc66-f07bcb4eb64e','304f3e22-7f8e-11e3-bc66-f07bcb4eb64e','304f5862-7f8e-11e3-bc66-f07bcb4eb64e',
          '304f71ee-7f8e-11e3-bc66-f07bcb4eb64e','304fb6fe-7f8e-11e3-bc66-f07bcb4eb64e','304fcd9c-7f8e-11e3-bc66-f07bcb4eb64e',
          '304fe106-7f8e-11e3-bc66-f07bcb4eb64e','304ff5b0-7f8e-11e3-bc66-f07bcb4eb64e','305008d4-7f8e-11e3-bc66-f07bcb4eb64e',
          '30501e3c-7f8e-11e3-bc66-f07bcb4eb64e','305031f6-7f8e-11e3-bc66-f07bcb4eb64e','30504812-7f8e-11e3-bc66-f07bcb4eb64e',
          '30506ca2-7f8e-11e3-bc66-f07bcb4eb64e','305086ce-7f8e-11e3-bc66-f07bcb4eb64e','3050a118-7f8e-11e3-bc66-f07bcb4eb64e',
          '3050b68a-7f8e-11e3-bc66-f07bcb4eb64e','3050c9f4-7f8e-11e3-bc66-f07bcb4eb64e','3050df70-7f8e-11e3-bc66-f07bcb4eb64e',
          '3050f5b4-7f8e-11e3-bc66-f07bcb4eb64e','30510c48-7f8e-11e3-bc66-f07bcb4eb64e','30511eea-7f8e-11e3-bc66-f07bcb4eb64e',
          '30513452-7f8e-11e3-bc66-f07bcb4eb64e','305146ae-7f8e-11e3-bc66-f07bcb4eb64e','30515c66-7f8e-11e3-bc66-f07bcb4eb64e',
          '30516e9a-7f8e-11e3-bc66-f07bcb4eb64e','30518308-7f8e-11e3-bc66-f07bcb4eb64e','305194f6-7f8e-11e3-bc66-f07bcb4eb64e',
          '3051aa68-7f8e-11e3-bc66-f07bcb4eb64e','3051bcba-7f8e-11e3-bc66-f07bcb4eb64e','3051d27c-7f8e-11e3-bc66-f07bcb4eb64e',
          '3051e4c4-7f8e-11e3-bc66-f07bcb4eb64e','3051f946-7f8e-11e3-bc66-f07bcb4eb64e','30520b34-7f8e-11e3-bc66-f07bcb4eb64e',
          '305222a4-7f8e-11e3-bc66-f07bcb4eb64e','30523ae6-7f8e-11e3-bc66-f07bcb4eb64e','30525508-7f8e-11e3-bc66-f07bcb4eb64e',
          '30527056-7f8e-11e3-bc66-f07bcb4eb64e','30528ac8-7f8e-11e3-bc66-f07bcb4eb64e','3052a35a-7f8e-11e3-bc66-f07bcb4eb64e',
          '3052be94-7f8e-11e3-bc66-f07bcb4eb64e','3052d9ba-7f8e-11e3-bc66-f07bcb4eb64e','30530264-7f8e-11e3-bc66-f07bcb4eb64e',
          '30531d4e-7f8e-11e3-bc66-f07bcb4eb64e','305339a0-7f8e-11e3-bc66-f07bcb4eb64e','30535552-7f8e-11e3-bc66-f07bcb4eb64e',
          '3053714a-7f8e-11e3-bc66-f07bcb4eb64e','30538a72-7f8e-11e3-bc66-f07bcb4eb64e','3053a78c-7f8e-11e3-bc66-f07bcb4eb64e',
          '3053c370-7f8e-11e3-bc66-f07bcb4eb64e','3053dcd4-7f8e-11e3-bc66-f07bcb4eb64e','3053f962-7f8e-11e3-bc66-f07bcb4eb64e',
          '30541406-7f8e-11e3-bc66-f07bcb4eb64e','30542cd4-7f8e-11e3-bc66-f07bcb4eb64e','3054482c-7f8e-11e3-bc66-f07bcb4eb64e',
          '305463ac-7f8e-11e3-bc66-f07bcb4eb64e','30547c8e-7f8e-11e3-bc66-f07bcb4eb64e','30549886-7f8e-11e3-bc66-f07bcb4eb64e',
          '3054b35c-7f8e-11e3-bc66-f07bcb4eb64e','3054cc2a-7f8e-11e3-bc66-f07bcb4eb64e','3054e7e6-7f8e-11e3-bc66-f07bcb4eb64e',
          '30550334-7f8e-11e3-bc66-f07bcb4eb64e','30551ff4-7f8e-11e3-bc66-f07bcb4eb64e','305539c6-7f8e-11e3-bc66-f07bcb4eb64e')
model = 'RDb.NEResource'
js = []
for i in range(len(periodictable)):
    pt = periodictable[i]
    js += ['{\"model\":\"'+model+'\",\"pk\":'+str(i)+
        ',\"fields\":{\"name\":\"'+pt+'\",\"long_name\":\"'+
        e2elem[pt]+'\"}}']
jstring = ''
for j in js[:-1]:
    jstring += j+',\n'
jstring +=js[-1]
f = open('Initial-Data/ptable.json','w')
f.write('[\n')
f.writelines(jstring)
f.write(']')