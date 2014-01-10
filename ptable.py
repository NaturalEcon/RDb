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
model = 'NEResource'
js = []
for i in range(len(periodictable)):
    pt = periodictable[i]
    js += ['  {\n    \"model\":\"'+model+'\",\n    \"pk\":\"'+str(i)+
        '\",\n    \"fields\": {\n      \"name\":\"'+pt+'\",\n      \"long_name\":\"'+
        e2elem[pt]+'\"\n    }\n  },']
jstring = ''
for j in js:
    jstring += j+'\n'
f = open('ptable-json.js','w')
f.write('[\n')
f.writelines(jstring)
f.write(']')