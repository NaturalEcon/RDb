from django.db import models
from managers import *
from datetime import date
"""
Created on Tue Jan  7 12:55:59 2014

@author: acumen
"""
# For descriptions of most of the sets here, see the following mathematical model
# definition: http://naturalecon.wordpress.com/glossary/
# Note that there are some differences, such as the lack of a 'Component' class
# in this model, and the addition of several survey value types.
rclasses = (
    ('R','Resource'),('M','Material'),('P','Product'),('S','Service'),('D','Data')
)
# A "forward" dependency for resource R is a resource which depends on R.
# A "backward" dependency for resource R is a resource on which R depends.
# An "inter" dependency is either a co-product of R, or a member of a renewable cycle
dtypes = (('f','Forward'),('b','Backward'),('i','Inter'))
# Info types are types of values derived from or describing a value type.
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
        ('FE','Feedstock Energy')
        )
    ),
    ('Other', (
        ('%Y','Percent Yield'),
        ('MT','Mean time before failure'),
        ('MF','Maintenance-free Operating Period'),
        ('PR','Property Value'),
        ('EC','Embodied Carbon')
        )
    ),
)
ptypes = (
    ('Mass', (
        ('mco','Concentration'),
        ('mdi','Dispersion'),
        ('mxp','Transport'),
        ('mre','Reduction'),
        ('mac','Accretion'),
        ('mmi','Milling'),
        ('mgr','Grinding'),
        ('mcu','Cutting'),
        ('mbe','Bending'),
        ('mfo','Forming'),
        ('mag','Aggregation'),
        ('msm','Smelting'),        
        ('mds','Dissolution'),
        ('mas','Assembling'),
        ('mal','Alloying'),
        ('mus','Disassembling'),
        ('mrp','Repairing'),
        ('mrc','Recycling'),
        ('mrx','Reaction'),
        )
    ),
    ('Energy', (   
        ('egc','Conversion'),
        ('egs','Storage'),
        ('ego','Concentration'),
        ('ege','Entropic'),
        ('egf','Flow'),
        )
    ),
    ('Time', (
        ('ter','Erosion'),
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
atypes = ( ('org','Organization'),('ogn','Organism'),('sys','System'),('hom','Person') )

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
    long_name = models.CharField(max_length=128)
    ##########################
    # R Classes:
    # R: Resource
    # M: Material
    # P: Product
    # S: Service
    # D: Data
    ##########################
    rclass = models.CharField(max_length=1,choices=rclasses,
                              blank=True,default='R',
                              verbose_name='Resource Class')
    objects = models.Manager()
    dataframe = DataFrameManager()
    
    class Meta:
        verbose_name = 'Resource'
    
    def __repr__(self):
        return self.name
    def __unicode__(self):
        return self.__repr__()
        
        
class NEDependency(models.Model):
    parent_resource = models.ForeignKey('NEMaterial',related_name='parent_resources')
    dependency = models.ForeignKey(NEResource,related_name='child_resources')
    dependency_mult = models.FloatField(default=1.0,verbose_name='Dependency Multiplicity')
    
    class Meta:
        verbose_name_plural = 'Dependencies'
        unique_together = (('parent_resource','dependency'),)
    
    def __repr__(self):
        return "%5.2f x %s" % (self.dependency_mult, self.dependency)
    def __unicode__(self):
        return self.__repr__()
        
class NEMaterialClass(models.Model):
    classname = models.CharField(max_length=64,verbose_name='Class Name')
    subtype = models.CharField(max_length=64,blank=True,null=True)
    description = models.TextField(blank=True,default='')
    current_standard = models.ForeignKey('NEMaterial',related_name='std_of_material_class',
                                         blank=True,null=True,
                                         verbose_name='Current Standard')
    members = models.ManyToManyField('NEMaterial',related_name='parent_class',
                                         verbose_name='Member Materials')
    subclasses = models.ManyToManyField('NEMaterialClass',related_name='superclass',
                                         symmetrical=False,'Subclasses')
    objects = models.Manager()
    dataframe = DataFrameManager()
    
    class Meta:
        verbose_name = 'Material Class'
        verbose_name_plural = 'Material Classes'
    
    def __repr__(self):
        return "Material class: %s:\n \"%s\"\n Current standard: %s" % \
            (self.classname,self.description,self.current_standard)
    def __unicode__(self):
        return self.__repr__()
        
class NEMaterial(NEResource):
    # ID is a 6-character hex code
    # The materials address space could be broken down further using material classes.
    # e.g. Polymer, Structural, Refractory, Conductive.
    # This could also be automatically defined using extended property selection.
    __addressspace__ = (120,524288)
    mclass = models.ForeignKey(NEMaterialClass,related_name='material_class_members',
                               blank=True,null=True,
                               verbose_name='Material Class')
                               
    deps = models.ManyToManyField(NEResource, related_name='forward_dependency',through='NEDependency',
                                  symmetrical=False,verbose_name='Dependency')
    objects = models.Manager()
    dataframe = DataFrameManager()
    
    class Meta:
        verbose_name = 'Material'
    
    def __repr__(self):
        return "Material %s, type %i" % (self.name,self.mclass)
    def __unicode__(self):
        return self.__repr__()


class NEProductClass(models.Model):
    classname = models.CharField(max_length=50,verbose_name='Class Name')
    description = models.TextField(blank=True,default='')
    current_standard = models.ForeignKey('NEProduct',related_name='std_of_product_class',
                                         blank=True,null=True,
                                         verbose_name='Current Standard')

    objects = models.Manager()
    dataframe = DataFrameManager()

    class Meta:
        verbose_name = 'Product Class'        
        verbose_name_plural = 'Product Classes'                            
    
    def __repr__(self):
        return "Product class %s:\n \"%s\"\n Current standard: %s" % \
            (self.classname,self.description,self.current_standard)
    def __unicode__(self):
        return self.__repr__()
    

class NEProduct(NEMaterial):
    # ID is a 6-character hex code
    # There are 16,252,928 possible products that can go in this database.
    # This address space could be broken down further using product classes.
    __addressspace__ = (524288,16777216)
    pclass = models.ForeignKey(NEProductClass,related_name='product_class_members',blank=True,null=True)
    
    objects = models.Manager()
    dataframe = DataFrameManager()    
    
    class Meta:
        verbose_name = 'Product'    
    
    def __repr__(self):
        return "Product %s, type %s" % (self.name,self.pclass)
    def __unicode__(self):
        return self.__repr__()        

class NEProperty(models.Model):
    rid = models.ForeignKey('NEResource',related_name='property_rsc',
                            blank=True,null=True,
                            verbose_name='Resource')
    pid = models.ForeignKey('NEProcess',related_name='property_pro',
                            blank=True,null=True,
                            verbose_name='Process')
    aid = models.ForeignKey('NEActor',related_name='property_act',
                            blank=True,null=True,
                            verbose_name='Actor')
    name = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    pclass = models.ForeignKey('NEPropertyClass',related_name='property_subtypes',verbose_name='Property Class')
    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
    
    def __repr__(self):
        return '%s of %s: %f %s' % (self.name,self.rid,self.value,self.unit)
    def __unicode__(self):
        return self.__repr__()


class NEPropertyClass(models.Model):
    classname = models.CharField(max_length=30,verbose_name='Class name')
    description = models.TextField(blank=True,default='')
    effects = models.ManyToManyField('NEPropertyClass',related_name='affected')
    class Meta:
        verbose_name = 'Property Class'
        verbose_name_plural = 'Property Classes'
    
    def __repr__(self):
        '%s,\n %s\n Affects:\n %s' % (self.classname,self.description,self.effects)
    def __unicode__(self):
        return self.__repr__()
    
# NE Process represents an industrial process or (limited scale) natural process.
class NEProcess(models.Model):
    pname = models.CharField(max_length=30,verbose_name='Process name')
    ptype = models.CharField(max_length=1,choices=ptypes,verbose_name='Process type')
    io = models.ManyToManyField( NEResource,through='NEProcessIO',symmetrical=False,
                                verbose_name='Inputs/Outputs',related_name='relevant_processes')

    objects = models.Manager()
    dataframe = DataFrameManager()
     
    class Meta:
        verbose_name = 'Process'
        verbose_name_plural = 'Processes'

    def addNewIO(self,argid=None,argweight=None,argtype=None):
        if argid == None:
            raise ValueError("You must specify a resource.")
        if argweight == None:
            raise ValueError("You must specify a weight.")
        if argtype == 'I':
            argtype='I'
        elif argtype == 'O':
            argtype='O'
        self.inputs += [NEProcessIO(pid=self,argid=argid,argweight=argweight,argtype=argtype)]
    
    def __repr__(self):
        return "%s (Type %s)\n Inputs: %s \n Outputs: %s" % (self.pname,self.ptype,self.inputs,self.outputs)
            
class NEProcessIO(models.Model):
    pid = models.ForeignKey(NEProcess,related_name='process',verbose_name='Process')
    argid = models.ForeignKey(NEResource,related_name='process_arg',verbose_name='Argument')
    argweight = models.FloatField(default=1.0,verbose_name='Argument weight')
    argtype = models.CharField(max_length=1,choices=argtypes,verbose_name='Argument type')
    class Meta:
        verbose_name = 'Process IO'
        verbose_name_plural = 'Process IO'

# NE Citation is a simple research citation class until I implement Zotero support.
#  Because it is not intended to be in the project long-term, it will be limited to only
#   a few types.        
class NECitation(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50,blank=True,default='Unknown Author')
    date = models.DateField(blank=True,auto_now_add=True)
    doi = models.CharField(max_length=30,blank=True,default='',verbose_name='DOI')
    isbn = models.CharField(max_length=13,blank=True,default='',verbose_name='ISBN')
    ctype = models.CharField(max_length=1,choices=ctypes,verbose_name='Citation type')
    
    objects = models.Manager()
    dataframe = DataFrameManager()    
    
    class Meta:
        verbose_name = 'Citation'
    
    def __repr__(self):
        output = ""
        if self.title is not None: output += self.title + ". "
        if self.author is not None: 
            output += self.author + ", "
        if self.doi is not None: output += self.doi + " "
        return output

    def __unicode__(self):
        return self.__repr__()        
        
        
# NESurveyValue is intended to represent a single data point.
class NESurveyValue(models.Model):
    # Resource or process ID
    resource = models.ForeignKey(NEResource,blank=True,null=True,related_name='surveyvalue_rsc')
    process = models.ForeignKey(NEProcess,blank=True,null=True,related_name='surveyvalue_proc')
    actor = models.ForeignKey('NEActor',blank=True,null=True,related_name='surveyvalue_act')
    # UNIX time of observation
    date = models.DateField()
    # Value type.  See static 'valuetypes' definition for documentation.    
    valuetype = models.CharField(max_length=3,choices=valuetypes)
    value = models.FloatField()
    unit = models.CharField(max_length=10)
    # If this is about a property of a resource, put the property here.
    prop_pointer = models.ForeignKey('NEProperty',blank=True,null=True,
                                     related_name='property_data',verbose_name='Property')
    # Location of the survey; May be replaced with "energy distance"
    loc = models.TextField(verbose_name='Location')
    # All survey values should have citations to back them up.
    ref = models.ForeignKey(NECitation,verbose_name='Citation')
    
    # Managers
    objects = models.Manager()
    resources = ResourceSurveyManager()
    processes = ProcessSurveyManager()
    actors = ActorSurveyManager()
    dataframe = DataFrameManager()    
    
    class Meta:
        verbose_name = 'Survey Value'
        
    def __repr__(self):
        sinq = ""
        inq = None
        if self.resource is not None:
            sinq = "Resource: "
            inq = self.resource
        if self.process is not None:
            sinq = "Process: "
            inq = self.process
        start = sinq + "%s\n Year: \n Type: %s\n Value: %5.2f%s \n" \
            % (inq,self.valuetype,self.value,self.unit,self.loc,self.ref)
        if self.loc != None: l = "\n Location: %s" % self.loc
        else: l = "No Location"
        if self.ref != None: ref = "\n Reference: %s" % self.ref
        else: ref = "\n Unsourced"
        return str(start+l+ref)
        
    def __unicode__(self):
        return self.__repr__()
   
# NEResourceInfo is designed to represent information extrapolated from a collection of data,
# as in a statistical survey or meta-study.
class NESurveyInfo(models.Model):
    resource = models.ForeignKey(NEResource,blank=True,null=True,related_name='surveyinfo_rsc')
    process = models.ForeignKey(NEProcess,blank=True,null=True,related_name='surveyinfo_proc')
    actor = models.ForeignKey('NEActor',blank=True,null=True,related_name='surveyinfo_act')
    startdate = models.DateField()
    enddate = models.DateField(blank=True,default=startdate)
    value = models.FloatField()
    valuetype = models.CharField(max_length=3,choices=valuetypes)
    infotype = models.CharField(max_length=1,choices=infotypes)
    records = []
    nrecords = 0
    
    objects = models.Manager()
    dataframe = DataFrameManager()    
    
    class Meta:
        verbose_name = 'Survey Info'
        verbose_name_plural = 'Survey Info'    
        
    
    def setRecords(self,records):
        rtype = type(records[0])
        refs = []
        if rtype == NEInfoCitation:
            self.records = records
            self.nrecords = records.nrecords
            return self.records
        if rtype == NECitation:
            for r in records:
                refs += [NEInfoCitation(iid=self, cid=r)]
            self.nrecords = len(refs)
        if rtype == NESurveyValue:
            for r in records:
                refs += [NEInfoCitation(cid=r.ref)]
            self.nrecords = len(refs)
        return refs

    
    def __repr__(self):
        sinq = ""
        inq = None
        if self.resource is not None:
            sinq = "Resource: "
            inq = self.resource
        if self.process is not None:
            sinq = "Process: "
            inq = self.process
        if self.actor is not None:
            sinq = "Actor: "
            inq = self.actor
        start = sinq + "%i Value: %5.2f Type: %s Start time: %s End time: %s" \
            % (inq,self.value, self.infotype,self.startdate.strftime("%Y"),self.enddate.strftime("%Y"))
        if self.loc is not None: l = "\n Location: %s" % self.loc
        else: l = "No Location"
        if self.ref is not None: ref = "\n Reference: %s" % self.ref
        else: ref = "Unsourced"
        return str(start+l+ref)
    def __unicode__(self):
        return self.__repr__()

class NEInfoCitation(models.Model):
    description = models.TextField(blank=True,default='')
    iid = models.ForeignKey(NESurveyInfo,related_name='info_citation')
    cid = models.ForeignKey(NECitation,related_name='meta_study')
    class Meta:
        verbose_name = 'Info Citation'
    
#NE Actor is the base class for organisms, organizations, and complex systems.
class NEActor(models.Model):
    name = models.CharField(max_length=30)
    parents = models.ManyToManyField('NEActor',related_name='actor_parent',blank=True,null=True)
    children = models.ManyToManyField('NEActor',related_name='actor_child',blank=True,null=True)
    atype = models.CharField(max_length=3,choices=atypes)
    class Meta:
        verbose_name = 'Actor'