from django.db import models
from managers import *
from types import value_types
"""
commonmodels.py: Abstract models shared by all other model modules.
Created on Fri Jan 31 12:31:24 2014

@author: acumen
:const valuetypes: Value type choices for VALUE.
:class NEOBJECT: An abstract class representing an economically relevant object that is to be tracked by RDb.
:class DESCRIPTION: An abstract class to give a description set to RDb tables.
:class ABOUT: An abstract class for objects that are about NEObjects.
:class VALUE: An abstract float value field with a type and an optional unit.
"""  

class NEOBJECT(models.Model):
    """
    NEOBJECT: An abstract class representing an economically relevant object that is to be tracked by RDb.
    :param neid: A UUID to use as the primary key for the object.
    :param dataframe: Get a dataframe of the objects in this table.
    :type dataframe: DataFrameManager
    """
    neid = models.CharField(max_length=40,primary_key=True)
    objects = models.Manager()
    dataframe = DataFrameManager()

    class Meta:
        abstract=True    
        app_label='RDb'
    
    
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
        app_label='RDb'
        
        
class ABOUT(models.Model):
    """
    ABOUT: An abstract class for objects that are about NEObjects.
    Fields:
    :param resource: An optional foreign key for an NEResource.
    :param process: An optional foreign key for an NEProcess.
    :param actor: An optional foreign key for an NEActor.
    :param collection: An optional foreign key for an NECollection.
    Managers:
    :type objects: An ABOUTManager, which has a function for each NEOBJECT type.
    """
    resource = models.ForeignKey('NEResource',null=True,blank=True)
    process = models.ForeignKey('NEProcess', null=True,blank=True)
    actor = models.ForeignKey('NEActor', null=True,blank=True)
    collection = models.ForeignKey('NECollection', null=True,blank=True)
    # Managers
    objects = ABOUTManager()

    class Meta:
        abstract=True
        app_label='RDb'
    
    
class VALUE(models.Model):
    """
    VALUE: An abstract float value field with a type and an optional unit.
    :param value: The value of this entry.
    :type value: django.models.FloatField
    :param value_type: The type of value of this entry.
    :param unit: The SI unit of this entry.
    """
    value = models.FloatField()
    value_type= models.CharField(max_length=9,choices=value_types)
    unit = models.CharField(max_length=16,blank=True,null=True)

    class Meta:
        abstract=True
        app_label='RDb'
