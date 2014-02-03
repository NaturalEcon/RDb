from commonmodels import DESCRIPTION, NEOBJECT
from django.db import models
from managers import ResourceSurveyManager, DataFrameManager
from types import atypes, ptypes, ctypes
"""
basemodels.py Base classes for RDb.
Created on Sun Feb  2 22:48:46 2014

@author: acumen
"""

class NEResource(DESCRIPTION,NEOBJECT):
    """
    NEResource: NEOBJECT for materials and energy.
    :param dependencies: A many-to-many field for the resources this one is composed of or depend on to exist.
    :param subclasses: A many-to-many field for the resources that are more specialized cases of this one.
    :type surveys: ResourceSurveyManager.
    """
    dependencies = models.ManyToManyField('NEResource', related_name='fdeps',related_query_name='fdep', 
                                          through='NEDependency', symmetrical=False)
    subclasses   = models.ManyToManyField('NEResource', related_name='superclasses', related_query_name='superclass', 
                                          through='NERSubclass', symmetrical=False)
    surveys      = ResourceSurveyManager()    
    
    class Meta:
        verbose_name = 'Resource'
        app_label='RDb'
        db_table = 'RDb_neresource'
        
    def is_instance(self):
        return self.subclasses.first() is None
        
    def __repr__(self):
        return self.name
        
    def __unicode__(self):
        return self.__repr__()
        
        
class NEActor(NEOBJECT,DESCRIPTION):
    """
    NEActor: An NEOBJECT representing active systems, organisms, or other complexes with agency (externally).
    :param children: A many-to-many field for the children of this actor.
    :param subclasses: A many-to-many field for qualitative subclasses of this actor.
    :param atype: The type of actor that this is.  See the common models for the choices.
    """
    children = models.ManyToManyField('NEActor',related_name='actor_parents',blank=True,null=True)
    subclasses = models.ManyToManyField('NEActor',related_name='actor_superclass',blank=True,
                                        null=True,through='NEASubclass')
                                        
    atype = models.CharField(max_length=3,choices=atypes)

    class Meta:
        verbose_name = 'Actor'
        app_label='RDb'
        db_table = 'RDb_neactor'

    def is_instance(self):
        return self.subclasses.first() is None


class NEProcess(NEOBJECT,DESCRIPTION):
    """
    NEProcess: An NEOBJECT representing an interaction that results in a change from one set of NEOBJECTS to another.
    :param ptype: The type of process this is.  See the common models for the choices.
    :param subclasses: A many-to-many field for qualitative classfication of processes.
    :param io: A many-to-many field for the inputs and outputs of this process.
    """
    ptype = models.CharField(max_length=2,choices=ptypes,verbose_name='Process type')
    subclasses = models.ManyToManyField('NEProcess',related_name='process_superclass',blank=True,
                                        null=True,through='NEPSubclass')
    io = models.ManyToManyField( NEResource,through='NEProcessIO',symmetrical=False,
                                verbose_name='Inputs/Outputs',related_name='relevant_processes')
     
     
    class Meta:
        verbose_name = 'Process'
        verbose_name_plural = 'Processes'
        app_label='RDb'
        db_table = 'RDb_neprocess'

    def is_instance(self):
        return self.subclasses.first() is None
        
    def __repr__(self):
        return "%s (Type %s)\n Inputs: %s \n Outputs: %s" % (self.pname,self.get_ptype_display(),self.inputs,self.outputs)


class NERSubclass(DESCRIPTION):
    """
    NESubclass: Qualitative subgroup of NEOBJECTs.
    :param parent_class: The superclass in the relationship.
    :param child_class: The subclass in the relationship.
    """
    parent_class = models.ForeignKey(NEResource,related_name='rsubclasses',
                                     related_query_name='rsubclass')
    
    child_class = models.ForeignKey(NEResource,related_name='rsuperclasses',
                                     related_query_name='rsuperclass')
    
    class Meta:
        verbose_name = 'Subclass'
        verbose_name_plural = 'Subclasses'
        app_label='RDb'
        db_table = 'RDb_nersubclass'
    
    def __repr__(self):
        return 'Superclass: %s\nSubclass: %s' % (self.parent_class,self.child_class)
        
        
class NEPSubclass(DESCRIPTION):
    """
    NEPSubclass: Qualitative subgroup of NEProcesses.
    :param parent_class: The superclass in the relationship.
    :param child_class: The subclass in the relationship.
    """
    parent_class = models.ForeignKey(NEProcess,related_name='psubclasses',
                                     related_query_name='psubclass')
    
    child_class = models.ForeignKey(NEProcess,related_name='psuperclasses',
                                     related_query_name='psuperclass')
    
    class Meta:
        verbose_name = 'Subclass'
        verbose_name_plural = 'Subclasses'
        app_label='RDb'
        db_table = 'RDb_nepsubclass'        
    
    def __repr__(self):
        return 'Superclass: %s\nSubclass: %s' % (self.parent_class,self.child_class)
   


class NEASubclass(DESCRIPTION):
    """
    NEASubclass: Qualitative subgroup of NEActors.
    :param parent_class: The superclass in the relationship.
    :param child_class: The subclass in the relationship.
    """
    parent_class = models.ForeignKey(NEActor,related_name='asubclasses',
                                     related_query_name='asubclass')
    
    child_class = models.ForeignKey(NEActor,related_name='asuperclasses',
                                     related_query_name='asuperclass')
    
    class Meta:
        verbose_name = 'Subclass'
        verbose_name_plural = 'Subclasses'
        app_label='RDb'
        db_table = 'RDb_neasubclass'
        
    def __repr__(self):
        return 'Superclass: %s\nSubclass: %s' % (self.parent_class,self.child_class)
        
        
class NECitation(models.Model):
    """
    NECitation: A rudimentary citation data structure.
    :param title: The title of the cited work.
    :param author: The author of the cited work.
    :param date: The date on which the work was published.
    :param doi: The Document Object Identifier (DOI) for the work (optional).
    :param isbn: The International Standard Book Number (ISBN) for the work (optional).
    :param ctype: The type of work being cited.
    """
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
        app_label='RDb'
        db_table = 'RDb_necitation'
    
    def __repr__(self):
        output = ""
        if self.title is not None: output += self.title + ""
        if self.author is not None: 
            output += self.author + "."
        if self.doi is not None: output += self.doi + " "
        return output

    def __unicode__(self):
        return self.__repr__()        

class NECollection(DESCRIPTION):
    """NECollection: A group of heterogeneous NEOBJECTS."""
    
    class Meta:
        verbose_name= 'Collection'
        verbose_name_plural = 'Collections'
        app_label='RDb'
        db_table = 'RDb_necollection'