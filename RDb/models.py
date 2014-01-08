from django.db import models
"""
Created on Tue Jan  7 12:55:59 2014

@author: acumen
"""
rclasses = (
    ('R','Resource'),('M','Material'),('P','Product'),('S','Service'),('D','Data')
)

dtypes = (('f','Forward'),('b','Backward'),('i','Inter'))
infotypes = ( 
    ('u','Mean'),    
    ('m','Median'),
    ('o','Mode'),
    ('a','Maximum'),
    ('i','Minimum'),
    ('s','Standard deviation of'),
    ('E','Expected value of'),
    ('V','Variance of'),
    ('M','Moment'),
    ('^','Estimated'),
    ('e','Error of'),
    ('w','Skew of'),
    ('k','Kurtosis of'),
    ('p','Significance level of'),
    ('*','Optimal'),
    ('x','Safety'),
)
valuetypes = (
    ('Mass', (
        ('K','Known'),
        ('S','In Reserve'),
        ('E','Exploited'),
        ('D','Demanded'),
        )
    ),
    ('Rate', (
        ('dK','Discovery Rate'),
        ('dS','Reserve Rate'),
        ('dE','Exploitation Rate'),
        ('dD','Rate of Change in Demand'),
        )
    ),
    ('Energy', (
        ('EE','Embodied Energy'),
        ('PE','Process Energy'),
        ('EX','Exergy'),
        ('EM','Emergy'),
        )
    ),
    ('Other', (
        ('%Y','Percent Yield'),
        )
    ),
)
ptypes = (
    ('Mass', (
        ('Unary', (
            ('mco','Concentration'),
            ('mdi','Dispersion'),
            ('mxp','Transport'),
            ('mre','Reduction'),
            ('mac','Accretion'),
            ),
        ),
        ('One-to-One', (
            ('mmi','Milling'),
            ('mgr','Grinding'),
            ('mcu','Cutting'),
            ('mbe','Bending'),
            ('mfo','Forming'),        
            ),        
        ),
        ('Many-to-one', (
            ('mag','Aggregation'),
            ('msm','Smelting'),        
            ('mds','Dissolution'),
            ('mas','Assembling'),
            ('mal','Alloying'),
            ),
        ),
        ('One-to-many', (
            ('mus','Disassembling'),
            ),        
        ),
        ('Recursive', (
            ('mrp','Repairing'),
            ),
        ),
        ('Many-to-many', (
            )
        ),
        ('Multiple', (
            ('mrc','Recycling'),
            ('mrx','Reaction'),
            ),
        ),
        )
    ),
    ('Energy', 
        ('General', (    
            ('egc','Conversion'),
            ('egs','Storage'),
            ('ego','Concentration'),
            ('ege','Entropic'),
            ('egf','Flow'),
            )
        ),
        ('Electrical', (
            ('eet','Transmission'),
            )
        )
    ),
    ('Time', (
        
        )
    ),
    ('Actor',(
        ('asc','State Change'),
        )
    ),
)
argtypes = (('I','Input'),('O','Output'))
ctypes = (
    ('J','Journal article'),('R','Report'),('P','Personal communication'),
    ('B','Book'),('M','Memo')
)
class NEResource(models.Model):
    ##########################
    # ID namespace:
    # 0:       Time
    # 1-118:   Elements by atomic number
    # 119:     Energy
    # 120-256: Top 136 most abundant materials
    # ID is a 6-character hex code, giving the possibility for up to 
    # 16,777,216 different resources in the database.
    # Size of fully-populated NEResource table: 432MiB
    ##########################
    # NEResource names:
    # Please try to stay within 20 characters.  If the name is longer, it will
    # be replaced with a longname ID, which will point to a row in a table of 
    # long names.  This is done to speed up searching and reduce the size of
    # this required table.
    ##########################
    name = models.CharField(max_length=20)
    ##########################
    # R Classes:
    # R: Resource
    # M: Material
    # P: Product
    # S: Service
    # D: Data
    ##########################
    rclass = models.CharField(max_length=1,choices=rclasses)
    
    
class Dependency(models.Model):
    resource = models.ForeignKey(NEResource)
    dependency = models.ForeignKey(NEResource)
    dtype = models.CharField(max_length=1,choices=dtypes)
    dependency_mult = models.FloatField()
    
    def __repr__(self):
        return "%5.2f x %s" % (self.dependency_mult, self.dependency)
        
class NEMaterialClass(models.Model):
    classname = models.CharField(max_length=50)
    
    def __repr__(self):
        return "Material class: %s" % (self.classname)
        
        
class NEMaterial(NEResource):
    # ID is a 6-character hex code
    # The materials address space could be broken down further using material classes.
    # e.g. Polymer, Structural, Refractory, Conductive.
    # This could also be automatically defined using extended property selection.
    __addressspace__ = (120,524288)
    mclass = models.ForeignKey(NEMaterialClass)
        
    def __repr__(self):
        return "Material %i, type %i" % (self.id,self.mclass)

# NE Process represents an industrial process or (limited scale) natural process.
class NEProcess(models.Model):
    pname = models.CharField(max_length=30)
    ptype = models.CharField(max_length=1,choices=ptypes)
    inputs = []
    outputs = []            

    def addNewIO(self,v_id=None,v_weight=None,v_type=None):
        if v_id == None:
            raise ValueError("You must specify a resource.")
        if v_weight == None:
            raise ValueError("You must specify a weight.")
        if v_type == 'I':
            self.inputs += NEProcessIO(v_id=v_id,v_weight=v_weight,v_type='I')
        elif v_type == 'O':
            self.output += NEProcessIO(v_id=v_id,v_weight=v_weight,v_type='O')
    
    def __repr__(self):
        return "%s (#%s)\n Inputs: %s \n Outputs: %s" % (self.pname,self.pid,self.inputs,self.outputs)
            
class NEProcessIO(models.Model):
    __tablename__ = 'processio'
    pid = models.ForeignKey(NEProcess)
    argid = models.ForeignKey(NEResource)
    argweight = models.FloatField()    
    argtype = models.CharField(max_length=1,choices=argtypes)

#NE Citation is a simple research citation class until I implement Zotero support.
# Because it is not intended to be in the project long-term, it will be limited to only
# a few types.        
class NECitation(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50,empty=True)
    date = models.DateField(empty=True)
    doi = models.CharField(max_length=30,empty=True)
    isbn = models.CharField(max_length=13,empty=True)
    ctype = models.CharField(max_length=1,choices=ctypes)
    
    def __repr__(self):
        output = ""
        if self.title != None: output += self.title + ". "
        if self.author != None: 
            output += self.author + " "
        if self.date != None: output += self.date.strftime("%Y") + " "
        if self.doi != None: output += self.doi + " "
        return output
        
        
# NESurveyValue is intended to represent a single data point.
class NESurveyValue(models.Model):
    # Resource or process ID
    resource = models.ForeignKey(NEResource,empty=True)
    process = models.ForeignKey(NEProcess,empty=True)
    actor = models.ForeignKey('NEActor',empty=True)
    # UNIX time of observation
    date = models.DateField()
    # Valuetype can be one of the following:
    #########################################
    # Mass-based
    #  K,S,E,D: Resource mass quantity, in kg
    #       K: resources known (R,M)
    #       S: resources in reserve (R) or inventory (M,P)
    #       E: reserve and allocated resources (R,M) or products in use (P)
    #       D: material requirements (R,M) or product demand (P). The latter requires user input.
    #########################################
    # Rate-based
    #   dK,dS,dE,dD: Changes in  in kg per year 
    #       dK: rate of discovery (R,M)
    #       dS: replenishment rate (RR) or discovery rate (NRR)
    #       dE: extraction rate (R) or production rate (M,P)
    #       dD: rate of change in demand
    #   dEG,dEE,dEX,dEM: Changes in kWh/kg per year
    #       dEE: rate of change in embodied energy
    #       dPE: rate of change in process energy
    #       dEX: rate of change in exergy
    #       dEM: rate of change in emergy
    #########################################
    # Energy-based
    #  EG, EE, EX, EM: Energy input requirement for the resource in kWh/kg
    #       EE: embodied energy content
    #       PE: process energy
    #       EX: exergy value
    #       EM: emergy value
    #########################################
    valuetype = models.CharField(max_length=3,choices=valuetypes)
    value = models.FloatField()
    # Location of the survey; May be replaced with "energy distance"
    loc = models.TextField()
    ref = models.ForeignKey(NECitation)
    # Valid valuetype codes:
        
    def __repr__(self):
        sinq = ""
        inq = None
        if self.resource != None:
            sinq = "Resource: "
            inq = self.resource
        if self.process != None:
            sinq = "Process: "
            inq = self.process
        start = sinq + "%i Year: %s Type: %s Value: %5.2f Location: %s Reference: %s" \
            % (inq,self.t.strftime("%Y"),self.valuetype,self.value,self.loc,self.ref)
        if self.locs != None: l = "\n Location: %s" % self.loc
        else: l = "No Location"
        if self.ref != None: ref = "\n Reference: %s" % self.ref
        else: ref = "\n Unsourced"
        return str(start+l+ref)

   
# NEResourceInfo is designed to represent information extrapolated from a collection of data,
# as in a statistical survey or meta-study.
class NESurveyInfo(models.Model):
    resource = models.ForeignKey(NEResource,empty=True)
    process = models.ForeignKey(NEProcess,empty=True)
    actor = models.ForeignKey('NEActor',empty=True)
    starttime = models.DateField()
    endtime = models.DateField(empty=True)
    value = models.FloatField()
    valuetype = models.CharField(max_length=3,choices=valuetypes)
    infotype = models.CharField(max_length=1,choices=infotypes)
    citations = []
    
    def setCitations(self,citations):
        ctype = type(citations[0])
        refs = []
        if ctype == NEInfoCitation:
            self.citations = citations.citations
            return self.citations
        if ctype == NECitation:
            for c in citations:
                refs += [NEInfoCitation(cid=c.id)]
        return refs

    
    def __repr__(self):
        sinq = ""
        inq = None
        if self.resource != None:
            sinq = "Resource: "
            inq = self.resource
        if self.process != None:
            sinq = "Process: "
            inq = self.process
        start = sinq + "%i Value: %5.2f Type: %s Start time: %s End time: %s" \
            % (inq,self.value, self.infotype,self.t.strftime("%Y"),self.endtime.strftime("%Y"))
        if self.loc != None: l = "\n Location: %s" % self.loc
        else: l = "No Location"
        if self.ref != None: ref = "\n Reference: %s" % self.ref
        else: ref = "Unsourced"
        return str(start+l+ref)

class NEInfoCitation(models.Model):
    description = models.TextField(blank=True)
    iid = models.ForeignKey(NESurveyInfo)
    cid = models.ForeignKey(NECitation)
    
    
#NE Actor is the base class for organisms, organizations, and complex systems.
class NEActor(models.Model):
    name = models.CharField(max_length=30)
    parents = models.ManyToMany('NEActor')
    children = models.ManyToMany('NEActor')
