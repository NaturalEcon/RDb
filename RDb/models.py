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
    rid = models.CharField(max_length=40,primary_key=True)
    name = models.CharField(max_length=64)
    short_name = models.CharField(max_length=16,blank=True,default='')
    long_name = models.CharField(max_length=128,blank=True,default='')
    description = models.TextField()
    dependencies = models.ManyToManyField('NEResource', related_name='fdeps',related_query_name='fdep', 
                                          through='NEDependency', symmetrical=False)
    subclasses   = models.ManyToManyField('NEResource', related_name='superclasses', related_query_name='superclass', 
                                          through='NESubclass', symmetrical=False)
                                          
    objects = models.Manager()
    dataframe = DataFrameManager()
    
    class Meta:
        verbose_name = 'Resource'
    
    def __repr__(self):
        return self.name
    def __unicode__(self):
        return self.__repr__()

        
#NE Actor is the base class for organisms, organizations, and complex systems.
class NEActor(models.Model):
    name = models.CharField(max_length=30)
    children = models.ManyToManyField('NEActor',related_name='actor_parents',blank=True,null=True)
    atype = models.CharField(max_length=3,choices=atypes)
    
    class Meta:
        verbose_name = 'Actor'

        
# NE Process represents an industrial process or (limited scale) natural process.
class NEProcess(models.Model):
    name = models.CharField(max_length=64,verbose_name='Process name')
    ptype = models.CharField(max_length=1,choices=ptypes,verbose_name='Process type')
    io = models.ManyToManyField( NEResource,through='NEProcessIO',symmetrical=False,
                                verbose_name='Inputs/Outputs',related_name='relevant_processes')
    description = models.TextField(blank=True,default='')
    
    objects = models.Manager()
    dataframe = DataFrameManager()
     
    class Meta:
        verbose_name = 'Process'
        verbose_name_plural = 'Processes'

    def __repr__(self):
        return "%s (Type %s)\n Inputs: %s \n Outputs: %s" % (self.pname,self.ptype,self.inputs,self.outputs)

class NEProperty(models.Model):
#    resource = models.ForeignKey(NEResource, related_name='rproperties',null=True,blank=True)
#    process = models.ForeignKey('NEProcess', related_name='pproperties',null=True,blank=True)
#    actor = models.ForeignKey('NEActor', related_name='aproperties',null=True,blank=True)
    pname = models.CharField(max_length=64,verbose_name='Property name')
    description = models.TextField()
    value = models.FloatField()
    error = models.FloatField()
    
    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'

# An adjacency table for NE Process inputs and outputs
class NEProcessIO(models.Model):
    pid = models.ForeignKey(NEProcess,related_name='process',verbose_name='Process')
    pname = models.CharField(max_length=64)
    arg_id = models.ForeignKey(NEResource,related_name='process_arg',verbose_name='Argument')
    arg_name = models.CharField(max_length=64,verbose_name='Argument Name')
    arg_weight = models.FloatField(default=1.0,verbose_name='Argument weight')
    arg_type = models.CharField(max_length=1,choices=argtypes,verbose_name='Argument type')
    class Meta:
        verbose_name = 'Process IO'
        verbose_name_plural = 'Process IO'
    
    def __repr__(self):
        return '%s: %f x %s' % (self.pname,self.arg_weight,self.arg_name)
    def __unicode__(self):
        return self.__repr__()

# A collection of resources, processes, or actors.        
class NECollection(models.Model):
    collection_id = models.IntegerField(verbose_name='Collection ID')
    collection_name = models.CharField(max_length=128,blank=True,null=True)
    resource = models.ForeignKey(NEResource, related_name='rcollections',null=True,blank=True)
    process = models.ForeignKey('NEProcess', related_name='pcollections',null=True,blank=True)
    actor = models.ForeignKey('NEActor', related_name='acollections',null=True,blank=True)

    class Meta:
        verbose_name= 'Collection'
        verbose_name_plural = 'Collections'
        
    def __repr__(self):
        output = '#%i:' % self.collection_id
        if self.resource is not None:
            output += ' %s ' % self.resource
        if self.process is not None:
            output += ' %s ' % self.process
        if self.actor is not None:
            output += ' %s ' % self.actor
        return output
        
    def __unicode__(self):
        return self.__repr__()

# An adjacency table for the composition of a complex resource    
class NEDependency(models.Model):
    parent_resource = models.ForeignKey(NEResource,related_name='backward_dependencies',
                                        related_query_name='backward_dependency')
    dependency = models.ForeignKey(NEResource,related_name='forward_dependencies',
                                        related_query_name='forward_dependency')
    dependency_mult = models.FloatField(default=1.0,verbose_name='Dependency Multiplicity')
    
    class Meta:
        verbose_name = 'Dependency'
        verbose_name_plural = 'Dependencies'
        unique_together = (('parent_resource','dependency'),)
    
    def __repr__(self):
        return "%s requires %5.2f x %s" % (self.parent_resource,self.dependency_mult,self.dependency)
    def __unicode__(self):
        return self.__repr__()

# An adjacency table for classification
class NESubclass(models.Model):
    parent_class = models.ForeignKey(NEResource,related_name='parent_classes',
                                     related_query_name='parent_class')
    parent_name = models.CharField(max_length=64)
    child_class = models.ForeignKey(NEResource,related_name='child_classes',
                                     related_query_name='child_class')
    child_name = models.CharField(max_length=64)
    description = models.TextField()
    
    class Meta:
        verbose_name = 'Subclass'
        verbose_name_plural = 'Subclasses'
    
    def __repr__(self):
        return 'Superclass: %s\nSubclass: %s' % (self.parent_class,self.child_class)
        
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
        if self.title is not None: output += self.title + ""
        if self.author is not None: 
            output += self.author + "."
        if self.doi is not None: output += self.doi + " "
        return output

    def __unicode__(self):
        return self.__repr__()        
        
        
# NESurveyValue is intended to represent a single data point about a resource, process, or actor
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
    # UNIX time of observation
    date = models.DateField(auto_now_add=True)
    # Relationship is used for rows that contain data in two or more of the first four columns.
    relationship = models.CharField(max_length=6,default='Improperly Entered Row')    
    # name = models.CharField(max_length=64,blank=True,null=True)
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
        output = ''
        if self.resource is not None:
            output = '%s(%s): %f %s' % (self.valuetype,self.resource,self.value,self.unit)
        elif self.process is not None:
            output = '%s(%s): %f %s' % (self.valuetype,self.process,self.value,self.unit)
        elif self.actor is not None:
            output = '%s(%s): %f %s' % (self.valuetype,self.actor,self.value,self.unit)
        else:
            'Ambiguous survey.  Please delete or re-enter.'
        return output  
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
    resource = models.ForeignKey(NEResource,blank=True,related_name='surveyinfo_rsc',default="302f5076-7f8e-11e3-bc66-f07bcb4eb64e")    
    collection = models.ForeignKey(NECollection,blank=True,null=True,related_name='surveyinfo_col')
    process = models.ForeignKey(NEProcess,blank=True,null=True,related_name='surveyinfo_proc')
    actor = models.ForeignKey('NEActor',blank=True,null=True,related_name='surveyinfo_act')
    # Relationship is used for rows that contain data in two or more of the first four columns.
    # For now the database will just contain the information, without the application having much use for it.
    relationship = models.CharField(max_length=6,default='')    
    description = models.TextField(blank=True,null=True)
    
    startdate = models.DateField(auto_now_add=True,blank=True,null=True)
    enddate = models.DateField(auto_now_add=True,blank=True,null=True)
    
    value = models.FloatField()
    # Specifies what is being quantified
    valuetype = models.CharField(max_length=3,choices=valuetypes)
    unit = models.CharField(max_length=10)
    # Specifies the type of quantification.
    infotype = models.CharField(max_length=1,choices=infotypes,default="u")
    record = models.ForeignKey('NECitation',null=True,blank=True)
    #records = models.ManyToManyField('NECitation',through='NEInfoCitation',
    #                                 related_name='cited_by',symmetrical=True)
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
    
    def __repr__(self):
        output = ''
        if self.collection is not None and self.resource is not None:
            output = '%s(%s %s %s): %f %s' % (self.valuetype,self.resource,self.relationship,self.collection,self.value,self.unit)
        elif self.collection is not None and self.process is not None:
            output = '%s(%s %s %s): %f %s' % (self.valuetype,self.process,self.relationship,self.collection,self.value,self.unit)
        elif self.collection is not None and self.actor is not None:
            output = '%s(%s %s %s): %f %s' % (self.valuetype,self.actor,self.relationship,self.collection,self.value,self.unit)
        elif self.resource is not None:
            output = '%s(%s): %f %s' % (self.valuetype,self.resource,self.value,self.unit)
        elif self.process is not None:
            output = '%s(%s): %f %s' % (self.valuetype,self.process,self.value,self.unit)
        elif actor is not None:
            output = '%s(%s): %f %s' % (self.valuetype,self.actor,self.value,self.unit)
        else:
            'Ambiguous survey.  Please delete or re-enter.'
        return output
    def __unicode__(self):
        return self.__repr__()


class NEInfoCitation(models.Model):
    description = models.TextField(blank=True,default='')
    iid = models.ForeignKey(NESurveyInfo,related_name='info_citation')
    cid = models.ForeignKey(NECitation,related_name='meta_study')
    class Meta:
        verbose_name = 'Info Citation'