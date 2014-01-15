from django.db import models
from managers import *

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
        ('EC','Embodied Carbon'),
        ('ECe','Embodied Carbon Equivalent')
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
    name = models.CharField(max_length=64)
    short_name = models.CharField(max_length=16,blank=True,default='')
    long_name = models.CharField(max_length=128,blank=True,default='')
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
    deps = models.ManyToManyField('NEResource', related_name='fdep',through='NEDependency',
                                         symmetrical=False,verbose_name='Dependency')
    objects = models.Manager()
    dataframe = DataFrameManager()
    
    class Meta:
        verbose_name = 'Resource'
    
    def __repr__(self):
        return self.name
    def __unicode__(self):
        return self.__repr__()
        
    
class NECollection(models.Model):
    collection_id = models.IntegerField(verbose_name='Collection ID')
    resource = models.ForeignKey(NEResource, related_name='rcollections',null=True,blank=True)
    process = models.ForeignKey('NEProcess', related_name='pcollections',null=True,blank=True)
    actors = models.ForeignKey('NEActor', related_name='acollections',null=True,blank=True)
    name = models.TextField(max_length=32,verbose_name='Collection name')
    class Meta:
        verbose_name= 'Resource Collection'
        verbose_name_plural = 'Resource Collections'
        unique_together = (('collection_id','resource'),('collection_id','process'),('collection_id','actors'),)
        
    def __repr__(self):
        return "Collection: %i, %s\n" % \
            (self.collection_id,self.resource.name)
    def __unicode__(self):
        return self.__repr__()
    
class NEDependency(models.Model):
    parent_resource = models.ForeignKey(NEResource,related_name='forward_dependency')
    dependency = models.ForeignKey(NEResource,related_name='backward_dependency')
    dependency_mult = models.FloatField(default=1.0,verbose_name='Dependency Multiplicity')
    
    class Meta:
        verbose_name_plural = 'Dependencies'
        unique_together = (('parent_resource','dependency'),)
    
    def __repr__(self):
        return "%5.2f x %s" % (self.dependency_mult, self.dependency)
    def __unicode__(self):
        return self.__repr__()
        
        
class NEMaterial(NEResource):
    description = models.TextField(blank=True,default='')
    current_standard = models.ForeignKey('NEMaterial',related_name='std_of_material_class',
                                         blank=True,null=True,
                                         verbose_name='Current Standard')
    mchildren = models.ManyToManyField('NEMaterial',related_name='mparents',
                                         symmetrical=False,verbose_name='Child Materials')
    objects = models.Manager()
    dataframe = DataFrameManager()
    
    class Meta:
        verbose_name = 'Material'
    
    def __repr__(self):
        return self.name
    def __unicode__(self):
        return self.__repr__()
    

class NEProduct(NEResource):
    description = models.TextField(blank=True,default='')
    pchildren = models.ManyToManyField('NEProduct',related_name='pparents',
                                         verbose_name='Child Products', symmetrical=False)
    objects = models.Manager()
    dataframe = DataFrameManager()

    class Meta:
        verbose_name = 'Product'        
    
    def __repr__(self):
        return self.name
    def __unicode__(self):
        return self.__repr__()     


class NEProperty(models.Model):
    resource = models.ForeignKey('NEResource',related_name='property_rsc',
                            blank=True,null=True,
                            verbose_name='Resource')
    process = models.ForeignKey('NEProcess',related_name='property_pro',
                            blank=True,null=True,
                            verbose_name='Process')
    actor = models.ForeignKey('NEActor',related_name='property_act',
                            blank=True,null=True,
                            verbose_name='Actor')
    name = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
    
    def __repr__(self):
        return '%s of %s: %f %s' % (self.name,self.rid,self.value,self.unit)
    def __unicode__(self):
        return self.__repr__()
        
        
# NE Process represents an industrial process or (limited scale) natural process.
class NEProcess(models.Model):
    pname = models.CharField(max_length=30,verbose_name='Process name')
    ptype = models.CharField(max_length=1,choices=ptypes,verbose_name='Process type')
    io = models.ManyToManyField( NEResource,through='NEProcessIO',symmetrical=False,
                                verbose_name='Inputs/Outputs',related_name='relevant_processes')
    description = models.TextField(blank=True,default='')
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
        
        
# NESurveyValue is intended to represent a single data point about a resource, process,
# actor, or property.
class NESurveyValue(models.Model):
    ###############################
    # ABOUT fields    
    # The first group of fields specifies what the survey is about.
    ###############################
    # If more than one of the following columns are non-null, then the relationship column should be filled.
    # Example usage: 'resource by actor', 'property of resource', 'resource from process'
    resource = models.ForeignKey(NEResource,blank=True,null=True,related_name='surveyvalue_rsc')
    process = models.ForeignKey(NEProcess,blank=True,null=True,related_name='surveyvalue_proc')
    actor = models.ForeignKey('NEActor',blank=True,null=True,related_name='surveyvalue_act')
    prop = models.ForeignKey('NEProperty',blank=True,null=True,related_name='surveyvalue_prp')
    # UNIX time of observation
    date = models.DateField()
    # Relationship is used for rows that contain data in two or more of the first four columns.
    relationship = models.CharField(max_length=6,default='Improperly Entered Row')    
    description = models.TextField(blank=True,null=True)
    # Value type.  See static 'valuetypes' definition for documentation.    
    valuetype = models.CharField(max_length=3,choices=valuetypes)
    value = models.FloatField()
    unit = models.CharField(max_length=10)
    # Location of the survey; May be replaced with "energy distance"
    location = models.TextField(verbose_name='Location')
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
# as in a statistical survey or meta-study, or data about collections of resources, processes,
# or actors.
class NESurveyInfo(models.Model):
    ###############################
    # ABOUT fields    
    # The first group of fields specifies what the survey is about.
    ###############################
    # If more than one of the following columns are non-null, then the relationship column should be filled.
    # Example usage: 'resource by collection', 'collection by actor', 'resource from process'
    resource = models.ForeignKey(NEResource,blank=True,null=True,related_name='surveyinfo_rsc')    
    collection = models.ForeignKey(NECollection,blank=True,null=True,related_name='surveyinfo_col')
    process = models.ForeignKey(NEProcess,blank=True,null=True,related_name='surveyinfo_proc')
    actor = models.ForeignKey('NEActor',blank=True,null=True,related_name='surveyinfo_act')
    # Relationship is used for rows that contain data in two or more of the first four columns.
    # For now the database will just contain the information, without the application having much use for it.
    relationship = models.CharField(max_length=6,default='Improperly Entered Row')    
    description = models.TextField(blank=True,null=True)
    
    startdate = models.DateField()
    enddate = models.DateField(blank=True,default='2050-01-01')
    
    value = models.FloatField()
    # Specifies what is being quantified
    valuetype = models.CharField(max_length=3,choices=valuetypes)
    unit = models.CharField(max_length=10)
    # Specifies the type of quantification.
    infotype = models.CharField(max_length=1,choices=infotypes)
    records = models.ManyToManyField('NECitation',through='NEInfoCitation',
                                     related_name='cited_by',symmetrical=True)
    location = models.TextField(verbose_name='Location')
    
    objects =   models.Manager()
    resources = ResourceSurveyManager()
    processes = ProcessSurveyManager()
    actors =    ActorSurveyManager()
    collections = CollectionSurveyManager()
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
        if self.collection is not None:
            sinq = "Collection: "
            inq = self.collection
        start = sinq + "%s Value: %5.2f Type: %s Start time: %s End time: %s" \
            % (inq,self.value, self.infotype,self.startdate.strftime("%Y"),self.enddate.strftime("%Y"))
        if self.location is not None: l = "\n Location: %s" % self.location
        else: l = "No Location"
        return str(start+l)
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
    children = models.ManyToManyField('NEActor',related_name='actor_parents',blank=True,null=True)
    atype = models.CharField(max_length=3,choices=atypes)
    class Meta:
        verbose_name = 'Actor'