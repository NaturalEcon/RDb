from django.db import models
from managers import *
"""
Created on Fri Jan 31 12:31:24 2014

@author: acumen
:const rclasses: Classes of NEResource.
:const dtypes: Types of NEDependencies.
:const infotypes: Types of information.
:const valuetypes: Types of data. Incomplete.
:const ptypes: Types of processes.  Far from complete.
:const atypes: Types of actors.  Far from complete.
:class NEOBJECT: An abstract class representing an economically relevant object that is to be tracked by RDb.
:class DESCRIPTION: An abstract class to give a description set to RDb tables.
:class ABOUT: An abstract class for objects that are about NEObjects.
:class VALUE: An abstract float value field with a type and an optional unit.
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
atypes = ( ('org','Organization'),('ogn','Organism'),('sys','System'),('hom','Person') )
   

class NEOBJECT(Model):
    """
    NEOBJECT: An abstract class representing an economically relevant object that is to be tracked by RDb.
    :param neid: A UUID to use as the primary key for the object.
    :param objects: The default manager for the object.
    :param dataframe: Get a dataframe of the objects in this table.
    :type dataframe: DataFrameManager
    """
    neid = models.CharField(max_length=40,primary_key=True)
    objects = models.Manager()
    dataframe = DataFrameManager()

    class Meta:
        abstract=True    
        
        
class DESCRIPTION(models.Model):
    """
    DESCRIPTION: An abstract class to give a description set to RDb tables.
    :param name: The most common name for the object.
    :param short_name: The shortened name of this object.
    :param long_name: The most proper name for this object.
    :param description: A description for this object.
    """
    name = models.CharField(max_length=64)
    short_name = models.CharField(max_length=16,blank=True,default='')
    long_name = models.CharField(max_length=128,blank=True,default='')
    description = models.TextField()
    
    class Meta:
        abstract=True
        
class ABOUT(Model):
    """
    ABOUT: An abstract class for objects that are about NEObjects.
    :param resource: An optional foreign key for an NEResource.
    :param process: An optional foreign key for an NEProcess.
    :param actor: An optional foreign key for an NEActor.
    :param collection: An optional foreign key for an NECollection.
    :param subclass: An optional foreign key for an NESubclass.
    :param resources: Get all resources in this table.
    :param processes: Get all processes in this table.
    :param actors: Get all actors in this table.
    :param collections: Get all collections in this table.
    :param subclasses: Get all subclasses in this table.
    """
    resource = models.ForeignKey('NEResource', related_name='resource',null=True,blank=True)
    process = models.ForeignKey('NEProcess', related_name='process',null=True,blank=True)
    actor = models.ForeignKey('NEActor', related_name='actor',null=True,blank=True)
    collection = models.ForeignKey('NECollection', related_name='collection',null=True,blank=True)
    subclass = models.ForeignKey('NESubclass',related_name='subclass',null=True,blank=True)
    # Managers
    resources = ResourceManager()
    processes = ProcessManager()
    actors = ActorManager()
    collections = CollectionManager()
    subclasses = SubclassManager()

    class Meta:
        abstract=True
    
    
class VALUE(Model):
    """
    VALUE: An abstract float value field with a type and an optional unit.
    :param value: The value of this entry.
    :type value: django.models.FloatField
    :param value_type: The type of value of this entry.
    :param unit: The SI unit of this entry.
    """
    value = models.FloatField()
    value_type= models.CharField(max_length=9)
    unit = models.CharField(max_length=16,blank=True,null=True)

    class Meta:
        abstract=True
